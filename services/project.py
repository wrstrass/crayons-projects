from exceptions import HTTP_403
from models import ProjectModel, Permission
from schemas import ProjectSchema


class ProjectService:
    @staticmethod
    async def new(name: str, owner: int) -> ProjectModel:
        project = await ProjectModel(
            name=name,
            members={
                "owners": [owner,],
            },
        ).save()
        return ProjectSchema.from_model(project).format_access(Permission.FULL)
    
    @staticmethod
    async def get(name: str, user_id: int):
        project = await ProjectModel.get_by_name(name)
        access_level = project.access(user_id)
        return ProjectSchema.from_model(project).format_access(access_level)

    @staticmethod
    async def add_user(project_name: str, author_id: int, user_id: int, group: str):
        project = await ProjectModel.get_by_name(project_name)
        access_level = project.access(author_id)
        if access_level != Permission.FULL:
            raise HTTP_403()
        project.members.__getattribute__(group).append(user_id)
        await project.save()
        return project.members.__getattribute__(group)
