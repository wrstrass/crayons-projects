from pydantic import BaseModel


class NameSchema(BaseModel):
    name: str
