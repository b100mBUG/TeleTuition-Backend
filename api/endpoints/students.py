from fastapi import APIRouter
from database.utils import raise_exception
from api.schemas.students import StudentOut, StudentIn, StudentEdit, StudentSignin
from database.actions.students import (
    search_student, add_student, edit_student, delete_student,
    verify_student_otp, signin_student, resend_otp
)
from database.utils import generate_otp, send_otp_email

router = APIRouter()


@router.get("/student-search/", response_model=list[StudentOut])
async def find_students(search_term: str | None):
    students = await search_student(search_term)
    if not students:
        raise_exception(404, "Students not found")
    return students

@router.post("/students-add", response_model=StudentOut)
async def create_account(stdt: StudentIn):
    student = await add_student(stdt.model_dump())
    if not student:
        raise_exception(400, "Failed to add student account")
    
    return student

@router.post("/students-signin/", response_model=StudentOut)
async def student_signin(stdt: StudentSignin):
    student = await signin_student(stdt.model_dump())

    if not student:
        raise_exception(404, "Student not found")
    return student

@router.post("/student-otp-resend/")
async def start_resend_otp(student_email: str):
    otp = await resend_otp(student_email)
    if not otp:
        raise_exception(400, "Failed to resend OTP")
    return {"OTP resent"}

@router.put("/students-edit/", response_model=StudentOut)
async def refactor_student(student_id: str | None, student_detail: StudentEdit):
    student = await edit_student(student_id, student_detail.model_dump())
    if not student:
        raise_exception(400, "Failed to edit patient")
    
    return student
    
@router.put("/student-verify-otp/", response_model=StudentOut)
async def verify_otp(student_email: str | None, otp: str | None):
    student = await verify_student_otp(student_email, otp)
    if not student:
        raise_exception(404, "Failed to verify OTP")
    return student

@router.delete("/students-delete/")
async def remove_student(student_id: str | None):
    try:
        await delete_student(student_id)
        return "Deleted successfully"
    except Exception as e:
        raise_exception(500, e)