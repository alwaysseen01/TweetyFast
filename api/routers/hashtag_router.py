from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.hashtag_repository import HashtagRepository
from models.schemas import HashtagCreate, HashtagUpdate, HashtagRead
from utils.database import get_async_session

router = APIRouter(
    tags=["Hashtag"],
    prefix="/api"
)


@router.get("/hashtags/{hashtag_id}", response_model=HashtagRead)
async def get_hashtag_by_id(hashtag_id: int, session: AsyncSession = Depends(get_async_session)):
    hashtag_repository = HashtagRepository(session)

    hashtag = await hashtag_repository.get_hashtag_by_id(hashtag_id)
    return hashtag


@router.post("/hashtags/")
async def add_hashtag(hashtag_data: HashtagCreate, session: AsyncSession = Depends(get_async_session)):
    hashtag_repository = HashtagRepository(session)

    hashtag_to_add = await hashtag_repository.add_hashtag(hashtag_data)
    return hashtag_to_add


@router.put("/hashtags/{hashtag_id}")
async def update_hashtag(hashtag_id: int, hashtag_data: HashtagUpdate, session: AsyncSession = Depends(get_async_session)):
    hashtag_repository = HashtagRepository(session)

    hashtag_to_update = await hashtag_repository.update_hashtag(hashtag_id, hashtag_data)
    return hashtag_to_update


@router.delete("/hashtags/{hashtag_id}")
async def delete_hashtag(hashtag_id: int, session: AsyncSession = Depends(get_async_session)):
    hashtag_repository = HashtagRepository(session)

    hashtag_to_delete = await hashtag_repository.delete_hashtag(hashtag_id)
    return hashtag_to_delete
