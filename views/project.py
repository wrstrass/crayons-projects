from fastapi import APIRouter, Depends

from views.dependencies import authenticate, authenticate_optional
from schemas import NameSchema, UserAndGroupSchema
from models import PermissionSet
from services import ProjectService


router = APIRouter(prefix="/projects")


@router.post("/")
async def new_project(name: NameSchema, user_id: int = Depends(authenticate)):
    return await ProjectService.new(name.name, user_id)

@router.get("/")
async def get_projects(user_id: int = Depends(authenticate)):
    return await ProjectService.get_all(user_id)

@router.get("/{project_name}/")
async def get_project(project_name: str, user_id: int = Depends(authenticate_optional)):
    return await ProjectService.get(project_name, user_id)

@router.get("/{diagram_oid}/access")
async def get_diagram_access(diagram_oid: str, user_id: int = Depends(authenticate_optional)):
    return await ProjectService.get_access(diagram_oid, user_id)

@router.put("/{project_name}/user")
async def project_add_user(project_name: str, data: UserAndGroupSchema, user_id: int = Depends(authenticate)):
    return await ProjectService.add_user(project_name, user_id, data.user, data.group)

@router.put("/{project_name}/permissions")
async def project_permissions(project_name: str, permissions: PermissionSet, user_id: int = Depends(authenticate)):
    return await ProjectService.set_permissions(project_name, user_id, permissions)

@router.put("/{project_name}/{diagram_oid}")
async def project_add_diagram(project_name: str, diagram_oid: str, user_id: int = Depends(authenticate)):
    return await ProjectService.add_diagram(project_name, user_id, diagram_oid)
