# -*- coding: utf-8 -*-
from loguru import logger
from service.settings import config_settings
from service.database import db_session

async def startup_events():
    """
    Startup events for application
    """
    try:
        # connect to database
        await db_session.init()
        await db_session.db.create_all()
        logger.info("Connecting to database")

    except Exception as e:
        # log error
        logger.info(f"Error: {e}")
        logger.trace(f"tracing: {e}")

    # initiate log with statement
    if config_settings.release_env.lower() == "dev":
        logger.debug("initiating logging for api")
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    else:
        logger.info(f"api initiated release_env: {config_settings.release_env}")



async def shutdown_events():
    """
    Shut down events
    """
    # try:
    #     # discount database
    #     await database.disconnect()
    #     logger.info("Disconnecting from database")
    # except Exception as e:
    #     # log exception
    #     logger.info("Error: {error}", error=e)
    #     logger.trace("tracing: {exception} - {e}", error=e)

    logger.info("API shutting down")