# -*- coding: utf-8 -*-
import time

from loguru import logger

from service.core.user_lib import encrypt_pass
from service.database.user_schema import User
from service.settings import config_settings


class DatabaseInitializationError(Exception):
    """
    Custom exception for database initialization errors.
    """


async def startup_events():
    """
    Startup events for application. This function connects to the database and creates all tables.
    If there is an error during database initialization and table creation, a custom exception called
    DatabaseInitializationError is raised with the error message.

    """

    try:
        # connect to database
        # await db_session.db.init()
        logger.info("Connecting to database")
        # await db_session.db.create_all()
        logger.info("Creating database tables")
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

    if config_settings.admin_email is not None:
        await create_default_user()
        logger.warning(f"Admin user {config_settings.admin_email} created")

    if config_settings.create_demonstration_data:
        t0 = time.time()
        dao = UserDAO()
        await dao.create_demo_user_data(
            num_instances=config_settings.create_demonstration_quantity
        )
        t1 = f"It took {time.time() - t0:.2f} seconds to create demo data"
        print(t1)
        logger.warning(f"Demo data created in the database")


async def shutdown_events():
    """
    This function is responsible for shutting down events. It closes the database connection and logs the event.

    Args:
        None

    Returns:
        None
    """
    # try:
    #     # Close the database connection
    #     await db_session.db.disconnect()
    # except Exception as ex:
    #     # If there's an exception, log it as an error
    #     error: str = f"Error shutting down database: {ex}"
    #     logger.error(error)

    # # Log that the API is shutting down
    # logger.info("API shutting down")


from service.database.user_schema import UserDAO


async def create_default_user():
    # Check if there are any existing users in the database
    dao = UserDAO()
    filters = {"is_admin": True}
    existing_users = await dao.list_all(filters=filters)
    if existing_users:
        logger.warning(
            "Default user creation aborted. User table already has existing data."
        )
        return

    values: dict = {
        "user_name": config_settings.admin_user_name,
        "first_name": config_settings.admin_first_name,
        "last_name": config_settings.admin_last_name,
        "email": config_settings.admin_email.lower(),
        "password": None,
        "is_admin": True,
    }
    hash_pwd = encrypt_pass(config_settings.admin_password)
    values["password"] = hash_pwd

    user = await dao.create(**values)
    logger.debug(f"creating default user: {user}")
