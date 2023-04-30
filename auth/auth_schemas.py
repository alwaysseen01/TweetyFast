from datetime import datetime
from fastapi_users import schemas


class UserAuthRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserAuthCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserAuthUpdate(schemas.BaseUserUpdate):
    username: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
