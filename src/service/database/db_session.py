# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from loguru import logger
from service.settings import config_settings

Base = declarative_base()

db_driver = config_settings.database_driver


if db_driver == "sqlite+aiosqlite":
    if config_settings.sqlite_memory:
        db_config = f"{db_driver}:///:memory:"
    else:
        db_config = f"{db_driver}:///sqlite_db/{config_settings.db_name}.db"
else:
    db_config = f"{db_driver}://{config_settings.db_username}:{config_settings.db_password}@{config_settings.db_location}/{config_settings.db_name}"

logger.debug(f"Database Driver Setting: {db_driver}")



class AsyncDatabaseSession:
    """
    This class creates an async database session and has two methods:

    1. init() - Initializes the database engine and creates a sessionmaker with an AsyncSession class.
    2. create_all() - Creates all tables from the Base metadata using run_sync() method from the connection.

    Example usage:
        db = AsyncDatabaseSession()
        await db.init()
        await db.create_all()
    """

    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        """
        Initializes the database engine and creates a sessionmaker with an AsyncSession class.
        """
        logger.info("Initializing database engine...")
        self._engine = create_async_engine(
            db_config,
            future=True,
            echo=True,
        )

        async_session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

        self._session = async_session()
        logger.info("Database engine initialized successfully.")

    async def create_all(self):
        """
        Creates all tables from the Base metadata using run_sync() method from the connection.
        """
        logger.info("Creating database tables...")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")

db = AsyncDatabaseSession()
