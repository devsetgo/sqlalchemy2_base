# -*- coding: utf-8 -*-
from dsg_lib import logging_config
from fastapi import FastAPI
from service import resources
from service.app_routes import add_routes
from service.settings import config_settings

# Configure logging using dsg_lib.logging_config module
logging_config.config_log(
    logging_directory=config_settings.logging_directory,
    log_name=config_settings.log_name,
    logging_level=config_settings.loguru_logging_level,
    log_rotation=config_settings.loguru_rotation,
    log_retention=config_settings.loguru_retention,
    log_backtrace=config_settings.loguru_log_backtrace,
    app_name=config_settings.app_name,
    enable_trace_id=config_settings.enable_trace_id,
)

# Create a FastAPI app instance
app = FastAPI(
    title=config_settings.app_name,
    description=config_settings.app_description,
    version=config_settings.app_version,
    openapi_url="/openapi.json",
    docs_url="/docs",
    on_startup=[resources.startup_events],
    on_shutdown=[resources.shutdown_events],

)

# Add routes to the app instance
add_routes(app=app)
