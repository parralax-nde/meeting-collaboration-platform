"""FastAPI application factory for the File service."""

import logging

from fastapi import FastAPI

from .config import settings
from .routers import health

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    application = FastAPI(
        title="File",
        description="Handles file uploads and sharing within meetings",
        version="0.1.0",
    )
    application.include_router(health.router)
    return application


app = create_app()
