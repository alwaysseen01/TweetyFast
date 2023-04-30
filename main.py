from fastapi import FastAPI
from fastapi_users import fastapi_users, FastAPIUsers

from api.user_api import router as user_router
from api.tweet_api import router as tweet_router
from api.hashtag_api import router as hashtag_router
from auth.auth import auth_backend
from auth.auth_schemas import UserAuthRead, UserAuthCreate
from auth.manager import get_user_manager
from models.models import User

app = FastAPI(
    title='Tweety'
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(tweet_router, prefix="/tweets", tags=["tweets"])
app.include_router(hashtag_router, prefix="/hashtags", tags=["hashtags"])
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserAuthRead, UserAuthCreate), prefix="/auth", tags=["auth"])
