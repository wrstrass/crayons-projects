from fastapi import APIRouter, Depends

from views.dependencies import authenticate, authenticate_optional
from schemas import NameSchema, ProjectSchema
from services import ProjectService


router = APIRouter(prefix="/projects")


@router.get("/{project_name}/")
async def get_project(project_name: str, user_id: int = Depends(authenticate_optional)):
    return await ProjectService.get(project_name, user_id)

@router.post("/")
async def new_project(name: NameSchema, user_id: int = Depends(authenticate)):
    return await ProjectService.new(name.name, user_id)
