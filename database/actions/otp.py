from database.models import TutorEmailOTP, StudentEmailOTP
from config import async_session
from sqlalchemy import select

async def fetch_otp(target: str | None, user_id: str | None):
    if not target:
        return None
    if not user_id:
        return None
    
    async with async_session() as session:
        stmt = None
        if target == "student":
            stmt = select(StudentEmailOTP.otp_hash).where(
                StudentEmailOTP.student_id == user_id
            )
        elif target == "tutor":
            stmt = select(TutorEmailOTP.otp_hash).where(
                TutorEmailOTP.tutor_id == user_id
            )
        
        result = await session.execute(stmt)
        otp = result.scalars().first()

        if not otp:
            return None




