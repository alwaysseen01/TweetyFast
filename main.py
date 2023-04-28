from fastapi import FastAPI
from api.user_api import router as user_router
from api.tweet_api import router as tweet_router
from api.hashtag_api import router as hashtag_router

app = FastAPI(
    title='Tweety'
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(tweet_router, prefix="/tweets", tags=["tweets"])
app.include_router(hashtag_router, prefix="/hashtags", tags=["hashtags"])
