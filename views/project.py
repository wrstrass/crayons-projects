from fastapi import APIRouter, Depends

from views.dependencies import authenticate
from schemas import NameSchema
from services import ProjectService


router = APIRouter(prefix="/projects")

@router.post("/")
async def new_project(name: NameSchema, user_id: int = Depends(authenticate)):
    return await ProjectService.new(name.name, user_id)
