from fastapi import FastAPI
from api.user_api import router as user_router
from api.tweet_api import router as tweet_router

app = FastAPI(
    title='Tweety'
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(tweet_router, prefix="/tweets", tags=["tweets"])
