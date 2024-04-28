from siteseo.app.db.base import Base
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum
from siteseo.app.campus.app.classroom.models import Classroom
from espy_contact.util.enums import AccessRoleEnum, StatusEnum, GradeLevel, Term


# class ReachBase:
#     id = Column(String, primary_key=True, index=True)
#     timestamp = Column(DateTime(), server_default=func.now())
# address_associations = Table(
#     "address_associations", Base.metadata,
#     Column("id", String, primary_key=True, index=True),
#     Column("school_id", String, ForeignKey("schools.id")),
#     Column("user_id", String, ForeignKey("appusers.id")),
#     Column("address_id", String, ForeignKey("addresses.id")),
# )
class Address(Base):
    __tablename__ = "addresses"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    email = Column(String)
    phone_number = Column(String)
    country = Column(String)


class Appuser(Base):
    __tablename__ = "appusers"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    first_name = Column(String)
    last_name = Column(String)
    country = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    token = Column(String)
    dp = Column(String)
    is_active = Column(Boolean)
    roles = Column(ARRAY(Enum(AccessRoleEnum)))
    status = Column(Enum(StatusEnum))
    address_id = Column(
        String, ForeignKey("addresses.id"), nullable=True
    )  # Add foreign key
    address = relationship(
        "Address", uselist=False, backref="user"
    )  # One-to-one relationship


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dob = Column(Date)
    gender = Column(String)
    nationality = Column(String)
    user_id = Column(String, ForeignKey("appusers.id"))
    user = relationship("Appuser", foreign_keys=[user_id])
    parent_email = Column(String)
    current_school = Column(String)
    current_class = Column(String)
    achievements = Column(String)
    extracurricular = Column(String)
    parent_phone = Column(String)
    parent_name = Column(String)
    parent_occupation = Column(String)
    religion = Column(String)
    grade_level = Column(Enum(GradeLevel))
    term = Column(Enum(Term))
    academic_year = Column(Integer)
    remarks = Column(String)
    photo = Column(String)
    birth_certificate = Column(String)
    signature = Column(String)
    is_paid = Column(Boolean)


class School(Base):
    __tablename__ = "schools"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    owner_id = Column(String, ForeignKey("appusers.id"))
    timestamp = Column(DateTime(), server_default=func.now())
    address_id = Column(
        String, ForeignKey("addresses.id"), nullable=True
    )  # Add foreign key
    address = relationship(
        "Address", uselist=False, backref="school"
    )  # One-to-one relationship


class Student(Base):
    __tablename__ = "student"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    biodata_id = Column(
        String, ForeignKey("appusers.id")
    )  # Define ForeignKey for relationship
    biodata = relationship("Appuser")  # Define relationship
    date_of_birth = Column(String)
    id_card = Column(String)
    class_id = Column(String, ForeignKey("classrooms.id"))
    classroom = relationship("Classroom", foreign_keys=[class_id])


class Student_attendance(Base):
    __tablename__ = "attendance"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    student_id = Column(String, ForeignKey("student.id"))
    is_present = Column(Boolean, default=False)
    remarks = Column(String)
    created_by = Column(String)  # email of the teacher who makrked the attendance


class EnrollmentRequest(Base):
    __tablename__ = "enrollment"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    student_id = Column(
        String, ForeignKey("student.id")
    )  # Define ForeignKey for relationship
    student_profile = relationship("Student")
    grade_level = Column(String)
    academic_year = Column(Integer)
    remarks = Column(String)


class AcademicHistory(Base):
    """Student or teacher can have multiple AcademicHistory."""

    __tablename__ = "academic_history"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(), server_default=func.now())
    school_name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(String)
    grade_level = Column(String)
    reason_for_leaving = Column(String)
    classroom = Column(String)
    owner_id = Column(String, ForeignKey("appusers.id"))
    owner = relationship("Appuser", backref="academic_history")


# Additional model for assignment relationship (optional):
# class Class_Teacher(Base):
#     __tablename__ = "class_teacher"
#     id = Column(String, primary_key=True, index=True)
#     timestamp = Column(DateTime(), server_default=func.now())
#     classroom_id= Column(Integer, ForeignKey("classrooms.id"))  # ForeignKey to Classroom
#     teacher= Column(Integer, ForeignKey("appuser.id"))  # ForeignKey to Teacher
