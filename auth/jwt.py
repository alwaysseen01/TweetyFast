from datetime import datetime, timedelta

from fastapi import HTTPException, Header
from jose import jwt
from passlib.context import CryptContext

from utils.db_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm="HS256")
    return encoded_jwt


async def get_user_id(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        token_type, access_token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Authorization error")

        try:
            data = jwt.decode(access_token, str(SECRET_KEY), algorithms=ALGORITHM)
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Authorization error")

        return data['id']
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Authorization error")
