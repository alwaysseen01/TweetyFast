from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import TweetHashtag, Hashtag, Tweet
from models.schemas import TweetHashtagCreate


class TweetHashtagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_hashtags_by_tweet_id(self, tweet_id: int):
        hashtags = await self.session.execute(select(Hashtag).join(TweetHashtag).where(TweetHashtag.tweet_id == tweet_id))
        return hashtags.scalars().all()

    async def get_tweets_by_hashtag_id(self, hashtag_id: int):
        tweets = await self.session.execute(select(Tweet).join(TweetHashtag).where(TweetHashtag.hashtag_id == hashtag_id))
        return tweets.scalars().all()

    async def add_hashtag_to_the_tweet(self, tweet_hashtag_data: TweetHashtagCreate):
        tweet_hashtag_to_add = TweetHashtag(**tweet_hashtag_data.dict())
        self.session.add(tweet_hashtag_to_add)
        await self.session.commit()
        await self.session.refresh(tweet_hashtag_to_add)
        return tweet_hashtag_to_add

    async def delete_the_hashtag_of_tweet(self, tweet_id: int, hashtag_id: int):
        tweet_hashtag_to_delete = await self.session.execute(
            select(TweetHashtag).where(TweetHashtag.tweet_id == tweet_id).where(TweetHashtag.hashtag_id == hashtag_id)
        )

        if tweet_hashtag_to_delete is None:
            raise HTTPException(status_code=404, detail="Tweet-hashtag not found")

        tweet_hashtag_to_delete = tweet_hashtag_to_delete.scalar_one()

        await self.session.delete(tweet_hashtag_to_delete)
        await self.session.commit()


