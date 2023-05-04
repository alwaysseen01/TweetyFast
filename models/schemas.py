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
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    is_verified: bool
    registered_at: datetime.date

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
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


"""
Tweet-Hashtag schemas
"""


class TweetHashtagRead(BaseModel):
    tweet_id: int
    hashtag_id: int

    class Config:
        orm_mode = True


class TweetHashtagCreate(BaseModel):
    tweet_id: int
    hashtag_id: int

    class Config:
        orm_mode = True


"""
Follower schemas
"""


class FollowerCreate(BaseModel):
    user_id: int
    follower_id: int
    followed_at: datetime.date

    class Config:
        orm_mode = True


"""
UserProfile schemas
"""


class UserProfileCreate(BaseModel):
    first_name: str = None
    last_name: str = None
    bio: str = None
    location: str = None
    website: str = None

    class Config:
        orm_mode = True
