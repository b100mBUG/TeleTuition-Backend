from pydantic import BaseModel
from typing import Optional


class ResourceIn(BaseModel):
    resource_title: Optional[str] = None
    resource_subject: Optional[str] = None
    resource_about: Optional[str] = None

    class Config:
        from_attributes = True

class ResourceOut(BaseModel):
    resource_id: Optional[str] = None
    tutor_id: Optional[str] = None
    resource_title: Optional[str] = None
    resource_subject: Optional[str] = None
    resource_about: Optional[str] = None
    file_url: Optional[str] = None

    class Config:
        from_attributes = True
