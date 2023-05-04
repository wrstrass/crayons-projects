from fastapi import APIRouter
from views import project
from config import PREFIX


router = APIRouter(prefix=PREFIX)

router.include_router(project.router)
