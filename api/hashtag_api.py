from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Hashtag
from models.schemas import HashtagRead, HashtagUpdate, HashtagCreate
from utils.database import get_async_session

router = APIRouter()


@router.get('/', response_model=List[HashtagRead])
async def get_hashtags(session: AsyncSession = Depends(get_async_session)):
    hashtags = await session.execute(select(Hashtag))
    return hashtags.scalars().all()


@router.get('/{hashtag_id}', response_model=HashtagRead)
async def get_hashtag(hashtag_id: int, session: AsyncSession = Depends(get_async_session)):
    hashtag = await session.execute(select(Hashtag).where(Hashtag.id == hashtag_id))
    if hashtag is None:
        raise HTTPException(status_code=404, detail="Hashtag not found")
    return hashtag.scalar_one()


@router.post('/', response_model=HashtagRead)
async def add_hashtag(hashtag_data: HashtagCreate, session: AsyncSession = Depends(get_async_session)):
    hashtag_to_add = Hashtag(**hashtag_data.dict())
    session.add(hashtag_to_add)
    await session.commit()
    await session.refresh(hashtag_to_add)
    return hashtag_to_add


@router.put('/{hashtag_id}', response_model=HashtagRead)
async def update_hashtag(hashtag_id: int, hashtag_data: HashtagUpdate, session: AsyncSession = Depends(get_async_session)):
    hashtag_to_update = await session.execute(select(Hashtag).where(Hashtag.id == hashtag_id))
    if hashtag_to_update is None:
        raise HTTPException(status_code=404, detail="Hashtag not found")

    hashtag_to_update = hashtag_to_update.scalar_one()

    for field, value in hashtag_data.dict().items():
        setattr(hashtag_to_update, field, value)
    await session.commit()
    await session.refresh(hashtag_to_update)
    return hashtag_to_update


@router.delete('/{hashtag_id}')
async def delete_hashtag(hashtag_id: int, session: AsyncSession = Depends(get_async_session)):
    hashtag_to_delete = await session.execute(select(Hashtag).where(Hashtag.id == hashtag_id))
    if hashtag_to_delete is None:
        raise HTTPException(status_code=404, detail="Hashtag not found")

    hashtag_to_delete = hashtag_to_delete.scalar_one()
    await session.delete(hashtag_to_delete)
    await session.commit()
