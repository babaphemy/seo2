from siteseo.app.db.session import get_db
import csv
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, exc
from espy_contact.util.enums import AccessRoleEnum
from siteseo.app.campus.app.info.models import (
    Appuser,
    School,
    Address,
    Enrollment,
    Student,
    Student_attendance,
)
from . import validator
from siteseo.app.campus.app.classroom.models import Classroom
from siteseo.app.campus.app.info.schema import (
    AppuserDto,
    SchoolResponse,
    SchoolDto,
    AddressDto,
    UserResponse,
    EnrollmentDto,
)
from espy_contact import service
from typing import List
from siteseo.app.campus.app.util import converter
import uuid
import os


def make_file(file, save_location="local"):
    """Saves a file to a local directory or uploads it to AWS S3.

    Args:
        file: A file-like object containing the file data.
        save_location: (Optional) String specifying the save location ("local" or "s3"). Defaults to "local".

    Returns:
        A string representing the saved file path (local) or S3 object key (S3).
    """

    if not file:
        raise ValueError("No file provided")

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"

    if save_location == "local":
        # Save to local directory (replace 'your_local_dir' with your desired path)
        save_path = os.path.join("your_local_dir", filename)
        with open(save_path, "wb") as f:
            f.write(file.read())
        return save_path

    elif save_location == "s3":
        # Upload to AWS S3 (replace placeholders with your S3 configuration)
        import boto3

        s3_client = boto3.client(
            "s3",
            aws_access_key_id="your_access_key_id",
            aws_secret_access_key="your_secret_access_key",
        )
        s3_client.upload_fileobj(file, "your-bucket-name", filename)
        return filename  # Return the S3 object key

    else:
        raise ValueError(f"Invalid save location: {save_location}")


def user_enrol_signup(user: EnrollmentDto, db: Session) -> bool:
    try:
        user_enrolled = db.query(Appuser).filter(Appuser.email == user.email).first()
        if user_enrolled:
            raise ValueError(f"The email {user.email} already enrolled ")
        address = Address(
            street=user.address.street,
            city=user.address.city,
            state=user.address.state,
            zip_code=user.address.zip_code,
            email=user.address.email,
            phone_number=user.address.phone_number,
            country=user.address.country,
        )
        new_user = Appuser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            roles=[role for role in user.role],
            timestamp=user.timestamp,
            address=address,
        )
        new_enrol = Enrollment(
            user=new_user,
            dob=user.dob,
            gender=user.gender,
            nationality=user.nationality,
            parent_email=user.parent_email,
            current_school=user.current_school,
            current_class=user.current_class,
            achievements=user.achievements,
            extracurricular=user.extracurricular,
            parent_phone=user.parent_phone,
            parent_name=user.parent_email,
            parent_occupation=user.parent_occupation,
            religion=user.religion,
            photo=make_file(user.photo) if user.photo else None,
            birth_certificate=make_file(user.birth_certificate)
            if user.birth_certificate
            else None,
            signature=user.signature,
        )
        db.add(new_enrol)
        db.commit()
        db.refresh(new_enrol)
        return True
    except Exception as e:
        raise e


def all_enroll(db: Session) -> List[EnrollmentDto]:
    enrols = db.query(Enrollment).all()
    return [converter.to_enrollment(e) for e in enrols]


def one_enrol(eid: str, db: Session) -> EnrollmentDto:
    try:
        enrol = db.query(Enrollment).options(joinedload(Enrollment.user)).get(eid)
        if not enrol:
            raise ValueError(f"No enrollment with ID {eid}")
        return converter.to_enrollment(enrol)

    except Exception as e:
        raise e


def add_user(user: AppuserDto, db: Session) -> Appuser:
    addr: Address = create_address(user.address, db)
    new_user = Appuser(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=service.encrypt_pass(user.password),
        is_active=user.is_active,
        roles=[role for role in user.role],
        timestamp=user.timestamp,
        address_id=addr.id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def bulk_upload_users(file_path: str, file_type: str, db: Session) -> int:
    """
    Uploads user data from a CSV or JSON file.

    Args:
        file_path (str): The path to the CSV or JSON file.
        file_type (str): "csv" or "json".
        db (Session): The database session object.

    Returns:
        int: The number of users successfully uploaded.
    """

    uploaded_count = 0
    with open(file_path, "r") as file:
        if file_type == "csv":
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    user_dto = AppuserDto(**row)  # Convert row to AppuserDto
                    uploaded_count += 1
                    add_user(user_dto, db)
                except Exception as e:  # Catch general exceptions for data processing
                    print(f"Error processing user data (row {reader.line_no}): {e}")

        elif file_type == "json":
            data = json.load(file)
            for user_data in data:
                try:
                    user_dto = AppuserDto(**user_data)  # Convert data to AppuserDto
                    uploaded_count += 1
                    add_user(user_dto, db)
                except Exception as e:  # Catch general exceptions for data processing
                    print(
                        f"Error processing user data (index {data.index(user_data)}): {e}"
                    )
        else:
            raise ValueError("Invalid file type. Supported types: csv, json")

    return uploaded_count


def delete_user(uid: str, db: Session) -> bool:
    user = db.query(Appuser).get(uid)
    db.delete(user)
    db.commit()
    return True


def update_user(user: AppuserDto, db: Session) -> bool:
    user = db.query(Appuser).get(user.id)
    user.update({Appuser.email: user.email})

    db.commit()
    return True


def assign_student_to_class(student_id: str, class_id: str, db: Session) -> bool:
    """Assigns a student to a class and handles potential errors.

    Args:
        student_id: The ID of the student to assign.
        class_id: The ID of the class to assign the student to.
        db: The database session object.

    Returns:
        bool: True if successful, False otherwise.
    """

    try:
        student = db.query(Student).get(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")

        classroom = db.query(Classroom).get(class_id)
        if not classroom:
            raise ValueError(f"Classroom with ID {class_id} not found")

        student.classroom = classroom

        db.commit()

        return True

    except (ValueError, exc.IntegrityError) as e:
        print(f"Error assigning student: {e}")
        return False  # Return False on errors


def get_user(id: int) -> Appuser:
    db = get_db()
    user = db.query(Appuser).filter(Appuser.id == id).first()
    return user

def get_userby_username(email: str,db) -> Appuser:
    user = db.query(Appuser).filter(Appuser.email == email).first()
    return user


def all_users(db) -> List[UserResponse]:
    users = db.query(Appuser).all()
    users_resp = [
        UserResponse(
            id=user.id,
            timestamp=user.timestamp,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            role=user.roles,
        )
        for user in users
    ]
    return users_resp


def users_by_role(db: Session, role: AccessRoleEnum) -> List[UserResponse]:
    """
    Retrieve users based on their role.

    Args:
        db (Session): Database session.
        role (str): Role to filter users.

    Returns:
        List[UserResponse]: List of users matching the specified role.
    """
    users = db.query(Appuser).filter(Appuser.roles.contains([role])).all()
    users_resp = [
        UserResponse(
            id=user.id,
            timestamp=user.timestamp,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            role=user.roles,
        )
        for user in users
    ]
    return users_resp


def is_exist(email: str, db: Session) -> bool:
    user = db.query(Appuser).filter(Appuser.email == email).first()
    return bool(user)


def create_address(address: AddressDto, db: Session) -> bool:
    new_addr = Address(
        street=address.street,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
        email=address.email,
        phone_number=address.phone_number,
        country=address.country,
    )
    db.add(new_addr)
    db.commit()
    db.refresh(new_addr)
    address.id = new_addr.id
    return address


def add_school(schoolDto: SchoolDto, db: Session) -> SchoolResponse:
    addr: Address = create_address(schoolDto.address, db)
    new_school = School(
        owner_id=schoolDto.owner, name=schoolDto.name, address_id=addr.id
    )
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return SchoolResponse(
        id=new_school.id,
        address_id=new_school.address_id,
        owner_id=new_school.owner_id,
        name=new_school.name,
        create_at=new_school.timestamp,
    )


def bulk_upload_students(file_path: str, file_type: str, db: Session) -> int:
    """
    Uploads student data from a spreadsheet (CSV) or JSON file.

    Args:
        file_path (str): The path to the CSV or JSON file.
        file_type (str): "csv" or "json".
        db (Session): The database session object.

    Returns:
        int: The number of students successfully uploaded.

    Raises:
        ValueError: If an invalid file type is provided.
        Exception: If an unexpected error occurs during file handling or database operations.
    """

    try:
        uploaded_count = 0
        with open(file_path, "r") as file:
            if file_type == "csv":
                reader = csv.DictReader(file)
                for row in reader:
                    if validator.validate_student_data(row):
                        try:
                            student = Student(**row)
                            db.add(student)
                            db.commit()
                            uploaded_count += 1
                        except IntegrityError as e:
                            print(
                                f"Error uploading student: {e}"
                            )  # Log or handle duplicate key errors
            elif file_type == "json":
                data = json.load(file)
                for student_data in data:
                    if validator.validate_student_data(student_data):
                        try:
                            student = Student(**student_data)
                            db.add(student)
                            db.commit()
                            uploaded_count += 1
                        except IntegrityError as e:
                            print(
                                f"Error uploading student: {e}"
                            )  # Log or handle duplicate key errors
            else:
                raise ValueError("Invalid file type. Supported types: csv, json")
        return uploaded_count

    except Exception as e:
        raise Exception(f"An error occurred during bulk student upload: {e}") from e


def mark_attendance(
    student_id: str,
    is_present: bool,
    remarks: str = None,
    created_by: str = None,
    db: Session = get_db,
):
    """
    Marks student attendance in a class.

    Args:
        student_id (str): The ID of the student.
        is_present (bool): True for present, False for absent.
        remarks (str, optional): Any additional remarks about the attendance.
        created_by (str, optional): Email of the teacher or student marking the attendance.
        db (Session, optional): The database session object. If not provided, a new session will be created.

    Returns:
        Student_attendance: The created attendance record.
    """

    try:
        attendance = Student_attendance(
            student_id=student_id,
            is_present=is_present,
            remarks=remarks,
            created_by=created_by,
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)  # Refresh to get updated attributes
        return attendance
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error marking attendance: {e}") from e
    finally:
        if not db.is_active:  # Close session if not provided
            db.close()
