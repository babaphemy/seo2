from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from espy_contact.util.enums import ResourceEnum, GradeLevel
from .models import Term
import uuid


class Resource(BaseModel):
    """Type of resource can be Poll, Form Builder, Questionnaire, RichText, Video, Audio, File, Hyperlink."""

    id: Optional[str] = str(uuid.uuid4())
    title: str
    type: ResourceEnum
    lesson_id: str


class Lesson_note(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: str
    content: str
    lesson_id: Optional[str] = None


class Quiz(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: str
    question: str
    options: List[str]
    answer: str
    lesson_id: Optional[str] = None


class Lesson(BaseModel):  # defintion of biology, branches of biology
    id: Optional[str] = str(uuid.uuid4())
    title: str  # Intro to Biology
    quiz: Optional[Quiz] = None
    note: Optional[Lesson_note] = None
    assets: Optional[
        List[str]
    ] = []  # these are assets shared between users not same as resources
    resources: Optional[List[ResourceEnum]] = []
    topic_id: Optional[str] = None


class LessonDto(Lesson):
    class_id: Optional[str] = None


class Topic(BaseModel):  # Introduction to Biology
    id: Optional[str] = str(uuid.uuid4())
    title: str
    timestamp: Optional[datetime] = None
    subject_id: Optional[str] = None
    lessons: Optional[List[Lesson]] = []


class TopicDto(Topic):
    age: Optional[datetime] = datetime


class SubjectDto(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: str  # Biology
    class_id: Optional[str] = None  # Grade
    grade: Optional[GradeLevel] = None
    term: Term
    topics: Optional[List[Topic]] = None
    lesson_count: Optional[int] = 0


class ClassroomDto(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: str
    subjects: Optional[List[SubjectDto]]
    # teachers: List[Teacher]  # ManyToMany relationship with Teacher


class Review(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: str
    review: str
    rating: float
    reviewer: str
    created_at: datetime
    subject: SubjectDto
