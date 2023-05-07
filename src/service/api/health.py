# -*- coding: utf-8 -*-

# Import necessary modules
import io
import tracemalloc
from datetime import date, datetime, timedelta
from typing import Dict, List, Union

from cpuinfo import get_cpu_info_json
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import ORJSONResponse
from fastapi_async_sqlalchemy.middleware import db
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette_exporter import handle_metrics

# Import custom modules
from service.core.http_codes import SYSTEM_INFO_CODE
from service.core.process_checks import get_processes
from service.database.common_schema import BaseDAO
from service.settings import config_settings

# Create an instance of APIRouter
router = APIRouter()

# Add a route to handle /metrics endpoint
router.add_route("/metrics", handle_metrics, include_in_schema=True)  # pragma: no cover


class HealthCheckResponseModel(BaseModel):
    """
    Health check response model to represent the system's status, uptime, and current datetime.

    Attributes:
        status (str): The status of the system.
        uptime (timedelta): The duration since the system started running.
        current_datetime (str): The current date and time on the system.

    """

    status: str
    uptime: timedelta
    current_datetime: str

    class Config:
        """
        Configuration for the health check response model.
        """

        # Example schema to help understand the expected format of data
        schema_extra = {
            "example": {
                "status": "up",
                "uptime": "1 days, 5 hours, 23 minutes, 45 seconds",
                "current_datetime": "2022-06-30 15:43:10.123456",
            }
        }


# route is /api/health
@router.get(
    "/status",
    tags=["system-health"],
    response_class=ORJSONResponse,
    response_model=HealthCheckResponseModel,
)
async def health_main() -> HealthCheckResponseModel:
    """
    GET status, uptime, and current datetime.

    Returns:
        dict: A dictionary containing the status, uptime, and current datetime of the system.

    Example:

        {
            "status": "UP",
            "uptime": "1 days, 5 hours, 23 minutes, 45 seconds",
            "current_datetime": "2022-06-30 15:43:10.123456"
        }

    """
    try:
        # Get the current datetime on the system
        current_datetime = datetime.now().isoformat(timespec="microseconds")

        # Calculate uptime by subtracting the start time from the current time
        uptime = datetime.now() - config_settings.date_run

        # Convert uptime to timedelta object for better representation
        uptime_value = timedelta(seconds=int(uptime.total_seconds()))

        # Define a log message with the relevant information
        log_message = f"Health check succeeded. Uptime: {uptime_value}, Current datetime: {current_datetime}"

        # Log the message at the INFO level
        logger.info(log_message)

        # Return the status, uptime, and current datetime in a dictionary format
        return {
            "status": "up",
            "uptime": uptime_value,
            "current_datetime": current_datetime,
        }
    except Exception as ex:  # pragma: no cover
        error: str = f"Error retriiving status: {ex}"
        # Log an error message if an exception is raised
        logger.error(error)
        raise HTTPException(status_code=500, detail=error)


# route is /api/health
@router.get(
    "/database",
    tags=["system-health"],
    response_class=ORJSONResponse,
    response_model=dict,
)
async def health_database() -> dict:
    """
    Check the status of the database connection.

    Returns:
        A dictionary containing the status of the database connection.
        If the connection is successful, it returns a dictionary with the following keys:
            - "database": "up"
            - "database_type": The type of the database (e.g. PostgreSQL, MySQL, etc.)
            - "version": The version of the database
        If the connection fails, it returns a dictionary with the following keys:
            - "database": "down"
            - "error_message": The error message returned by the database driver
    """
    # Get the database driver from the config settings
    data_base_driver = config_settings.database_driver

    try:
        # Retrieve database version using the db session
        if "sqlite" in data_base_driver:
            result = await db.session.execute(text("SELECT sqlite_version()"))
            version = result.scalar()
        else:
            result = await db.session.execute(text("SELECT version()"))
            version = result.scalar()

        # Determine database type based on the driver name
        if "postgresql" in data_base_driver:
            database_type = "PostgreSQL"
        elif "sqlite" in data_base_driver:
            database_type = "SQLite"
        elif "mysql" in data_base_driver:
            database_type = "MySQL"
        elif "oracle" in data_base_driver:
            database_type = "Oracle"
        else:
            database_type = "Unknown"

        # Log success message
        logger.success("Database is up and running")

        # Return the database status
        return {"database": "up", "database_type": database_type, "version": version}
    except Exception as e:
        # Log error message
        logger.error(f"Error connecting to database: {str(e)}")

        # Return an error message if connection fails
        return {"database": "down", "error_message": str(e)}


# route is /api/health
@router.get("/system-info", response_class=ORJSONResponse, tags=["system-health"])
def get_system_info() -> Dict[str, str]:
    """
    GET Request for CPU and process data.

    Returns a dictionary containing the current datetime and system information.
    The "system_info" key contains information about the system's CPU usage.
    """
    try:
        cpu_info = get_cpu_info_json()
        current_datetime = datetime.now().isoformat(timespec="microseconds")

        result = {"current_datetime": current_datetime, "cpu_info": cpu_info}

        # Log a message with the returned result at the DEBUG level
        logger.debug(f"Returned system info: {result}")

        return result

    except Exception as ex:  # pragma: no cover
        error: str = f"Error retrieving system info: {str(ex)}"
        # Log an error message with the exception details at the ERROR level
        logger.error(error)
        raise HTTPException(status_code=500, detail=error)


class Process(BaseModel):
    pid: int
    name: str
    username: str


class ProcessesResponse(BaseModel):
    current_datetime: str
    running_processes: List[Process]


# route is /api/health
@router.get(
    "/processes",
    response_class=ORJSONResponse,
    response_model=ProcessesResponse,
    tags=["system-health"],
)
async def health_processes() -> ProcessesResponse:
    """
    GET running processes and filter by python processes
    Returns:
        dict -- [pid, name, username]
    """
    try:
        running_processes = await get_processes()
        current_datetime = datetime.now().isoformat(timespec="microseconds")
        result = ProcessesResponse(
            current_datetime=current_datetime, running_processes=running_processes
        )
        logger.debug(f"Returned running processes: {result}")
        return result
    except Exception as ex:  # pragma: no cover
        logger.error(ex)
        raise


class ConfigurationResponse(BaseModel):
    configuration: Dict[str, Union[List[str], str, date]]

    class Config:
        """
        Configuration for the health check response model.
        """

        # Example schema to help understand the expected format of data
        schema_extra = {
            "example": {
                "configuration": {
                    "app_name": "Demo",
                    "app_version": "1.0.0",
                    "app_description": "This is what the app is for.",
                    "release_env": "prd",
                    "logging_directory": "log",
                    "log_name": "log.json",
                    "loguru_retention": "30 days",
                    "loguru_rotation": "10 MB",
                    "loguru_logging_level": "INFO",
                    "loguru_log_backtrace": "True",
                    "date_run": "2023-04-15",
                }
            }
        }


# route is /api/health
@router.get(
    "/configuration", responses=SYSTEM_INFO_CODE, response_model=ConfigurationResponse
)
async def configuration():
    """
    API information endpoint
    This function is used to retrieve API information like app version, environment running in (dev/prd),
    Doc/Redoc link, License information, and support information.
    Returns:
        [json] -- [description] app version, environment running in (dev/prd),
        Doc/Redoc link, Lincense information, and support information
    """
    try:
        # Retrieve configuration settings from a dictionary
        configuration: dict = config_settings.dict()

        # Remove sensitive data from the configuration dictionary using the pop() method.
        # These keys will be removed from the dictionary if they exist, otherwise nothing happens.
        key_exclude = config_settings.exclude_config
        key_exclude.append("exclude")

        for (
            key
        ) in (
            configuration.copy()
        ):  # iterate over a copy of the original keys so we can safely mutate the dictionary
            for exclude_word in key_exclude:
                if exclude_word in key:
                    configuration.pop(key, None)
                    break  # move on to the next key if an excluded word is found for this key

        # Create a dictionary with the resulting configuration data
        result = {
            "configuration": configuration,
        }

        # Log a message with the returned result at the INFO level
        logger.info("Completed configuration request.")

        # Return the resulting dictionary as JSON
        return result

    except Exception as ex:  # pragma: no cover
        error: str = f"Error retrieving configuration: {ex}"
        # If an exception is raised, log an error message and raise an HTTPException with status 409.
        logger.error(error)
        raise HTTPException(status_code=409, detail=error)


# route is /api/health
@router.get("/heapdump")
async def heapdump():
    """
    Retrieve a heap dump from the running application.

    Returns:
        A JSON object containing the heap dump.
    """
    tracemalloc.start()
    snapshot = tracemalloc.take_snapshot()
    buffer = io.StringIO()
    stats = snapshot.statistics("lineno")
    for stat in stats:
        buffer.write(str(stat) + "\n")
    heap_dump = buffer.getvalue().encode("utf-8")
    # Return the heap dump as a JSON response
    return Response(content=heap_dump, media_type="text/plain")
