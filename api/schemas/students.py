from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentIn(BaseModel):
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    student_password: Optional[str] = None
    student_about: Optional[str] = "Hey there, let's learn together!"

    class Config:
        from_attributes = True

class StudentOut(BaseModel):
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    student_email: Optional[EmailStr] = None
    student_about: Optional[str] = "Hey there, let's learn together!"
    student_profile: Optional[str] = None

    class Config:
        from_attributes = True

class StudentEdit(BaseModel):
    student_name: Optional[str] = None
    student_email: Optional[EmailStr] = None

    class Config:
        from_attributes = True

class StudentSignin(BaseModel):
    student_email: Optional[EmailStr] = None
    student_password: Optional[str] = None

    class Config:
        from_attributes = True
