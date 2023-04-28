from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from ..utils.database import Base, metadata


class User(Base):
    __tablename__ = 'users'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
