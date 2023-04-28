from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from models.schemas import UserRead, UserUpdate, UserCreate
from utils.database import get_async_session

router = APIRouter()


@router.get('/', response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    users = await session.execute(select(User))
    return users.scalars().all()


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.scalar_one()


@router.post('/', response_model=UserRead)
async def add_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_to_add = User(**user_data.dict())
    session.add(user_to_add)
    await session.commit()
    await session.refresh(user_to_add)
    return user_to_add


@router.put('/{user_id}', response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user_to_update = await session.execute(select(User).where(User.id == user_id))
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_update = user_to_update.scalar_one()

    for field, value in user_data.dict().items():
        setattr(user_to_update, field, value)
    await session.commit()
    await session.refresh(user_to_update)
    return user_to_update


@router.delete('/{user_id}')
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_to_delete = await session.execute(select(User).where(User.id == user_id))
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_to_delete = user_to_delete.scalar_one()
    await session.delete(user_to_delete)
    await session.commit()
