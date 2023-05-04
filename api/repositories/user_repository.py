from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from models.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self):
        users = await self.session.execute(select(User))
        return users.scalars().all()

    async def get_user_by_id(self, user_id: int):
        user = await self.session.execute(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(status_code=404, detail="Tweet not found")

        return user.scalar_one()

    async def get_user_by_username(self, username: str):
        user = await self.session.execute(select(User).where(User.username == username))
        if not user.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="User not found")

        return user.scalar_one()

    async def add_user(self, user_data: UserCreate) -> User:
        user_to_add = User(**user_data.dict())
        self.session.add(user_to_add)
        await self.session.commit()
        await self.session.refresh(user_to_add)
        return user_to_add

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user_to_update = await self.session.execute(select(User).where(User.id == user_id))
        if not user_to_update.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="User not found")

        user_to_update = user_to_update.scalar_one()

        for field, value in user_data.dict().items():
            setattr(user_to_update, field, value)
        await self.session.commit()
        await self.session.refresh(user_to_update)
        return user_to_update

    async def delete_user(self, user_id: int) -> None:
        user_to_delete = await self.session.execute(select(User).where(User.id == user_id))
        if not user_to_delete.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="User not found")

        user_to_delete = user_to_delete.scalar_one()

        await self.session.delete(user_to_delete)
        await self.session.commit()
