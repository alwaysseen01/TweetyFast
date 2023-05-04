from datetime import datetime

from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'user'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    profile = relationship('UserProfile', uselist=False, back_populates='user')
    tweet = relationship('Tweet', back_populates='user')

    following = relationship("Follower", foreign_keys="[Follower.user_id]", back_populates="user")
    followers = relationship("Follower", foreign_keys='Follower.follower_id', back_populates="follower")


class UserProfile(Base):
    __tablename__ = 'user_profile'
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    bio = Column(String(256), nullable=True)
    location = Column(String(50), nullable=True)
    website = Column(String(256), nullable=True)

    user = relationship('User', back_populates='profile')


class Tweet(Base):
    __tablename__ = 'tweet'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    text = Column(String(280), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='tweet')
    hashtags = relationship('Hashtag', secondary='tweet_hashtags', back_populates='tweets')


class Hashtag(Base):
    __tablename__ = 'hashtag'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tweets = relationship('Tweet', secondary='tweet_hashtags', back_populates='hashtags')


class TweetHashtag(Base):
    __tablename__ = 'tweet_hashtags'
    metadata = metadata

    tweet_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey('hashtag.id'), primary_key=True)


class Follower(Base):
    __tablename__ = "follower"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    follower_id = Column(Integer, ForeignKey("user.id"))
    followed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="followers")
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
