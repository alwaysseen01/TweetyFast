import datetime

from pydantic import BaseModel

"""
User schemas
"""


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    registered_at: datetime.date
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    registered_at: datetime.date
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


"""
Tweet schemas
"""


class TweetRead(BaseModel):
    id: int
    user_id: int
    text: str
    created_at: datetime.date

    class Config:
        orm_mode = True


class TweetCreate(BaseModel):
    user_id: int
    text: str
    created_at: datetime.date

    class Config:
        orm_mode = True


class TweetUpdate(BaseModel):
    text: str

    class Config:
        orm_mode = True


"""
Hashtag schemas
"""


class HashtagRead(BaseModel):
    id: int
    name: str
    created_at: datetime.date
    updated_at: datetime.date

    class Config:
        orm_mode = True


class HashtagCreate(BaseModel):
    name: str
    created_at: datetime.date
    updated_at: datetime.date

    class Config:
        orm_mode = True


class HashtagUpdate(BaseModel):
    name: str
    updated_at: datetime.date

    class Config:
        orm_mode = True
