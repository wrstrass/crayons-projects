from models import ProjectModel
from repository import ProjectRepository


class ProjectService:
    @staticmethod
    async def new(name: str, owner: int) -> ProjectModel:
        return await ProjectRepository.new(ProjectModel(
            name=name,
            members={
                "owners": [owner,],
            },
        ))
