from datetime import datetime
from pydantic import BaseModel
import jwt

from exceptions import HTTP_401
from config import AUTH_SECRET_KEY


class JWTToken(BaseModel):
    user_id: int
    created_at: datetime


def decode(token: str) -> JWTToken:
    try:
        token = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except jwt.DecodeError:
        raise HTTP_401(detail="Invalid JWT")
    token["created_at"] = datetime.fromtimestamp(token["created_at"])
    return JWTToken(**token)
