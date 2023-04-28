from fastapi import FastAPI
from api.user_api import router as user_router

app = FastAPI(
    title='Tweety'
)

app.include_router(user_router)
