from pydantic import BaseModel
from models import ProjectModel, Members, PermissionSet, Permission


class NameSchema(BaseModel):
    name: str


class ProjectSchema(BaseModel):
    name: str
    permissions: PermissionSet
    access_level: Permission | None = None
    members: Members
    diagrams: list[str]

    @classmethod
    def from_model(cls, obj: ProjectModel) -> "ProjectSchema":
        return ProjectSchema(
            name=obj.name,
            permissions=obj.permissions,
            members=obj.members,
            diagrams=obj.diagrams,
        )

    def format_access(self, access_level: Permission) -> str:
        self.access_level = access_level
        if access_level == Permission.FORBID:
            exclude = {"name", "permissions", "members", "diagrams"}
        elif access_level == Permission.VIEW or access_level == Permission.EDIT:
            exclude = {"permissions", "members"}
        else:
            exclude = {}
        return self.dict(exclude=exclude)
