from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Tweet
from models.schemas import TweetCreate, TweetUpdate


class TweetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_tweets_by_user_id(self, user_id: int):
        tweets = await self.session.execute(select(Tweet).where(Tweet.user_id == user_id))

        return tweets.scalars().all()

    async def get_tweet_by_id(self, tweet_id: int):
        tweet = await self.session.execute(select(Tweet).where(Tweet.id == tweet_id))
        if not tweet.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Tweet not found")

        return tweet.scalar_one()

    async def add_tweet(self, tweet_data: TweetCreate) -> Tweet:
        tweet_to_add = Tweet(**tweet_data.dict())
        self.session.add(tweet_to_add)
        await self.session.commit()
        await self.session.refresh(tweet_to_add)
        return tweet_to_add

    async def update_tweet(self, tweet_id: int, tweet_data: TweetUpdate) -> Tweet:
        tweet_to_update = await self.session.execute(select(Tweet).where(Tweet.id == tweet_id))
        if not tweet_to_update.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Tweet not found")

        tweet_to_update = tweet_to_update.scalar_one()

        for field, value in tweet_data.dict().items():
            setattr(tweet_to_update, field, value)
        await self.session.commit()
        await self.session.refresh(tweet_to_update)
        return tweet_to_update

    async def delete_tweet(self, tweet_id: int) -> None:
        tweet_to_delete = await self.session.execute(select(Tweet).where(Tweet.id == tweet_id))
        tweet = tweet_to_delete.scalar_one_or_none()
        if not tweet:
            raise HTTPException(status_code=404, detail="Tweet not found")

        await self.session.delete(tweet)
        await self.session.commit()

