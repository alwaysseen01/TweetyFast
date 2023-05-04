from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User, Follower
from models.schemas import FollowerCreate


class FollowerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_follower_by_id(self, follower_id: int):
        follower = await self.session.execute(select(Follower).where(Follower.id == follower_id))
        if follower is None:
            raise HTTPException(status_code=404, detail="Follower not found")

        return follower.scalar_one_or_none()

    async def get_followers_of_user(self, user_id: int):
        followers = await self.session.execute(
            select(User).join(Follower, Follower.follower_id == User.id).where(Follower.user_id == user_id))

        return followers.scalars().all()

    async def get_follower_by_user_and_follower_id(self, user_id: int, follower_id: int):
        follower = await self.session.execute(
            select(Follower).where(and_(Follower.user_id == user_id, Follower.follower_id == follower_id)))
        if follower is None:
            raise HTTPException(status_code=404, detail="Follower not found")

        return follower.scalar_one_or_none()

    async def get_users_followed_by_user_id(self, user_id: int):
        users_followed = await self.session.execute(
            select(User).join(Follower, Follower.user_id == User.id).where(Follower.follower_id == user_id))

        return users_followed.scalars().all()

    async def add_follower_to_user(self, follower_data: FollowerCreate):
        follower_to_add = Follower(**follower_data.dict())

        self.session.add(follower_to_add)
        await self.session.commit()
        await self.session.refresh(follower_to_add)
        return follower_to_add

    async def delete_follower_of_user(self, user_id: int, follower_id: int):
        follower_to_delete = await self.session.execute(
            select(Follower).where(Follower.user_id == user_id).where(Follower.follower_id == follower_id))
        if follower_to_delete is None:
            raise HTTPException(status_code=404, detail="Follower not found")

        follower_to_delete = follower_to_delete.scalar_one()

        await self.session.delete(follower_to_delete)
        await self.session.commit()

