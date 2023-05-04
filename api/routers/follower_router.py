from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import get_async_session
from models.schemas import FollowerCreate
from api.repositories.follower_repository import FollowerRepository
from api.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users/{user_id}/followers", tags=["followers"])


@router.get("/")
async def get_followers_of_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    follower_repository = FollowerRepository(session)
    followers = await follower_repository.get_followers_of_user(user_id)
    await session.commit()
    return followers


@router.post("/")
async def add_follower_to_user(user_id: int, follower_data: FollowerCreate, session: AsyncSession = Depends(get_async_session)):
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Tweet not found")

    follower_repository = FollowerRepository(session)
    if follower_data.user_id == follower_data.follower_id:
        raise HTTPException(status_code=400, detail="User cannot follow themselves")

    existing_follower = await follower_repository.get_follower_by_user_and_follower_id(user_id,
                                                                                       follower_data.follower_id)
    if existing_follower:
        raise HTTPException(status_code=400, detail="User is already following this follower")

    follower = await follower_repository.get_follower_by_id(follower_data.follower_id)
    if follower is None:
        new_follower = await follower_repository.add_follower_to_user(follower_data)
        return new_follower

    await session.commit()
    return follower


@router.delete("/{follower_id}")
async def delete_follower_of_user(user_id: int, follower_id: int, session: AsyncSession = Depends(get_async_session)):
    follower_repository = FollowerRepository(session)

    await follower_repository.delete_follower_of_user(user_id, follower_id)
