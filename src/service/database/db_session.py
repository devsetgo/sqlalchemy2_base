# -*- coding: utf-8 -*-

"""
This module creates an Enum class called DatabaseDriverEnum which lists the URLs for different types of databases. It then creates a declarative base for SQLAlchemy as per documentation.

The `AsyncDatabaseSession` class in this module creates an async database session and has two methods:

1. init()
2. create_all()

`init()` method creates an engine and a sessionmaker with an AsyncSession class. The session is stored in the _session attribute.
The configuration settings are obtained from the 'config_settings' module from the 'service' package

`create_all()` method creates all tables from the Base metadata using run_sync() method from the connection.

Example:
    db = AsyncDatabaseSession()
    await db.init()
    await db.create_all()
"""

from pydantic import BaseSettings  # importing base settings from Pydantic
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from service.settings import (
    DatabaseDriverEnum,  # importing config settings from service package
)
from service.settings import config_settings

# from enum import Enum #importing Enum class from the enum module

# class DatabaseDriverEnum(str,Enum): #creating an Enum class
#     'postgres' ="postgresql+asyncpg"
#     'sqlite' = "sqlite+aiosqlite"
#     'mysql' = "mysql+aiomysql"
#     oracle = "oracle+cx_oracle"

# Creating a declarative base for SQLAlchemy as per documentation
Base = declarative_base()

# creating the URL for the database based on configuration settings
# db_config:str = f"{DatabaseDriverEnum.postgres}://{config_settings.db_username}:{config_settings.db_password}@{config_settings.db_location}/{config_settings.db_name}"

db_driver = config_settings.database_driver

if db_driver == "sqlite":
    if config_settings.sqlite_memory == True:
        db_config: str = f"{db_driver}:///:memory:"
    else:
        db_config: str = f"{db_driver}://sqlite_db/{config_settings.db_name}"
elif db_driver in DatabaseDriverEnum._member_names_:
    # db_driver = DatabaseDriverEnum(config_settings.database_driver)
    db_config: str = f"{db_driver}://{config_settings.db_username}:{config_settings.db_password}@{config_settings.db_location}/{config_settings.db_name}"

else:
    error = "There has been an issue creating the database configuration"
    raise ValueError("There has been an issue creating the database configuration")


# Creating a class for an async database session
class AsyncDatabaseSession:
    def __init__(self):
        self._session = None  # Initializing _session attribute
        self._engine = None  # Initializing _engine attribute

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine(
            db_config,
            future=True,
            echo=True,
        )

        async_session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

        self._session = async_session()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# Instantiating the AsyncDatabaseSession class
db = AsyncDatabaseSession()
