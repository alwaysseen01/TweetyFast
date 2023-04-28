import datetime

from pydantic import BaseModel


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
