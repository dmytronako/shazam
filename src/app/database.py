from typing import Generator, AsyncGenerator
import sqlalchemy.exc as sqlalchemy_exc
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from config import settings
from tables import Base


sync_engine = create_engine(settings.db_url)
async_engine = create_async_engine(settings.db_url)

create_session = sessionmaker(
    bind=sync_engine, class_=AsyncSession, expire_on_commit=False)
async_create_session = async_sessionmaker(
    bind=async_engine, class_=Session, expire_on_commit=False)


def db_session() -> Generator[Session]:
    with create_session() as session:
        try:
            yield session
        except sqlalchemy_exc.SQLAlchemyError as e:
            session.rollback()
            raise
            

async def async_db_session() -> AsyncGenerator[AsyncSession]:
    async with async_create_session() as async_session:
        try:
            yield async_session
        except sqlalchemy_exc.SQLAlchemyError as e:
            await async_session.rollback()
            raise


def init_db():
    Base.metadata.create_all(sync_engine)
