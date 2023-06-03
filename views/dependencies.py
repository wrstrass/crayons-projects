from datetime import datetime, timedelta
from fastapi import Header

from utils import decode
from exceptions import HTTP_401
from config import JWT_ACCESS_EXPIRE_TIME


async def authenticate(access_token: str = Header()) -> int:
    jwt_token = decode(access_token)
    if jwt_token.created_at + timedelta(minutes=JWT_ACCESS_EXPIRE_TIME) < datetime.now():
        raise HTTP_401(detail="Access Token expired")

    return jwt_token.user_id

async def authenticate_optional(access_token: str | None = Header(default=None)):
    if access_token is None:
        return -1
    else:
        return await authenticate(access_token)
