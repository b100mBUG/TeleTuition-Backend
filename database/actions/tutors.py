from database.models import Tutor, TutorEmailOTP
from config import async_session
from database.utils import hash_pwd, is_verified_pwd
from sqlalchemy import select
from database.utils import raise_exception
from database.utils import generate_otp, hash_otp, send_otp_email, is_verified_otp
from datetime import datetime, timezone


async def add_tutor(tutor_details: dict | None):
    if not tutor_details:
        raise_exception(400, "Tutor details required")
    async with async_session.begin() as session:
        new_tutor = Tutor(
            tutor_name = tutor_details.get("tutor_name"),
            tutor_email = tutor_details.get("tutor_email"),
            tutor_password = hash_pwd(tutor_details.get("tutor_password"))
        )

        try:
            session.add(new_tutor)
            await session.flush()
            otp = generate_otp()
            new_otp = TutorEmailOTP(
                tutor_id = new_tutor.tutor_id,
                otp_hash = hash_otp(otp)
            )
            session.add(new_otp)
            send_otp_email(new_tutor.tutor_email, otp)
            return new_tutor

        except Exception as e:
            raise_exception(500, f"An error occurred: \n {e}")

async def fetch_tutor(tutor_id: str | None):
    if not tutor_id:
        raise_exception(400, "Tutor ID required")

    async with async_session() as session:
        stmt = select(Tutor).where(
            Tutor.tutor_id == tutor_id
        )
        result = await session.execute(stmt)
        tutor = result.scalars().first()
        if not tutor:
            raise_exception(404, "Tutor not found")
        return tutor

async def search_tutor(search_term: str | None):
    if not search_term:
        raise_exception(400, "Search term required")
    
    async with async_session() as session:
        stmt = select(Tutor).where(
            Tutor.tutor_name.ilike(f"%{search_term}%")
        )
        result = await session.execute(stmt)
        tutors = result.scalars().all()

        if not tutors:
            raise_exception(404, "Tutors not found")
        
        return tutors

async def edit_tutor(tutor_id: str | None, tutor_details: str | None):
    if not tutor_id:
        raise_exception(400, "Tutor ID required")
    
    if not tutor_details:
        raise_exception(400, "Tutor details required")
    
    async with async_session.begin() as session:
        tutor = await fetch_tutor(tutor_id)
        if not tutor:
            raise_exception(404, "Tutor not found")
        
        tutor = await session.merge(tutor)
        
        try:
            tutor.tutor_name = tutor_details.get("tutor_name")
            tutor.tutor_email = tutor_details.get("tutor_email")

            return tutor

        except Exception as e:
            return None

async def signin_tutor(tutor_details: dict | None):
    if not tutor_details:
        raise_exception(400, "Tutor details required")
    async with async_session.begin() as session:
        stmt = select(tutor).where(
            tutor.tutor_email == tutor_details.get("tutor_email")
        )
        result = await session.execute(stmt)
        tutor = result.scalars().first()
        
        if not tutor:
            raise_exception(404, "Tutors not found")
        
        if not is_verified_pwd(tutor.tutor_password, tutor_details.get("tutor_password")):
            raise_exception(404, "Failed to sign in tutor")
        
        return tutor

async def verify_tutor_otp(tutor_id: str | None, otp: str | None):
    if not tutor_id:
        raise_exception(400, "Tutor ID required")
    if not otp:
        raise_exception(400, "OTP required")

    async with async_session() as session:
        result = await session.execute(select(Tutor).where(Tutor.tutor_id == tutor_id))
        tutor = result.scalars().first()
        if not tutor:
            raise_exception(404, "Tutor not found")

        result = await session.execute(select(TutorEmailOTP).where(TutorEmailOTP.tutor_id == tutor_id))
        hashed_otp = result.scalars().first()
        if not hashed_otp:
            raise_exception(404, "OTP not found")

        if hashed_otp.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
            raise_exception(400, "OTP expired!")

        if not is_verified_otp(otp, hashed_otp.otp_hash):
            raise_exception(404, "Failed to verify OTP")

        tutor.email_verified = True

        await session.commit()

        return tutor

async def delete_tutor(tutor_id: str | None):
    async with async_session.begin() as session:
        tutor = await fetch_tutor(tutor_id)
        await session.merge(tutor)
        if not tutor:
            raise_exception(404, "Tutor not found")
        
        await session.delete(tutor)

        return "Deleted successfully"