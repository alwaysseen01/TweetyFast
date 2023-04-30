from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import declarative_base, relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False, default='default_password')
    registered_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


class Tweet(Base):
    __tablename__ = 'tweets'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='tweets')
    text = Column(String(280), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class Hashtag(Base):
    __tablename__ = 'hashtags'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
