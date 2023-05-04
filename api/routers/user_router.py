from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.user_repository import UserRepository
from models.schemas import UserUpdate, UserRead
from utils.database import get_async_session

router = APIRouter(
    tags=["User"],
    prefix="/api"
)


@router.get("/users/", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    users = await user_repository.get_users()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    user = await user_repository.get_user_by_id(user_id)
    return user


@router.get("/users/by-username/{username}")
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    user = await user_repository.get_user_by_username(username)
    return user


"""
'add_user' method is configured in 'auth' module
"""


@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    user_to_update = await user_repository.update_user(user_id, user_data)
    return user_to_update


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)

    user_to_delete = await user_repository.delete_user(user_id)
    return user_to_delete
