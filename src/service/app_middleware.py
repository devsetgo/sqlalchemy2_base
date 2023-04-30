# -*- coding: utf-8 -*-
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from loguru import logger
from settings import config_settings
from starlette.middleware.sessions import SessionMiddleware
from starlette_exporter import PrometheusMiddleware

from service.core.custom_middleware import LoggerMiddleware


def add_middleware(app):
    # add middleware
    logger.info("Loading Middleware")
    # gzip middelware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    # logger middleware
    app.add_middleware(LoggerMiddleware)
    # session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=config_settings.secret_key,
        max_age=config_settings.max_timeout,
        same_site="strict",
        session_cookie="session_set",
    )
    # require HTTPS
    if config_settings.https_on == True:
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.warning(
            f"https is set to {config_settings.https_on} and will required https connections"
        )

    if config_settings.prometheus_on == True:
        app.add_middleware(
            PrometheusMiddleware,
            app_name=config_settings.app_name,
            prefix=config_settings.app_name,
            group_paths=True,
            buckets=[0.1, 0.25, 0.5],
            skip_paths=["/metrics"],
            always_use_int_status=False,
        ),
        logger.info("prometheus middleware enabled")
