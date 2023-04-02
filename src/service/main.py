# -*- coding: utf-8 -*-
from typing import Any
from typing import Dict

from fastapi import FastAPI
from service.settings import config_settings
from service.app_routes import add_routes

from dsg_lib import logging_config

logging_config.config_log(
    logging_directory=config_settings.logging_directory,
    # or None and defaults to logging
    log_name=config_settings.log_name,
    # or None and defaults to "log.log"
    logging_level=config_settings.loguru_logging_level,
    # or "info" or "debug" or "warning" or "error" or "critical"
    # or None and defaults to "info"
    log_rotation=config_settings.loguru_rotation,
    # or None and default is 10 MB
    log_retention=config_settings.loguru_retention,
    # or None and defaults to "14 Days"
    log_backtrace=config_settings.loguru_log_backtrace,
    # or None and defaults to False
    app_name=config_settings.app_name,
    # app name is used to identify the application
    # this is an optional field
    enable_trace_id=config_settings.enable_trace_id,
)


# fastapi start
app = FastAPI(
    title=config_settings.app_name,
    description=config_settings.app_description,
    version=config_settings.app_version,
    openapi_url="/openapi.json",
    docs_url="/docs"
)

from service.app_routes import add_routes

add_routes(app=app)
