"""FastAPI application factory for the Action Items service."""

from fastapi import FastAPI

from mcp_shared.errors import register_error_handlers
from mcp_shared.logging import configure_logging

from .config import settings
from .routers import health

logger = configure_logging("action_items", level=settings.log_level)


def create_app() -> FastAPI:
    application = FastAPI(
        title="Action Items",
        description="Tracks action items assigned during meetings",
        version="0.1.0",
    )
    application.include_router(health.router)
    register_error_handlers(application)
    return application


app = create_app()
