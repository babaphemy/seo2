from siteseo.app.db.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, Float
from espy_contact.util.enums import ResourceEnum, GradeLevel, Term
import uuid


class Resource(Base):
    """Type of resource can be Poll, Form Builder, Questionnaire, RichText, Video, Audio, File, Hyperlink."""

    __tablename__ = "resources"
    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime(), server_default=func.now())
    title = Column(String)
    type = Column(Enum(ResourceEnum))
    lesson_id = Column(String, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", foreign_keys=[lesson_id])


# class QuizOption(Base):
#     __tablename__ = "quiz_options"
#     id = Column(String, primary_key=True, index=True)
#     option_text = Column(String)
#     quiz_id = Column(String, ForeignKey("quizzes.id"))
#     quiz = relationship("Quiz", back_populates="options", foreign_keys=[quiz_id])

# class Quiz(Base):
#     __tablename__ = "quizzes"
#     id = Column(String, primary_key=True, index=True)
#     question = Column(String)
#     options = relationship("QuizOption", back_populates="quiz",foreign_keys=[QuizOption.quiz_id])
#     answer_id = Column(String, ForeignKey("quiz_options.id"))
#     answer = relationship("QuizOption",foreign_keys=[answer_id])
#     lesson_id = Column(String, ForeignKey("lessons.id"))
#     lesson = relationship("Lesson", foreign_keys=[lesson_id])


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    question = Column(String)
    options = Column(JSON)  # Store options as JSON
    answer = Column(String)
    lesson_id = Column(String, ForeignKey("lessons.id"))
    Lesson = relationship("Lesson", foreign_keys=[lesson_id])


class LessonNote(Base):
    __tablename__ = "lesson_notes"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    title = Column(String)
    lesson = relationship("Lesson", back_populates="note")


class LessonResource(Base):
    __tablename__ = "lesson_resource"

    lesson_id = Column(String, ForeignKey("lessons.id"), primary_key=True)
    resource_id = Column(String, ForeignKey("resources.id"), primary_key=True)


class LessonAssets(Base):
    __tablename__ = "lessons_assets"
    asset = Column(String)
    lesson_id = Column(String, ForeignKey("lessons.id"), primary_key=True)
    lesson = relationship("Lesson", back_populates="assets")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    note_id = Column(String, ForeignKey("lesson_notes.id"))
    note = relationship("LessonNote", back_populates="lesson")
    assets = relationship(
        "LessonAssets", back_populates="lesson"
    )  # Consider using a separate table for assets
    topic_id = Column(String, ForeignKey("topics.id"))
    quiz_id = Column(String, ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", foreign_keys=[quiz_id])


class Topic(Base):
    __tablename__ = "topics"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    title = Column(String)
    lessons = relationship("Lesson", backref="topic")
    subject_id = Column(String, ForeignKey("subjects.id"))
    timestamp = Column(DateTime(), server_default=func.now())


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    title = Column(String)
    grade = Column(Enum(GradeLevel))
    topics = relationship("Topic", backref="subject")
    term = Column(Enum(Term))
    reviews = relationship("Review", backref="reviewed_subject")
    class_id = Column(String, ForeignKey("classrooms.id"))
    classroom = relationship("Classroom", back_populates="subjects")


class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    title = Column(String, unique=True)
    timestamp = Column(DateTime(), server_default=func.now())
    teacher_id = Column(String, ForeignKey("appusers.id"), nullable=True)
    teacher = relationship("Appuser")  # Optional backref
    school_id = Column(String)

    subjects = relationship("Subject", back_populates="classroom")
    students = relationship("Student", back_populates="classroom")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    title = Column(String)
    review = Column(String)
    rating = Column(Float)
    reviewer = Column(String)
    created_at = Column(DateTime)
    subject_id = Column(String, ForeignKey("subjects.id"))
    # reviewed_subject = relationship("Subject", foreign_keys=[subject_id])


class ClassroomSubject(Base):
    __tablename__ = "classroom_subjects"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    classroom_id = Column(String, ForeignKey("classrooms.id"))
    subject_id = Column(String, ForeignKey("subjects.id"))
