from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from siteseo.app.campus.app.info import service
from siteseo.app.campus.app.info.models import Appuser
from typing import List
from siteseo.app.campus.app.info.schema import (
    AppuserDto,
    SchoolDto,
    SchoolResponse,
    UserResponse,
    EnrollmentDto,
)
from espy_contact.util.enums import AccessRoleEnum
from sqlalchemy.orm import Session
from siteseo.app.db.session import get_db
from siteseo.app.campus.app.auth.oauth2 import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/info", tags=["user-mgmt"])



router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = service.get_userby_username(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not service.verify_password(form_data.password, user_dict['password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # If password is correct, generate a token or log the user in
    return {"message": "User authenticated successfully"}


@router.post("/user")
def add_user(user: AppuserDto, db: Session = Depends(get_db)):
    return service.add_user(user, db)


@router.get("/exists")
def user_exists(email: str, db: Session = Depends(get_db), user: Appuser = Depends(get_current_user)) -> bool:
    return service.is_exist(email, db)


@router.get("/all")
def get_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    return service.all_users(db)


@router.post("/enrol")
def student_enrol(enrol: EnrollmentDto, db: Session = Depends(get_db)) -> bool:
    try:
        return service.user_enrol_signup(enrol, db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("enrols")
def all_enrollments(db: Session = Depends(get_db)) -> List[EnrollmentDto]:
    """Only admin."""
    return service.all_enroll(db)


@router.get("/enrol")
def get_enrol(eid: str, db: Session = Depends(get_db)) -> EnrollmentDto:
    try:
        return service.one_enrol(eid, db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/byrole")
def get_by_role(
    role: AccessRoleEnum, db: Session = Depends(get_db)
) -> List[UserResponse]:
    """Get teacher admin staff students or any user by role."""
    return service.users_by_role(role=role, db=db)


@router.post("/school")
def add_school(schoolDto: SchoolDto, db: Session = Depends(get_db)) -> SchoolResponse:
    return service.add_school(schoolDto=schoolDto, db=db)


@router.put("/student/class")
def assign_student_class(sid: str, cid: str, db: Session = Depends(get_db)):
    return service.assign_student_to_class(sid, cid, db)


@router.post("/students/upload", status_code=status.HTTP_201_CREATED)
async def upload_students(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> int:
    """
    Uploads student data from a CSV or JSON file.

    Args:
        file (UploadFile): The uploaded file.
        db (Session): The database session object (dependency).

    Returns:
        StudentUploadResponse: Response object containing information about the upload.
    """
    try:
        if file.content_type not in ("text/csv", "application/json"):
            raise ValueError(
                "Invalid file type. Supported types: csv, json"
            )  # Raise a specific exception

        file_type = file.content_type.split("/")[1]
        return service.bulk_upload_students(file.filename, file_type, db)

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  # Appropriate status code for constraint violations
            detail={"message": "Error uploading students. Please check the data."},
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # Generic error handling
            detail={"message": "An unexpected error occurred."},
        ) from exc


@router.post("/users/upload", status_code=status.HTTP_201_CREATED)
async def upload_users(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads user data from a CSV or JSON file.

    Args:
        file (UploadFile): The uploaded file.
        db (Session): The database session object (dependency).

    Returns:
        int: The number of users successfully uploaded.
    """

    try:
        if file.content_type not in ("text/csv", "application/json"):
            return JSONResponse(
                content={"message": "Invalid file type. Supported types: csv, json"},
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        file_type = file.content_type.split("/")[1]
        uploaded_count = service.bulk_upload_users(file.filename, file_type, db)

        return JSONResponse(
            content={"message": f"{uploaded_count} users uploaded successfully."},
            status_code=status.HTTP_201_CREATED,
        )

    except IntegrityError as e:
        # Handle potential duplicate key errors
        print(f"Error uploading users: {e}")
        return JSONResponse(
            content={"message": "Error uploading users. Please check the data."},
            status_code=status.HTTP_409_CONFLICT,
        )

    except Exception as e:
        print(f"Unexpected error during upload: {e}")
        return JSONResponse(
            content={"message": "An unexpected error occurred."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/attendance", status_code=status.HTTP_201_CREATED)
async def mark_student_attendance(
    student_id: str,
    is_present: bool,
    remarks: str,
    created_by: str,
    db: Session = Depends(get_db),
):
    """
    Marks student attendance in a class.

    Args:
        student_id (str): The ID of the student.
        is_present (bool): True for present, False for absent.
        remarks (str, optional): Any additional remarks about the attendance.
        created_by (str, optional): Email of the teacher or student marking the attendance.
        db (Session): The database session object (dependency).

    Returns:
        JSONResponse: A JSON response containing information about the marked attendance.
    """

    try:
        attendance = service.mark_attendance(
            student_id, is_present, remarks, created_by, db
        )
        return JSONResponse(
            content={
                "message": "Attendance marked successfully.",
                "data": attendance.dict(),
            },
            status_code=status.HTTP_201_CREATED,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
