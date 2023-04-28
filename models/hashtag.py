from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from ..utils.database import Base, metadata


class Hashtag(Base):
    __tablename__ = 'hashtags'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

