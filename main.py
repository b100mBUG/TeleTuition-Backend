from fastapi import FastAPI
from api.endpoints.students import router as students_router
from api.endpoints.resources import router as resources_router
from api.endpoints.tutors import router as tutors_router

from dotenv import load_dotenv

load_dotenv("config.env")

app = FastAPI()

app.include_router(resources_router, prefix="/resources", tags=["resources"])
app.include_router(students_router, prefix="/students", tags=["students"])
app.include_router(tutors_router, prefix="/tutors", tags=["tutors"])
