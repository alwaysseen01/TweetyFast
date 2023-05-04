from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Hashtag, Tweet
from models.schemas import HashtagCreate, HashtagUpdate


class HashtagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_hashtag_by_id(self, hashtag_id):
        hashtag = await self.session.execute(select(Hashtag).where(Hashtag.id == hashtag_id))
        if hashtag is None:
            raise HTTPException(status_code=404, detail="Hashtag not found")

    async def add_hashtag(self, hashtag_data: HashtagCreate) -> Hashtag:
        hashtag_to_add = Hashtag(**hashtag_data.dict())
        self.session.add(hashtag_to_add)
        await self.session.commit()
        await self.session.refresh(hashtag_to_add)
        return hashtag_to_add

    async def update_hashtag(self, hashtag_id: int, hashtag_data: HashtagUpdate) -> Tweet:
        hashtag_to_update = await self.session.execute(select(Hashtag).where(Hashtag.id == hashtag_id))
        if not hashtag_to_update.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Hashtag not found")

        hashtag_to_update = hashtag_to_update.scalar_one()

        for field, value in hashtag_data.dict().items():
            setattr(hashtag_to_update, field, value)
        await self.session.commit()
        await self.session.refresh(hashtag_to_update)
        return hashtag_to_update

    async def delete_hashtag(self, hashtag_id: int) -> None:
        hashtag_to_delete = await self.session.execute(select(Hashtag).where(Hashtag.id == hashtag_id))
        if hashtag_to_delete is None:
            raise HTTPException(status_code=404, detail="Hashtag not found")

        hashtag_to_delete = hashtag_to_delete.scalar_one()

        await self.session.delete(hashtag_to_delete)
        await self.session.commit()
