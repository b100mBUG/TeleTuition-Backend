from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String,
    DateTime, Float, Text, 
    ForeignKey, Time, Date, Boolean, func
)
from uuid import uuid4
from datetime import datetime, timedelta, timezone

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True, default= lambda: str(uuid4()), index=True)
    student_name = Column(String, index=True)
    student_email = Column(String, index=True, unique=True)
    email_verified = Column(Boolean, default=False)
    student_password = Column(String)
    student_profile = Column(String, nullable=True)
    student_about = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    tutorials = relationship("Tutorial", back_populates="student", cascade="all, delete-orphan")


class Tutor(Base):
    __tablename__ = "tutors"
    tutor_id = Column(String, primary_key=True, default= lambda: str(uuid4()), index=True)
    tutor_name = Column(String, index=True)
    tutor_email = Column(String, index=True, unique=True)
    email_verified = Column(Boolean, default=False)
    tutor_password = Column(String)
    tutor_rating = Column(Float, default=0)
    tutor_amount = Column(Float, default=0)
    tutor_profile = Column(String, nullable=True)
    tutor_about = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    resources = relationship("Resource", back_populates="tutor", cascade="all, delete-orphan")

class Resource(Base):
    __tablename__ = "resources"
    resource_id = Column(String, primary_key=True, default= lambda: str(uuid4()), index=True)
    tutor_id = Column(String, ForeignKey("tutors.tutor_id"), index=True)

    resource_title = Column(String, index=True)
    resource_subject = Column(String, index=True)
    resource_about = Column(Text, index=True)
    file_url = Column(String)
    resource_price = Column(Float, default=50.0)
    created_at = Column(DateTime, default=func.now())

    tutor = relationship("Tutor", back_populates="resources")
    tutorials = relationship("Tutorial", back_populates="resource")



class Tutorial(Base):
    __tablename__ = "tutorials"
    tutorial_id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    student_id = Column(String, ForeignKey("students.student_id"), index=True)
    resource_id = Column(String, ForeignKey("resources.resource_id"), index=True)

    created_at = Column(DateTime, default=func.now())

    student = relationship("Student", back_populates="tutorials")
    resource = relationship("Resource", back_populates="tutorials")

class StudentEmailOTP(Base):
    __tablename__ = "student_email_otps"

    otp_id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    student_id = Column(String, ForeignKey("students.student_id"), index=True)

    otp_hash = Column(String, nullable=False)

    expires_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5)
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


class TutorEmailOTP(Base):
    __tablename__ = "tutor_email_otps"

    otp_id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    tutor_id = Column(String, ForeignKey("tutors.tutor_id"), index=True)

    otp_hash = Column(String, nullable=False)

    expires_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5)
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
