from exceptions import HTTP_403
from models import ProjectModel, PermissionSet, Permission
from schemas import ProjectSchema, ProjectOverview


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
    async def get_all(user_id: int) -> list[ProjectOverview]:
        result = []
        for group in ("owner", "dev", "user"):
            async for project in ProjectModel._collection.find({f"members.{group}s": user_id}):
                print(project)
                result.append(ProjectOverview(
                    name=project["name"],
                    group=group + "s",
                    permission=project["permissions"][group],
                ))
        return result

    @staticmethod
    async def get(name: str, user_id: int):
        project = await ProjectModel.get_by_name(name)
        access_level = project.access(user_id)
        return ProjectSchema.from_model(project).format_access(access_level)

    @staticmethod
    async def get_access(diagram_oid: str, user_id: int):
        project = await ProjectModel.find(diagrams=diagram_oid)
        return project.access(user_id)

    @staticmethod
    async def add_user(project_name: str, author_id: int, user_id: int, group: str):
        project = await ProjectModel.get_by_name(project_name)
        access_level = project.access(author_id)
        if access_level != Permission.FULL:
            raise HTTP_403()
        project.members.__getattribute__(group).append(user_id)
        await project.save()
        return project.members.__getattribute__(group)

    @staticmethod
    async def add_diagram(project_name: str, author_id: int, diagram_oid: str):
        project = await ProjectModel.get_by_name(project_name)
        access_level = project.access(author_id)
        if access_level != Permission.FULL:
            raise HTTP_403()
        project.diagrams.append(diagram_oid)
        await project.save()
        return diagram_oid

    @staticmethod
    async def set_permissions(project_name: str, author_id: int, permissions: PermissionSet):
        project = await ProjectModel.get_by_name(project_name)
        access_level = project.access(author_id)
        if access_level != Permission.FULL:
            raise HTTP_403()
        project.permissions = permissions
        await project.save()
        return project.permissions
