from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from siteseo.app.campus.app.info.schema import UserResponse
from siteseo.app.campus.app.db.mongodb_utils import get_db
from .model import UserCol, CurriculumMap,CourseItem
from .service import horace_users, a_user, getby_username, find_course_detail_map, all_courses,lte_courses
from espy_contact.service import verify_password

router = APIRouter(prefix="/horace/users", tags=["horace-users"])


@router.post("/login")
async def login_old(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = getby_username(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user_dict['password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # If password is correct, generate a token or log the user in
    return {"message": "User authenticated successfully"}

@router.get("/users", response_model=UserCol, response_model_by_alias=False,response_description="Get a students")
async def read_item(db: AsyncIOMotorClient = Depends(get_db)):
    return await horace_users(db)


@router.get(
    "/user/{id}",
    response_description="Get a single student",
    response_model=UserResponse,
    response_model_by_alias=False,
)
async def show_student(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    """
    Get the record for a specific student, looked up by `id`.
    """
    return await a_user(id, db)

course_router = APIRouter(prefix="/horace/courses", tags=["horace-courses"])

@course_router.get("/byid/{course_id}")
async def get_course(course_id: str, db: AsyncIOMotorClient = Depends(get_db)) -> CurriculumMap:
    """Find courses by course ID."""
    return await find_course_detail_map(course_id, db)
@course_router.get("/coursesfull",response_model=List[CourseItem])
async def courses(db: AsyncIOMotorClient = Depends(get_db)):
    return await all_courses(db)
@course_router.get("/allcourses", response_model=List[CourseItem])
async def get_courses(db: AsyncIOMotorClient = Depends(get_db)):
    return await lte_courses(db)
