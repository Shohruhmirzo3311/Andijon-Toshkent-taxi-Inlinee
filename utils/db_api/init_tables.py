import os

import sqlalchemy
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase


# Base class for models
class Base(DeclarativeBase):
    pass

# Database URL (example for PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/vodiy_taxi")
sqlalchemy.url = "postgresql+asyncpg://postgres:postgres@localhost/vodiy_taxi"


# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True for logging queries

# Session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



