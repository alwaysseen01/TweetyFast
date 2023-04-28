from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Tweet
from models.schemas import TweetRead, TweetUpdate, TweetCreate
from utils.database import get_async_session

router = APIRouter()


@router.get('/', response_model=List[TweetRead])
async def get_tweets(session: AsyncSession = Depends(get_async_session)):
    tweets = await session.execute(select(Tweet))
    return tweets.scalars().all()


@router.get('/{tweet_id}', response_model=TweetRead)
async def get_tweet(tweet_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
    if tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet.scalar_one()


@router.post('/', response_model=TweetRead)
async def add_tweet(tweet_data: TweetCreate, session: AsyncSession = Depends(get_async_session)):
    tweet_to_add = Tweet(**tweet_data.dict())
    session.add(tweet_to_add)
    await session.commit()
    await session.refresh(tweet_to_add)
    return tweet_to_add


@router.put('/{tweet_id}', response_model=TweetRead)
async def update_tweet(tweet_id: int, tweet_data: TweetUpdate, session: AsyncSession = Depends(get_async_session)):
    tweet_to_update = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
    if tweet_to_update is None:
        raise HTTPException(status_code=404, detail="Tweet not found")

    tweet_to_update = tweet_to_update.scalar_one()

    for field, value in tweet_data.dict().items():
        setattr(tweet_to_update, field, value)
    await session.commit()
    await session.refresh(tweet_to_update)
    return tweet_to_update


@router.delete('/{tweet_id}')
async def delete_tweet(tweet_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_to_delete = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
    if tweet_to_delete is None:
        raise HTTPException(status_code=404, detail="Tweet not found")

    tweet_to_delete = tweet_to_delete.scalar_one()
    await session.delete(tweet_to_delete)
    await session.commit()