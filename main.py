from fastapi import FastAPI

from api.routers.user_router import router as user_router
from api.routers.tweet_router import router as tweet_router
from api.routers.hashtag_router import router as hashtag_router
from api.routers.tweet_hashtag_router import router as tweet_hashtag_router
from api.routers.follower_router import router as follower_router
from auth.routers import router as auth_router

app = FastAPI(
    title='Tweety'
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(tweet_router)
app.include_router(hashtag_router)
app.include_router(tweet_hashtag_router)
app.include_router(follower_router)

