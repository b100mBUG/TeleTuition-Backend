from fastapi import APIRouter
from database.utils import raise_exception
from api.schemas.tutors import TutorOut, TutorIn, TutorEdit
from database.actions.tutors import (
    search_tutor, add_tutor, edit_tutor, delete_tutor, 
    verify_tutor_otp
)

router = APIRouter()


@router.get("/tutor-search/", response_model=list[TutorOut])
async def find_tutors(search_term: str | None):
    tutors = await search_tutor(search_term)
    if not tutors:
        raise_exception(404, "tutors not found")
    return tutors

@router.post("/tutors-add", response_model=TutorOut)
async def create_account(tut: TutorIn):
    tutor = await add_tutor(tut.model_dump())
    if not tutor:
        raise_exception(400, "Failed to add tutor account")
    
    return tutor

@router.put("/tutors-edit/", response_model=TutorOut)
async def refactor_tutor(tutor_id: str | None, tutor_detail: TutorEdit):
    tutor = await edit_tutor(tutor_id, tutor_detail.model_dump())
    if not tutor:
        raise_exception(400, "Failed to edit patient")
    
    return tutor

@router.put("/tutor-verify-otp/", response_model=TutorOut)
async def verify_otp(tutor_id: str | None, otp: str | None):
    tutor = await verify_tutor_otp(tutor_id, otp)
    if not tutor:
        raise_exception(404, "Failed to verify OTP")
    return tutor

@router.delete("/tutors-delete/")
async def remove_tutor(tutor_id: str | None):
    try:
        await delete_tutor(tutor_id)
    except Exception as e:
        raise_exception(500, e)