"""FastAPI application factory for the Action Items service."""

import logging

from fastapi import FastAPI

from .config import settings
from .routers import health

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    application = FastAPI(
        title="Action Items",
        description="Tracks action items assigned during meetings",
        version="0.1.0",
    )
    application.include_router(health.router)
    return application


app = create_app()
