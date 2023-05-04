from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select

from models.models import User, UserProfile
from auth.jwt import get_password_hash, verify_password, create_access_token
from models.schemas import UserCreate, UserProfileCreate
from utils.database import get_async_session
from auth.schemas import TokenOut, UserLogin
from utils.db_config import SECRET_KEY, ALGORITHM

router = APIRouter(
    tags=["Auth"],
    prefix="/api"
)


@router.post("/register")
async def register(user_data: UserCreate, profile_data: UserProfileCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        user_to_register = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            registered_at=datetime.utcnow(),
            is_active=user_data.is_active,
            is_verified=user_data.is_verified
        )
        session.add(user_to_register)
        await session.commit()
        await session.flush()
        await session.refresh(user_to_register)

        user_profile = UserProfile(
            user_id=user_to_register.id,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            bio=profile_data.bio,
            location=profile_data.location,
            website=profile_data.website
        )
        session.add(user_profile)

        await session.commit()
        await session.flush()
        await session.refresh(user_profile)

    except exc.IntegrityError as e:
        print(e)
        return {"Error": f'User with this email or username exists'}

    return user_to_register


@router.post("/login")
async def login(response: Response, user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    try:
        user_to_login = await session.execute(select(User).where(User.username == user_data.username))
        user_to_login = user_to_login.one()[0]

        if not verify_password(user_data.password, user_to_login.hashed_password):
            raise HTTPException(status_code=401, detail="Authorization error")
    except exc.NoResultFound as e:
        raise HTTPException(status_code=401, detail="Authorization error")

    data_to_encode = {"id": user_to_login.id}
    access_token = create_access_token(data_to_encode)
    refresh_token = create_access_token(data_to_encode, expires_delta=timedelta(minutes=1000))

    tokenOut = TokenOut(access_token=access_token, refresh_token=refresh_token)
    response.headers["Authorization"] = f'Bearer {access_token}'
    return tokenOut


@router.post("/refresh")
async def refresh(access_token: str, refresh_token: str, response: Response):
    try:
        data = jwt.decode(access_token, str(SECRET_KEY), algorithms=ALGORITHM)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Authorization error")

    new_access_token = create_access_token(data)
    new_refresh_token = create_access_token(data, expires_delta=timedelta(minutes=1000))
    tokenOut = TokenOut(access_token=new_access_token, refresh_token=new_refresh_token)
    response.headers["Authorization"] = f'Bearer {new_access_token}'
    return tokenOut
