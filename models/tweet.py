from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..utils.database import Base, metadata


class Tweet(Base):
    __tablename__ = 'tweets'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='tweets')
    text = Column(String(280), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
