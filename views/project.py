from fastapi import APIRouter, Depends

from views.dependencies import authenticate, authenticate_optional
from schemas import NameSchema, UserAndGroupSchema
from services import ProjectService


router = APIRouter(prefix="/projects")


@router.post("/")
async def new_project(name: NameSchema, user_id: int = Depends(authenticate)):
    return await ProjectService.new(name.name, user_id)

@router.get("/{project_name}/")
async def get_project(project_name: str, user_id: int = Depends(authenticate_optional)):
    return await ProjectService.get(project_name, user_id)

@router.put("/{project_name}/")
async def project_add_user(project_name: str, data: UserAndGroupSchema, user_id: int = Depends(authenticate)):
    return await ProjectService.add_user(project_name, user_id, data.user, data.group)
