from database.models import Student, StudentEmailOTP
from config import async_session
from database.utils import hash_pwd, is_verified_pwd, is_verified_otp, generate_otp, hash_otp, send_otp_email
from sqlalchemy import select
from database.utils import raise_exception
from database.actions.otp import fetch_otp
from datetime import datetime, timezone


async def add_student(student_details: dict | None):
    if not student_details:
        raise_exception(400, "Student ID is required")

    async with async_session.begin() as session:
        new_student = Student(
            student_name=student_details.get("student_name"),
            student_email=student_details.get("student_email"),
            student_password=hash_pwd(student_details.get("student_password", "@student_test"))
        )
        try:
            session.add(new_student)
            await session.flush()
            otp = generate_otp()
            new_otp = StudentEmailOTP(
                student_id = new_student.student_id,
                otp_hash = hash_otp(otp)
            )
            session.add(new_otp)
            
        except Exception as e:
            print(f"Error adding student: {e}")
            raise_exception(500, f"An error occurred: \n{e}")
    send_otp_email(new_student.student_email, otp)
    return new_student

async def resend_otp(student_email: str):
    async with async_session.begin() as session:
        stmt = select(Student).where(Student.student_email == student_email)
        result = await session.execute(stmt)
        student = result.scalars().first()
        if not student:
            return None

        otp_stmt = select(StudentEmailOTP).where(StudentEmailOTP.student_id == student.student_id)
        otp_res = await session.execute(otp_stmt)
        existing_otp = otp_res.scalars().first()
        if existing_otp:
            await session.delete(existing_otp)
        try:
            otp = generate_otp()
            new_otp = StudentEmailOTP(
                student_id=student.student_id,
                otp_hash=hash_otp(otp),
            )
            session.add(new_otp)
            await session.commit()

            send_otp_email(student_email, otp)
            return new_otp
        except Exception as e:
            return None
        

async def fetch_student(student_id: str | None):
    if not student_id:
        raise_exception(400, "Student ID is required")

    async with async_session() as session:
        stmt = select(Student).where(Student.student_id == student_id)
        result = await session.execute(stmt)
        student = result.scalars().first()
        if not student:
            raise_exception(404, "Student not found")
        
        return student
    
async def search_student(search_term: str | None):
    if not search_term:
        raise_exception(400, "Search tem required")
    
    async with async_session() as session:
        stmt = select(Student).where(
            Student.student_name.ilike(f"%{search_term}%")
        )

        result = await session.execute(stmt)
        students = result.scalars().all()

        if not students:
            raise_exception(404, "Students not found")
        return students

async def edit_student(student_id: str | None, student_details: dict | None):
    if not student_id:
        raise_exception(400, "Student ID is required")
    if not student_details: 
        raise_exception(400, "Student details are required")
    
    async with async_session.begin() as session:
        student = await fetch_student(student_id)
        if not student:
            raise_exception(404, "Student not found")
        
        student = await session.merge(student)
        
        student.student_name = student_details.get("student_name")
        student.student_email = student_details.get("student_email")

        return student

async def signin_student(student_details: dict | None):
    if not student_details:
        raise_exception(400, "Student credentials required")

    email = student_details.get("student_email")
    password = student_details.get("student_password")

    if not email or not password:
        raise_exception(400, "Email and password required")

    async with async_session() as session:
        stmt = select(Student).where(Student.student_email == email)
        result = await session.execute(stmt)
        student = result.scalars().first()

        if not student or not is_verified_pwd(password, student.student_password):
            raise_exception(401, "Invalid email or password")

        return student


async def verify_student_otp(student_email: str | None, otp: str | None):
    if not student_email:
        raise_exception(400, "student email required")
    if not otp:
        raise_exception(400, "OTP required")

    async with async_session() as session:
        result = await session.execute(select(Student).where(Student.student_email == student_email))
        student = result.scalars().first()
        if not student:
            raise_exception(404, "Student not found")

        result = await session.execute(select(StudentEmailOTP).where(StudentEmailOTP.student_id == student.student_id))
        hashed_otp = result.scalars().first()
        if not hashed_otp:
            raise_exception(404, "OTP not found")

        if hashed_otp.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
            raise_exception(400, "OTP expired!")

        if not is_verified_otp(otp, hashed_otp.otp_hash):
            raise_exception(404, "Failed to verify OTP")

        student.email_verified = True

        await session.commit()

        return student

async def delete_student(student_id: str | None):
    if not student_id:
        raise_exception(400, "Student ID is required")

    async with async_session.begin() as session:
        student = await fetch_student(student_id)
        if not student:
            raise_exception(404, "Student not found")
        
        student = await session.merge(student)
        
        await session.delete(student)

        return "Deleted successfully"
        


