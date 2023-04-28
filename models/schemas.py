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

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    registered_at: datetime.date

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str

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
