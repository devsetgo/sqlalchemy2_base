# -*- coding: utf-8 -*-
from typing import Any

from loguru import logger
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from service.settings import config_settings

Base = declarative_base()


def get_db_config() -> str:
    """
    Get the database configuration string based on the settings.

    Returns:
        str: The database configuration string.
    """
    db_driver = config_settings.database_driver

    if db_driver == "sqlite+aiosqlite":
        if config_settings.sqlite_memory:
            return f"{db_driver}:///:memory:?cache=shared"
        else:
            return f"{db_driver}:///_sqlite_db/{config_settings.db_name}.db"
    else:
        return f"{db_driver}://{config_settings.db_username}:{config_settings.db_password}@{config_settings.db_location}/{config_settings.db_name}"


db_config = get_db_config()
logger.debug(f"Database Driver Setting: {config_settings.database_driver}")


engine = create_async_engine(
    db_config,
    future=True,
)

# _Session = async_sessionmaker(engine, expire_on_commit=False, **session_args)
session_args = {}
_session_maker = async_sessionmaker(engine, expire_on_commit=False, **session_args)

# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception as e:
#             await session.rollback()
#         finally:
#             await session.close()
