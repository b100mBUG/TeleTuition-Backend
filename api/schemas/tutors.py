from pydantic import BaseModel, EmailStr
from typing import Optional

class TutorIn(BaseModel):
    tutor_name: Optional[str] = None
    tutor_email: Optional[EmailStr] = None
    tutor_password: Optional[str] = None
    tutor_about = Optional[str] = "Hey there, Let's learn together!"

    class Config:
        from_attributes = True

class TutorOut(BaseModel):
    tutor_id: Optional[str] = None
    tutor_name: Optional[str] = None
    tutor_email: Optional[EmailStr] = None
    tutor_about = Optional[str] = "Hey there, Let's learn together!"
    tutor_profile = Optional[str]

    class Config:
        from_attributes = True

class TutorEdit(BaseModel):
    tutor_name: Optional[str] = None
    tutor_email: Optional[EmailStr] = None

    class Config:
        from_attributes = True

class TutorSignin(BaseModel):
    tutor_email: Optional[EmailStr]
    tutor_password: Optional[str]

    class Config:
        from_attributes = True
