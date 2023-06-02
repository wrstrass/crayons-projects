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
    _id: ObjectId | None = PrivateAttr(None)
    name: str
    permissions: PermissionSet = PermissionSet()
    members: Members = Members()
    diagrams: list[str] = []

    _collection = projects_collection

    @classmethod
    async def find(cls, **lookup) -> "ProjectModel":
        return await cls._collection.find_one(lookup)

    @classmethod
    async def get_by_name(cls, name) -> "ProjectModel":
        return await cls.find(name=name)

    async def save(self) -> None:
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
