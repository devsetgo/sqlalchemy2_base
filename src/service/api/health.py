# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Optional

from cpuinfo import get_cpu_info
from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from loguru import logger
from pydantic import BaseModel
from starlette_prometheus import PrometheusMiddleware, metrics

from src.service.core.http_codes import SYSTEM_INFO_CODE
from src.service.core.process_checks import get_processes
from src.service.settings import config_settings

router = APIRouter()

# TODO: detmine method to shutdown/restart python application
# TODO: Determine method to get application uptime

router.add_route("/metrics", metrics)


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
                "status": "UP",
                "uptime": "1 days, 5 hours, 23 minutes, 45 seconds",
                "current_datetime": "2022-06-30 15:43:10.123456",
            }
        }


@router.get("/status", tags=["system-health"], response_model=HealthCheckResponseModel)
async def health_main() -> Optional[HealthCheckResponseModel]:
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
        # Calculate uptime by subtracting the start time from the current time
        uptime = datetime.now() - config_settings.date_run

        # Convert uptime to timedelta object for better representation
        uptime_value = timedelta(seconds=int(uptime.total_seconds()))

        # Get the current datetime on the system
        current_datetime = datetime.now().isoformat(timespec="microseconds")

        # Define a log message with the relevant information
        log_message = f"Health check succeeded. Uptime: {uptime_value}, Current datetime: {current_datetime}"

        # Log the message at the INFO level
        logger.info(log_message)

        # Return the status, uptime, and current datetime in a dictionary format
        return {
            "status": "UP",
            "uptime": uptime_value,
            "current_datetime": current_datetime,
        }

    except Exception as ex:
        # Define an error message with the relevant information
        error_message = f"Health check failed with error: {ex}"

        # Log the message at the ERROR level
        logger.error(error_message)

        # Raise an HTTPException with status code 500 and detail message
        raise HTTPException(
            status_code=500, detail="Health check failed. Please try again later."
        )


@router.get("/system-info", responses=SYSTEM_INFO_CODE, tags=["system-health"])
async def health_status() -> dict:
    """
    GET Request for CPU and process data.

    Returns a dictionary containing the current datetime and system information.
    The "system_info" key contains information about the system's CPU usage.
    """

    try:
        system_info = get_cpu_info()
        current_datetime = datetime.now().isoformat(timespec="microseconds")
        result = {
            "current_datetime": current_datetime,
            "system_info": system_info,
        }
        # Log a message with the returned result at the DEBUG level
        logger.debug(f"Returned system info: {result}")
        return result

    except Exception as ex:
        # Log an error message if an exception is raised
        logger.error(f"Error retrieving CPU information: {ex}")
        raise HTTPException(status_code=409, detail="Error retrieving CPU information.")


@router.get("/processes", tags=["system-health"])
async def health_processes() -> dict:
    """
    GET running processes and filter by python processes
    Returns:
        dict -- [pid, name, username]
    """
    try:
        system_info = get_processes()
        current_datetime = datetime.now().isoformat(timespec="microseconds")
        result: dict = {
            "current_datetime": current_datetime,
            # "note": "this is filter to only return, python, gunicorn,
            # uvicorn, hypercorn, and daphne pids for security",
            "running_processes": system_info,
        }
        # Log a message with the returned result at the DEBUG level
        logger.debug(f"Returned running processes: {result}")
        return result
    except Exception as ex:
        # Log an error message if an exception is raised
        logger.error(f"Error retrieving running processes: {ex}")
        raise HTTPException(
            status_code=409, detail="Error retrieving running processes."
        )


@router.get("/configuration", responses=SYSTEM_INFO_CODE)
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

    except Exception as ex:
        # If an exception is raised, log an error message and raise an HTTPException with status 409.
        logger.error(f"Error retrieving configuration: {ex}")
        raise HTTPException(status_code=409, detail="Error retrieving configuration.")
