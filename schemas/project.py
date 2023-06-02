from pydantic import BaseModel
from models import ProjectModel, PermissionSet, Members


class NameSchema(BaseModel):
    name: str


class ProjectSchema(BaseModel):
    name: str
    permissions: PermissionSet
    members: Members
    diagrams: list[str]

    @classmethod
    def from_model(cls, obj: ProjectModel) -> None:
        return ProjectSchema(
            name=obj.name,
            permissions=obj.permissions,
            members=obj.members,
            diagrams=obj.diagrams,
        )
