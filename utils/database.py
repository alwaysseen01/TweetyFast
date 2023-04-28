from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from db_config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


metadata = MetaData()
Base = declarative_base(metadata=metadata)


async def create_tables():
    engine = create_async_engine(DATABASE_URL)
    metadata.bind = engine  # bind metadata to the engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all, bind=engine)

async_sessionmaker = sessionmaker(
    bind=create_async_engine(DATABASE_URL, echo=True),
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    async with async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()
