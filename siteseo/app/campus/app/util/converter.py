import json
from pydantic import TypeAdapter
from siteseo.app.campus.app.classroom.schema import TopicDto, LessonDto
from siteseo.app.campus.app.classroom.models import Topic
from siteseo.app.campus.app.info.models import Enrollment
from siteseo.app.campus.app.info.schema import EnrollmentDto, AddressDto
from siteseo.app.campus.app.horace.model import CurriculumMap
from typing import List
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed version.
    """
    # Ensure both plain_password and hashed_password are bytes
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def encrypt_pass(plain_password: str) -> str:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode(), salt).decode()


# def to_topic_dto(topics: List[Topic]) -> List[TopicDto]:
#     """Converts a list of Topic objects to TopicDto objects."""
#     topic_dtos = []
#     for topic in topics:
#         lesson_dtos = []
#         for lesson in topic.lessons:
#             lesson_data = {}
#             for column in inspect(lesson).columns:
#                 lesson_data[column.name] = getattr(lesson, column.name)
#             lesson_dtos.append(LessonDto(**lesson_data))
#         topic_dto = TopicDto(
#             **{attr.name: getattr(topic, attr.name) for attr in inspect(topic).attrs},
#             age=datetime.now(),
#             lessons=lesson_dtos,
#         )
#         topic_dtos.append(topic_dto)
#     return topic_dtos


def topics_to_dtos(topics: List[Topic]) -> List[TopicDto]:
    """Converts a list of Topic objects to TopicDto objects."""
    topic_dtos = []
    for topic in topics:
        lesson_dtos = []
        for lesson in topic.lessons:
            lesson_data = LessonDto(
                id=lesson.id, title=lesson.title, topic_id=lesson.topic_id
            )
            # add asset note quiz
            lesson_dtos.append(lesson_data)
        topic_dto = TopicDto(
            id=topic.id,
            lessons=lesson_dtos,
            title=topic.title,
            timestamp=topic.timestamp,
        )
        topic_dtos.append(topic_dto)
    return topic_dtos


def to_enrollment(enrol: Enrollment) -> EnrollmentDto:
    dto_data = enrol.__dict__
    return EnrollmentDto(
        **dto_data,
        first_name=enrol.user.first_name,
        last_name=enrol.user.last_name,
        email=enrol.user.email,
        role=enrol.user.roles,
        address=AddressDto(
            id=enrol.user.address.id,
            street=enrol.user.address.street,
            city=enrol.user.address.city,
            state=enrol.user.address.state,
            zip_code=enrol.user.address.zip_code,
            country=enrol.user.address.country,
            phone_number=enrol.user.address.phone_number,
        ),
    )
def read_json(curriculum_json: str) -> CurriculumMap:
    # Assuming curriculum_json is a JSON string from the database
    curriculum_data = json.loads(curriculum_json)
    adapter = TypeAdapter(CurriculumMap)
    validated_curriculum = adapter.validate_python(curriculum_data)
    return validated_curriculum

