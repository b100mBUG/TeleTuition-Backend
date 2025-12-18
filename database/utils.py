from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
import random
import smtplib
from email.message import EmailMessage
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import ffmpeg

from dotenv import load_dotenv

load_dotenv("config.env")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")


def hash_pwd(password):
    return pwd_context.hash(password)

def is_verified_pwd(hashed_pwd, inputted_pwd):
    return pwd_context.verify(hashed_pwd, inputted_pwd)

def raise_exception(status_code: int | None, text: str | None):
    raise HTTPException(status_code=status_code, detail=text)


def hash_otp(otp: str) -> str:
    return pwd_context.hash(otp)

def is_verified_otp(inputted_otp: str, hashed_otp: str) -> bool:
    return pwd_context.verify(inputted_otp, hashed_otp)



def generate_otp():
    otp = ""

    for _ in range(6):
        otp += str(random.randint(0, 9))

    return otp

def send_otp_email(to_mail, otp):
    import smtplib
    from email.message import EmailMessage
    import os

    msg = EmailMessage()
    msg['Subject'] = "Verification One Time Password"
    msg['From'] = f"TeleTuition <{os.getenv('EMAIL_CLIENT')}>"
    msg['To'] = to_mail
    msg.set_content(f"Your OTP is {otp}\nDo not share this with anyone else.")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_CLIENT"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        print("OTP sent.")
    except Exception as e:
        print("An error occurred sending OTP:", e)


def compress_video(input_path, output_path, target_bitrate="700k", audio_bitrate="96k", preset="medium"):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec="libx264",
                video_bitrate=target_bitrate,
                acodec="aac",
                audio_bitrate=audio_bitrate,
                preset=preset,
                r=24  # FPS
            )
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"Compression complete: {output_path}")
    except ffmpeg.Error as e:
        raise RuntimeError(f"Compression failed: {e.stderr.decode()}") from e



cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure = True
)

def upload_video(file_path: str) -> str:
    result = cloudinary.uploader.upload(
        file_path,
        resource_type="video",
        folder="tutorials",
        format="mp4",
        eager=[
            {"format": "m3u8", "streaming_profile": "hd"}
        ],
        eager_async=True
    )

    return result["secure_url"]

def upload_picture(file_path: str) -> str:
    result = cloudinary.uploader.upload(file_path, folder="profiles/")
    return result["secure_url"]


