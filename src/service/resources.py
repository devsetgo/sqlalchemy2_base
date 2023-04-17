# -*- coding: utf-8 -*-
from loguru import logger
from service.settings import config_settings
from service.database import db_session
from service.database.user_model import User
from service.core.user_lib import encrypt_pass
import datetime


class DatabaseInitializationError(Exception):
    """
    Custom exception for database initialization errors.
    """

    pass


async def startup_events():
    """
    Startup events for application. This function connects to the database and creates all tables.
    If there is an error during database initialization and table creation, a custom exception called
    DatabaseInitializationError is raised with the error message.

    Example:
    --------
    To run this function, call it from another async function like so:

    >>> async def main():
    ...     await startup_events()

    """
    try:
        # connect to database
        await db_session.db.init()
        await db_session.db.create_all()
        logger.info("Connecting to database")

    except Exception as ex:
        error: str = f"Error during database initialization and table creation {ex}"
        logger.critical(error)
        raise DatabaseInitializationError(error)

    # initiate log with statement
    if config_settings.release_env.lower() == "dev":
        logger.warning(f"environment set to 'dev' ")
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    else:
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    await create_default_user()


async def shutdown_events():
    """
    This function is responsible for shutting down events. It closes the database connection and logs the event.

    Args:
        None

    Returns:
        None
    """
    try:
        # Close the database connection
        await db_session.db.close()

        # Log that the database has been disconnected
        logger.info("Disconnected from database")
    except Exception as ex:
        # If there's an exception, log it as an error
        error: str = f"Error shutting down database: {ex}"
        logger.error(error)

    # Log that the API is shutting down
    logger.info("API shutting down")


async def create_default_user():
    values: dict = {
        "first_name": config_settings.admin_first_name,
        "last_name": config_settings.admin_last_name,
        "email": config_settings.admin_email.lower(),
        "password": None,
        "is_admin": True,
    }
    hash_pwd = encrypt_pass(config_settings.admin_password)
    values["password"] = hash_pwd

    user = await User.create(**values)
    logger.debug(f"creating default user: {user}")
    await User.create_demo_data(num_instances=10)
