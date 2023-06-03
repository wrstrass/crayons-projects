from pydantic import BaseModel


class NameSchema(BaseModel):
    name: str


class UserAndGroupSchema(BaseModel):
    user: int
    group: str
