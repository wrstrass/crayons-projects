from models import ProjectModel


class ProjectService:
    @staticmethod
    async def new(name: str, owner: int) -> ProjectModel:
        return await ProjectModel(
            name=name,
            members={
                "owners": [owner,],
            },
        ).save()
