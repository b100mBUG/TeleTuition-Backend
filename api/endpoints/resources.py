from fastapi import APIRouter, UploadFile, File, Form
from database.utils import raise_exception
from api.schemas.resources import ResourceIn, ResourceOut
from database.actions.resources import (
    fetch_resources, search_resources, add_resource, 
    delete_resource
)

router = APIRouter()

@router.get("/resources-fetch/", response_model=list[ResourceOut])
async def show_resources():
    resources = await fetch_resources()
    if not resources:
        raise_exception(404, "Resources not found")
    return resources

@router.get("/resources-search/", response_model=list[ResourceOut])
async def find_resources(search_term: str | None):
    resources = await search_resources(search_term)

    if not resources:
        raise_exception(404, "Resources not found")
    return resources

@router.post("/resources-add/", response_model=ResourceOut)
async def new_resource(
    tutor_id: str = Form(...),
    resource_title: str = Form(...),
    resource_subject: str = Form(...),
    resource_about: str = Form(...),
    video_file: UploadFile = File(...)
):
    resource_details = {
        "resource_title": resource_title,
        "resource_subject": resource_subject,
        "resource_about": resource_about
    }

    resource = await add_resource(tutor_id, resource_details, video_file)
    
    if not resource:
        raise_exception(400, "Failed to add resource")
    
    return resource

@router.delete("/resources-delete/")
async def remove_resource(resource_id: str | None):
    try:
        await delete_resource(resource_id)
        return "Resource deleted successfuly"
    except Exception as e:
        raise_exception(500, "An error occurred while deleting resource")