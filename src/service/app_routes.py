# -*- coding: utf-8 -*-
from fastapi import status
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from service.core.http_codes import GET_CODES
from loguru import logger
from service.api import health



def add_routes(app):
    
    
    @app.get("/",responses=GET_CODES)
    async def root():
        """
        Root endpoint of API
        Returns:
            Redrects to openapi document
        """
        logger.info("Root endpoint called") # Log an info message
        # redirect to openapi docs
        response = RedirectResponse(url="/docs",status_code=307)
        return response
    
    # Health router
    app.include_router(
        health.router,
        prefix="/api/health",
        tags=["system-health"],
        # responses=router_responses,
    )