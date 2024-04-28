from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union, List
from .schema import ClassroomDto, SubjectDto, LessonDto, TopicDto
from .models import Lesson
from siteseo.app.db.session import get_db
from . import service

router = APIRouter(prefix="/classroom", tags=["classroom"])


@router.post("/")
def add_class(class_name: str, db: Session = Depends(get_db)) -> Union[bool, str]:
    return service.add_class(classroom=class_name, db=db)


@router.get("/")
def all_class(db: Session = Depends(get_db)) -> list[ClassroomDto]:
    return service.find_all_classes(db=db)


@router.get("/title")
def by_title(title: str, db: Session = Depends(get_db)) -> ClassroomDto:
    return service.find_class_by_title(title=title, db=db)


@router.get("/byid")
def class_by_id(cid: str, db: Session = Depends(get_db)) -> ClassroomDto:
    return service.find_class_by_id(cid, db)


@router.patch("/teacher/add")
def add_teacher(tid: str, cid: str, db: Session = Depends(get_db)) -> str:
    try:
        return service.add_teacher(tid, cid, db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/subject/add")
def add_subject(subject: SubjectDto, db: Session = Depends(get_db)):
    try:
        return service.add_subject(subject=subject, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/subject/all")
def subject_all(db: Session = Depends(get_db)) -> List[SubjectDto]:
    return service.subject_all(db)


def subject_by_class(cid: str, db: Session = Depends(get_db)) -> SubjectDto:
    return service.subjects_by_class(cid, db)


@router.get("/subject/one")
def one_subject(sid: str, db: Session = Depends(get_db)) -> SubjectDto:
    try:
        return service.subject_by_id(sid, db)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/subject/topics")
def subj_topics(sid: str, db: Session = Depends(get_db)) -> list[TopicDto]:
    return service.find_topics_by_subject_id(sid, db)


@router.post("/subject/topic")
def add_topic(topic: TopicDto, db: Session = Depends(get_db)) -> SubjectDto:
    return service.add_topic(topic, db)


def topic_by_id(tid: str, db: Session = Depends(get_db)):
    pass


@router.get("/subject/lesson")
def get_Lesson(lid: str, db: Session = Depends(get_db)) -> LessonDto:
    return service.find_lesson_by_id(db, lid)


def get_lessons(tid: str, db: Session = Depends(get_db)) -> List[LessonDto]:
    pass
