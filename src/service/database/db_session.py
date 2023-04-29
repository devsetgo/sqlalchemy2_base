# -*- coding: utf-8 -*-
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from loguru import logger
from service.settings import config_settings
from sqlalchemy.exc import SQLAlchemyError

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


class AsyncDatabaseSession:
    """
    A class for managing asynchronous database sessions using SQLAlchemy and async engine.

    Attributes:
        _session (AsyncSession): The async session object.
        _engine (create_async_engine): The async engine object.
    """

    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the underlying session object.

        Args:
            name (str): The attribute name.

        Returns:
            Any: The value of the requested attribute.
        """
        return getattr(self._session, name)

    async def init(self) -> None:
        """
        Initialize the database engine and create an async session.

        Raises:
            SQLAlchemyError: If there is an error initializing the database engine.
        """
        try:
            logger.info("Initializing database engine...")
            self._engine = create_async_engine(
                db_config,
                future=True,
            )

            async_session = sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession
            )

            async with async_session() as session:
                self._session = session

            logger.info("Database engine initialized successfully.")
        except SQLAlchemyError:
            logger.exception("Error initializing database engine")
            raise

    async def create_all(self) -> None:
        """
        Create all tables in the database.

        Raises:
            SQLAlchemyError: If there is an error creating the database tables.
        """
        try:
            logger.info("Creating database tables...")
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")
        except SQLAlchemyError:
            logger.exception("Error creating database tables")
            raise

    async def connect(self) -> None:
        """
        Connect to the database by initializing the engine and session.
        """
        await self.init()

    async def disconnect(self) -> None:
        """
        Disconnect from the database by closing the session and disposing the engine.
        """
        await self._session.close()
        await self._engine.dispose()
        logger.info("Disconnected from database")


db = AsyncDatabaseSession()


