# -*- coding: utf-8 -*-

from service.settings import config_settings


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
