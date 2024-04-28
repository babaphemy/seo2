from .schema import ClassroomDto, SubjectDto, LessonDto, TopicDto
from .models import Classroom, Subject, Lesson, Topic, Quiz, LessonNote, LessonAssets
from typing import Union, List, Optional
from espy_contact.util.enums import AccessRoleEnum
from siteseo.app.campus.app.util import converter
from siteseo.app.campus.app.info.models import Appuser, Student
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, orm
from sqlalchemy.orm import exc


def add_class(classroom: str, db: Session) -> bool:
    try:
        new_class = Classroom(title=classroom)
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return True
    except IntegrityError:
        db.rollback()
        return False


def find_all_classes(db: Session) -> list[ClassroomDto]:
    classes = db.query(Classroom).options(orm.joinedload(Classroom.subjects)).all()
    return classes


def find_class_by_title(title: str, db: Session) -> ClassroomDto:
    cl = (
        db.query(Classroom)
        .filter(func.lower(Classroom.title) == func.lower(title))
        .first()
    )
    return ClassroomDto(id=cl.id, title=cl.title, timestamp=cl.timestamp, subjects=cl.subjects)


def find_class_by_id(cid: str, db: Session) -> ClassroomDto:
    cl = (
        db.query(ClassroomDto)
        .select_from(Classroom)
        .filter(Classroom.id == cid)
        .first()
    )
    return cl


def add_teacher(tid: str, cid: str, db: Session) -> Union[bool, str]:
    """Adds a user (teacher) to a class.
        Args:
        tid (str): The ID of the user (teacher).
        cid (str): The ID of the class.
        db (Session): The SQLAlchemy database session.

    Returns:
        bool: True if the user was successfully added as a teacher, False otherwise.

    Raises:
        Exception: If an error occurs during the process.
    """
    # validate is teacher and active
    try:
        user = db.query(Appuser).filter(Appuser.id == tid).first()
        if not user:
            raise Exception(f"No user with ID {tid} .")
        if user.is_active is False:
            raise Exception(f"User with ID '{tid}' is not active.")
        if not AccessRoleEnum.TEACHER not in user.roles:
            raise Exception(f"User with ID '{tid}' does not have the 'Teacher' role.")
        classroom = db.query(Classroom).filter(Classroom.id == cid).first()
        if not Classroom:
            raise Exception(f"Class with ID '{cid}' not found!")
        classroom.teacher_id = user.id
        db.add(classroom)
        db.commit()
        return True
    except IntegrityError as e:
        raise Exception(f"Error adding teacher: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


def add_subject(subject: SubjectDto, db: Session) -> SubjectDto:
    try:
        cid = subject.class_id
        cl = db.query(Classroom).get(cid)
        if not cl:
            raise Exception(f"No Class with ID {cid} .")
        subj = Subject(
            title=subject.title,
            grade=subject.grade,
            term=subject.term,
            class_id=cl.id,
        )
        # Process topics
        for topic_data in subject.topics:
            topic: Topic = Topic(title=topic_data.title, subject=subj)
            for lesson_data in topic_data.lessons:
                lesson = Lesson(
                    title=lesson_data.title,
                    topic=topic,
                )
                if "note" in lesson_data:
                    lesson.note = LessonNote(
                        title=lesson_data.note.title, content=lesson_data.note.content
                    )
                if "quiz" in lesson_data:
                    lesson.quiz = Quiz(**lesson_data.quiz)  # Unpack quiz data
                if "assets" in lesson_data:
                    lesson.assets = LessonAssets(asset=lesson_data.assets[0])
                if topic.lessons is None:
                    topic.lessons = []
                else:
                    topic.lessons.append(lesson)
        if subj.topics is None:
            subj.topics = []
            subj.topics.append(topic)
        else:
            subj.topics.append(topic)
        db.add(subj)
        db.commit()
        db.refresh(subj)
        subject.id = subj.id
        return subject
    except Exception as e:
        raise Exception(f"An error occured: {str(e)}.")


def subject_all(db: Session) -> list[SubjectDto]:
    subjs = db.query(Subject).all()
    resp = [
        SubjectDto(
            id=s.id,
            title=s.title,
            class_id=s.classroom.id,
            grade=s.grade,
            term=s.term,
            lesson_count=len(s.topics),
        )
        for s in subjs
    ]
    return resp


def add_student_class(student_ids: List[str], cid: str, db: Session) -> bool:
    """Adds bulk students to a class.

    Args:
        student_ids: List of student IDs to add.
        cid: The class ID to add students to.
        db: The database session object.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Get the classroom object
        classroom = db.query(Classroom).get(cid)
        if not classroom:
            raise ValueError(f"No classroom with ID {cid}")

        # Check if students exist (using bulk in operator)
        existing_students = db.query(Student).filter(Student.id.in_(student_ids)).all()
        student_ids_to_add = [
            sid for sid in student_ids if sid not in [s.id for s in existing_students]
        ]

        # Check if students are already in another class (optional)
        # This requires additional logic depending on your database schema
        # ... (implement logic to check if students are already assigned to another class)

        # Add students to the class relationship (avoid duplicate addition)
        for sid in student_ids_to_add:
            student = db.query(Student).get(sid)
            if student:
                classroom.students.append(student)
            else:
                # Handle case where student wasn't found (optional)
                print(f"Student with ID {sid} not found, skipping")

        # Commit changes
        db.commit()
        return True

    except exc.IntegrityError as e:
        # Handle potential duplicate key errors
        print(f"Error adding students: {e}")
        db.rollback()
        return False
    except Exception as e:
        raise e


def subjects_by_class(cid: str, db: Session) -> List[SubjectDto]:
    """
    Retrieves all SubjectDto objects associated with a given classroom ID.

    Args:
        cid (str): The ID of the classroom.
        db (Session): Database session object.

    Returns:
        List[SubjectDto]: A list of SubjectDto objects representing subjects in the classroom.
    """

    # Use eager loading to efficiently fetch associated lessons
    subjects = (
        db.query(Subject)
        .options(orm.joinedload("lessons"))
        .filter(Subject.class_id == cid)
        .all()
    )

    # Convert subjects to SubjectDto objects
    subjects_dto = [SubjectDto(**subject.__dict__) for subject in subjects]
    return subjects_dto


def subject_by_id(sid: str, db: Session) -> Optional[SubjectDto]:
    """
    Finds a subject by its ID and returns a SubjectDto object.

    Args:
        sid (str): The ID of the subject to search for.
        db (Session): Database session object.

    Returns:
        Optional[SubjectDto]: A single SubjectDto object representing the subject, or None if not found.
    """
    try:
        su = db.query(Subject).options(joinedload(Subject.topics)).get(sid)
        if not su:
            raise ValueError(f"no subject wit id {sid}")
        return SubjectDto(
            id=su.id,
            title=su.title,
            term=su.term,
            timestamp=su.timestamp,
            class_id=su.class_id,
            grade=su.grade,
            topics=converter.topics_to_dtos(su.topics),
        )
    except Exception as e:
        raise e


def add_topic(topic: TopicDto, db: Session) -> SubjectDto:
    try:
        sid = topic.subject_id
        if not sid:
            raise ValueError("Subject ID is required to add a topic.")
        subject = db.query(Subject).get(sid)
        if not subject:
            raise ValueError(f"Subject with ID '{sid}' not found.")
        new_topic = Topic(**topic.__dict__)
        new_topic.subject_id = sid
        subject.topics.append(new_topic)
        db.add(new_topic)
        db.commit()
        return SubjectDto(**subject.__dict__)

    except Exception as e:
        db.rollback()
        raise e


def add_lesson(lesso: LessonDto, db: Session) -> None:
    try:
        topic = db.query(Topic).filter(Topic.id == lesso.topic_id).first()
        if not topic:
            raise ValueError(f"Topic with ID '{lesso.topic_id}' not found.")
        new_lesson = Lesson(title=lesso.title, topic_id=topic.id)
        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)
    except Exception as e:
        raise e


def find_topics_by_subject_id(sid: str, db: Session) -> List[TopicDto]:
    """
    Finds all Topic objects associated with a given subject ID.

    Args:
        sid (str): The ID of the subject to search for topics.
        db (Session): Database session object.

    Returns:
        List[Topic]: A list of Topic objects related to the subject, or an empty list if none found.
    """

    # Employ eager loading for efficient retrieval of associated topics
    topics = db.query(Topic).filter(Topic.subject_id == sid).all()
    # topics = (
    #     db.query(Topic)
    #     .options(
    #         orm.joinedload(Topic.subject)
    #     )  # Load topics with their subject relationship
    #     .filter(
    #         Topic.subject_id == sid
    #     )  # Filter for topics associated with the subject
    #     .all()
    # )
    topics_dto = converter.topics_to_dtos(topics)

    return topics_dto


# def make_lesson(l: Lesson ) -> LessonDto:
#     """
#     Creates a LessonDto instance from a Lesson object.
#     """
#     return LessonDto(id=l.id, title=l.title, note=l.note, assets=l.assets, subject_id=l.subject_id)
def find_lessons_by_topic_id(db: Session, topic_id: str) -> List[LessonDto]:
    """
    Finds all lessons associated with a given subject ID.

    Args:
        db (Session): Database session object.
        subject_id (str): The ID of the subject to search for.

    Returns:
        List[Lesson]: A list of Lesson objects matching the subject ID.
    """
    # Use eager loading to efficiently fetch associated notes and assets
    resp = (
        db.query(LessonDto)
        .select_from(Lesson)
        .options(orm.joinedload("note"), orm.joinedload("assets"))
        .filter(Lesson.topic_id == topic_id)
        .all()
    )
    return resp


def find_lesson_by_id(db: Session, lesson_id: str) -> LessonDto:
    """
    Finds a lesson by its ID.

    Args:
        db (Session): Database session object.
        lesson_id (str): The ID of the lesson to search for.

    Returns:
        Lesson: A single Lesson object matching the ID, or None if not found.
    """
    # Use get() to efficiently fetch a single lesson by ID
    lesson = (
        db.query(LessonDto)
        .select_from(Lesson)
        .options(orm.joinedload("note"), orm.joinedload("assets"))
        .filter(Lesson.id == lesson_id)
    )
    return lesson


def add_review():
    pass


def add_resource():
    pass


def create_note():
    pass


def add_quiz():
    pass


def add_quiz_option():
    pass


def create_lesson():
    pass


def add_quiz_lesson():
    pass


def add_asset_lesson():
    pass


def add_lesson_subject():
    pass
