from siteseo.app.db.base import Base
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from espy_contact.util.enums import StatusEnum
from datetime import datetime
from sqlalchemy import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Text, Date, Float
from sqlalchemy.orm import relationship


class Tranx(Base):
    __tablename__ = "tranx"

    ref = Column(String, primary_key=True)
    stripeId = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    payee_id = Column(String, ForeignKey("appusers.id"))
    detail = Column(Text)  # Text allows for larger details if needed
    createdOn = Column(DateTime, default=datetime)
    modifiedOn = Column(DateTime, onupdate=datetime)

    payee = relationship("Appuser", backref="transactions")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    bank = Column(String, nullable=False)  # Assuming NigerianBank is a string enum
    account_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    account_officer = Column(String)
    account_admin = Column(String)
    created_on = Column(DateTime, default=datetime)
    modified_on = Column(DateTime, onupdate=datetime)


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True)
    classroom_id = Column(String, ForeignKey("classrooms.id"))
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    status = Column(Enum(StatusEnum))

    classroom = relationship("Classroom")
