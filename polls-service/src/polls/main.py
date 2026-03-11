"""FastAPI application factory for the Polls service."""

from fastapi import FastAPI

from mcp_shared.errors import register_error_handlers
from mcp_shared.logging import configure_logging

from .config import settings
from .routers import health

logger = configure_logging("polls", level=settings.log_level)


def create_app() -> FastAPI:
    application = FastAPI(
        title="Polls",
        description="Manages in-meeting polls and voting",
        version="0.1.0",
    )
    application.include_router(health.router)
    register_error_handlers(application)
    return application


app = create_app()
