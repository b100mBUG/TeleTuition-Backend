from database.models import Resource, Tutorial
from config import async_session
from sqlalchemy import select, exists
from database.utils import raise_exception
from database.utils import upload_video, compress_video
import asyncio
import uuid, shutil, os


async def add_resource(tutor_id: str | None, resource_details: dict | None, video_file):
    if not tutor_id:
        raise_exception(400, "Tutor ID required")
    
    if not resource_details:
        raise_exception(400, "Resource details required")
    
    tmp_input_path = f"/tmp/{uuid.uuid4()}_original.mp4"
    with open(tmp_input_path, "wb") as f:
        shutil.copyfileobj(video_file.file, f)

    tmp_output_path = f"/tmp/{uuid.uuid4()}_compressed.mp4"
    await asyncio.to_thread(compress_video, tmp_input_path, tmp_output_path)

    file_url = await asyncio.to_thread(upload_video, tmp_output_path)

    os.remove(tmp_input_path)

    async with async_session.begin() as session:
        new_resource = Resource(
            tutor_id=tutor_id,
            resource_title=resource_details.get("resource_title"),
            resource_subject=resource_details.get("resource_subject"),
            resource_about=resource_details.get("resource_about"),
            file_url=file_url
        )

        try:
            session.add(new_resource)
            await session.flush()
            return new_resource
        except Exception as e:
            raise_exception(500, f"An error occurred: \n {e}")

async def view_resource(student_id: str | None, resource_id: str | None):
    if not student_id:
        raise_exception(400, "Student ID is required")
    
    if not resource_id:
        raise_exception(400, "Resource ID is required")

    
    async with async_session.begin() as session:
        stmt = select(
            exists().where(
                Tutorial.student_id == student_id,
                Tutorial.resource_id == resource_id
            )
        )

        if (await session.execute(stmt)).scalar():
            raise_exception(400, "Resource already exists")

        new_tutorial = Tutorial(
            student_id = student_id,
            resource_id = resource_id
        )

        try:
            session.add(new_tutorial)
            await session.flush()
            return new_tutorial
        except Exception as e:
            raise_exception(500, f"An error occurred: \n {e}")
        return "Added resource"

async def fetch_library(student_id: str):
    async with async_session() as session:
        stmt = (
            select(Resource)
            .join(Tutorial, Tutorial.resource_id == Resource.resource_id)
            .where(Tutorial.student_id == student_id)
        )

        result = await session.execute(stmt)
        return result.scalars().all()



async def fetch_resources():
    async with async_session() as session:
        stmt = select(Resource)
        result = await session.execute(stmt)
        resources = result.scalars().all()
        if not resources:
            raise_exception(404, "Resources not found")
        
        return resources

async def search_resources(search_term: str | None):
    if not search_term:
        raise_exception(400, "Search term required")
    
    async with async_session() as session:
        stmt = select(Resource).where(
            Resource.resource_title.ilike(f"%{search_term}%")
        )
        result = await session.execute(stmt)
        resources = result.scalars().all()
        
        if not resources:
            raise_exception(404, "Resources not found")
        
        return resources

async def delete_resource(resource_id: str | None):
    if not resource_id: 
        raise_exception(400, "Resource ID required")
    
    async with async_session.begin() as session:
        stmt = select(Resource).where(
            Resource.resource_id == resource_id
        )
        result = await session.execute(stmt)

        resource = result.scalars().first()

        if not resource:
            raise_exception(404, "Resources not found")
        
        try:
            await session.delete(resource)
        except Exception as e:
            print("An error occurred when deleting resource: ", e)
            return