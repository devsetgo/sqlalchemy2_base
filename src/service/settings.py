# -*- coding: utf-8 -*-

"""
Application configuration module.
Perform application configurations in accordance with the environment variables that have been set.
It is recommended to store environment variables locally using a .env file for local development.

Example usage:

    >>> from config import get_settings
    >>> settings = get_settings()

"""

import logging  # A Python library used for logging messages
import secrets  # A Python library used for generating secure random numbers
from datetime import datetime  # A Python library used for working with dates and times
from enum import Enum
from functools import lru_cache

from pydantic import (
    BaseSettings,  # A library for data validation and settings management
)
from pydantic import validator


class DatabaseDriverEnum(
    str, Enum
):  # creating an Enum class to hold database driver values
    postgres = "postgresql+asyncpg"  # defining the value for postgres driver
    sqlite = "sqlite+aiosqlite"  # defining the value for sqlite driver
    mysql = "mysql+aiomysql"  # defining the value for mysql driver
    oracle = "oracle+cx_oracle"  # defining the value for oracle driver

    class Config:  # creating a nested class to hold configuration options for the Enum class
        use_enum_values = True  # setting the configuration option to use the Enum values instead of their names


class Settings(BaseSettings):
    """
    Class that defines the various configuration attributes required by the application.

    Attributes:
        app_name (str): The name of the application.
        app_version (str): The current version of the application.
        app_description(str): A brief description of what the application does.

        release_env (str): The current environment in which the application is running.
        debug (bool): If true, enables debugging mode.

        workers (int): The number of worker threads to run on deployment.

        max_timeout (int): Time before session times out.
        same_site (str): Value of cookie attribute samesite ('lax', 'strict', 'none').
        login_timeout (int): Time allowed for login attempt.

        https_on (bool): Enable HTTPS validation.

        prometheus_on (bool): Enables Prometheus monitoring.

        database_driver (str): The type of database driver being used.
        db_username (str): The username to log in to the database.
        db_password (str): The password to log in to the database.
        db_location (str): The location of the database.
        db_name (str): The name of the database.

        log_name (str): The name of the logfile.
        loguru_retention (str): The retention period for log files.
        loguru_rotation (str): The maximum file size before rotation.
        loguru_logging_level (str): The minimum logging level.

        csrf_secret (str): A randomly generated session token.
        secret_key (str): A randomly generated app secret key.

        invalid_character_list (list): A list of characters that are not allowed in user input.

        date_run (datetime): The current date and time when the application was last run.

    """

    # List of configuration attributes to exclude from the configuration endpoint
    exclude_config: list = [
        "pwd",
        "password",
        "database_type",
        "key",
        "csrf",
        "secret",
        "username",
    ]

    # Default values for configuration attributes
    app_name: str = "Demo"
    app_version: str = "1.0.0"
    app_description: str = "This is what the app is for."

    release_env: str = "prd"
    debug: bool = False

    workers: int = 2

    max_timeout: int = 7200
    same_site: str = "lax"
    login_timeout: int = 120

    https_on: bool = False

    prometheus_on: bool = True

    # Define database connection attributes
    database_driver: DatabaseDriverEnum = "sqlite"
    db_username: str = "test"
    db_password: str = "test"
    db_location: str = "localhost"
    db_name: str = "api"
    sqlite_memory: bool = False

    # Logging settings
    logging_directory: str = "log"
    log_name: str = "log.json"
    loguru_retention: str = "30 days"
    loguru_rotation: str = "10 MB"
    loguru_logging_level: str = "INFO"
    loguru_log_backtrace: bool = True
    enable_trace_id: bool = True

    # Generate CSRF secret key and secret key
    csrf_secret = secrets.token_hex(256)
    secret_key = secrets.token_hex(256)

    # Default values for admin user creation
    admin_user_name: str
    admin_first_name: str
    admin_last_name: str
    admin_email: str
    admin_password: str
    create_demonstration_data: bool = False
    create_demonstration_quantity: int = 0

    # Set the current date and time when the application is run
    date_run: datetime = datetime.utcnow()

    @validator("database_driver", pre=True)
    def parse_database_driver(cls, value):
        """
        Validator function to convert the input string to the corresponding enum member value.

        Args:
            value (str): The input string to be converted.

        Returns:
            The corresponding enum member value if the input string is valid, otherwise returns the input value.
        """
        if isinstance(value, str):
            try:
                return DatabaseDriverEnum[value]
            except KeyError:
                pass
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True


@lru_cache()
def get_settings():
    """
    Returns application settings read from .env file.

    Returns:
        Settings: A pydantic BaseSettings object containing the configuration values.
    """

    return Settings()  # Create an instance of the Settings class and return it


config_settings = (
    get_settings()
)  # Store the base settings object in a variable named config_settings
