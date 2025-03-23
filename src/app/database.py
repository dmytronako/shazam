from typing import Generator, AsyncGenerator
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from config import settings


sync_engine = create_engine(settings.db_url)
async_engine = create_async_engine(settings.db_url)

create_session = sessionmaker(
    bind=sync_engine, class_=AsyncSession, expire_on_commit=False)
async_create_session = async_sessionmaker(
    bind=async_engine, class_=Session, expire_on_commit=False)


def db_session() -> Generator:
    with create_session() as session:
        yield session
    

async def async_db_session() -> AsyncGenerator:
    async with async_create_session() as async_session:
        yield async_session
