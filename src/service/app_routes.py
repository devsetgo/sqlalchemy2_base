# -*- coding: utf-8 -*-

from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from loguru import logger

from service.api import health
from service.core.http_codes import GET_CODES


def add_routes(app: FastAPI) -> None:
    """
    Adds routes to the FastAPI app instance.
    Args:
        app (FastAPI): The FastAPI app instance to which the routes needs to be added.
    """

    @app.get("/", response_class=HTMLResponse, responses=GET_CODES)
    async def root() -> Response:
        """
        Endpoint for the root URL path of API
        Returns:
            RedirectResponse: Redirects to openapi document
        """
        logger.info("Root endpoint called")  # Log an info message
        # redirect to openapi docs
        response = RedirectResponse(
            url="/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
        return response

    # Add Routers Below Here
    # Health Router
    app.include_router(
        health.router,
        prefix="/api/health",
        tags=["system-health"],
    )

    # user
    # auth
