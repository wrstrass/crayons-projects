from bson import ObjectId
from enum import StrEnum, auto
from pydantic import BaseModel, PrivateAttr
from db import projects_collection


class Permission(StrEnum):
    FORBID = auto()
    VIEW = auto()
    EDIT = auto()
    FULL = auto()

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
    _id: ObjectId = PrivateAttr(None)
    name: str
    permissions: PermissionSet = PermissionSet()
    members: Members = Members()
    diagrams: list[str] = []

    _collection = projects_collection

    @classmethod
    async def find(cls, **lookup) -> "ProjectModel":
        result = await cls._collection.find_one(lookup)
        model = ProjectModel(**result)
        model._id = result["_id"]
        return model

    @classmethod
    async def get_by_name(cls, name) -> "ProjectModel":
        return await cls.find(name=name)

    async def save(self) -> "ProjectModel":
        if self._id is None:
            result = await self._collection.insert_one(
                self.dict()
            )
            self._id = result.inserted_id
        else:
            await self._collection.replace_one(
                {"_id": self._id}, self.dict()
            )
        return self

    def group(self, user_id: int) -> str:
        if user_id in self.members.owners:
            return "owners"
        elif user_id in self.members.devs:
            return "devs"
        elif user_id in self.members.users:
            return "users"
        else:
            return "etc"

    def access(self, user_id: int) -> Permission:
        group = self.group(user_id)
        if group == "owners":
            return self.permissions.owner
        elif group == "devs":
            return self.permissions.dev
        elif group == "users":
            return self.permissions.user
        else:
            return self.permissions.etc
