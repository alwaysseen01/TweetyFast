from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True
        validate_assigment = True


class UserLogin(BaseModel):
    username: str
    password: str
