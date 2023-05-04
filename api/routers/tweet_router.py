from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.tweet_repository import TweetRepository
from models.schemas import TweetCreate, TweetUpdate
from utils.database import get_async_session

router = APIRouter(
    tags=["Tweet"],
    prefix="/api"
)


@router.get("/tweets/by-user-id/{user_id}")
async def get_tweets_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_repository = TweetRepository(session)

    tweets = await tweet_repository.get_tweets_by_user_id(user_id)
    return tweets


@router.get("/tweets/{tweet_id}")
async def get_tweet_by_id(tweet_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_repository = TweetRepository(session)

    tweet = await tweet_repository.get_tweet_by_id(tweet_id)
    return tweet


@router.post("/tweets/")
async def add_tweet(tweet_data: TweetCreate, session: AsyncSession = Depends(get_async_session)):
    tweet_repository = TweetRepository(session)

    tweet_to_add = await tweet_repository.add_tweet(tweet_data)
    return tweet_to_add


@router.put("/tweets/{tweet_id}")
async def update_tweet(tweet_id: int, tweet_data: TweetUpdate, session: AsyncSession = Depends(get_async_session)):
    tweet_repository = TweetRepository(session)

    tweet_to_update = await tweet_repository.update_tweet(tweet_id, tweet_data)
    return tweet_to_update


@router.delete("/tweets/{tweet_id}")
async def delete_tweet(tweet_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_repository = TweetRepository(session)

    tweet_to_delete = await tweet_repository.delete_tweet(tweet_id)
    return tweet_to_delete
