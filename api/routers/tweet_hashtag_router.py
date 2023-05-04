from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.tweet_hashtag_repository import TweetHashtagRepository
from models.schemas import TweetHashtagRead, TweetRead, TweetHashtagCreate, HashtagRead
from utils.database import get_async_session

router = APIRouter(
    tags=["Tweet-Hashtag"],
    prefix="/api"
)


@router.get("/tweets-hashtags/by-tweet-id/{tweet_id}", response_model=List[HashtagRead])
async def get_hashtags_by_tweet_id(tweet_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_hashtag_repository = TweetHashtagRepository(session)

    hashtags = await tweet_hashtag_repository.get_hashtags_by_tweet_id(tweet_id)
    return hashtags


@router.get("/tweets-hashtags/by-hashtag-id/{hashtag_id}", response_model=List[TweetRead])
async def get_tweets_by_hashtag_id(hashtag_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_hashtag_repository = TweetHashtagRepository(session)

    tweets = await tweet_hashtag_repository.get_tweets_by_hashtag_id(hashtag_id)
    return tweets


@router.post("/tweets-hashtags/{hashtag_id}")
async def add_hashtag_to_the_tweet(tweet_hashtag_data: TweetHashtagCreate, session: AsyncSession = Depends(get_async_session)):
    tweet_hashtag_repository = TweetHashtagRepository(session)

    hashtag_to_add = await tweet_hashtag_repository.add_hashtag_to_the_tweet(tweet_hashtag_data)
    return hashtag_to_add


@router.delete("/tweets-hashtags/{tweet_id}/{hashtag_id}")
async def delete_the_hashtag_of_tweet(tweet_id: int, hashtag_id: int, session: AsyncSession = Depends(get_async_session)):
    tweet_hashtag_repository = TweetHashtagRepository(session)

    hashtag_to_delete = await tweet_hashtag_repository.delete_the_hashtag_of_tweet(tweet_id, hashtag_id)
    return hashtag_to_delete
