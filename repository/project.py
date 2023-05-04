from models import ProjectModel
from db import projects_collection

class ProjectRepository:
    @staticmethod
    async def new(project: ProjectModel):
        await projects_collection.insert_one(project.dict())
        return project
