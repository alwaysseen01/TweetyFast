from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, MetaData, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


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
