from enum import StrEnum, auto
from pydantic import BaseModel


class Permission(StrEnum):
    FULL = auto()
    EDIT = auto()
    VIEW = auto()
    FORBID = auto()

class PermissionSet(BaseModel):
    owner: Permission = Permission.FULL
    dev: Permission = Permission.EDIT
    user: Permission = Permission.VIEW
    etc: Permission = Permission.FORBID


class Members(BaseModel):
    owners: list[int] = []
    devs: list[int] = []
    users: list[int] = []


class ProjectModel(BaseModel):
    name: str
    permissions: PermissionSet = PermissionSet()
    members: Members = Members()
    diagrams: list[str] = []
