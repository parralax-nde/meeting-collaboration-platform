"""Base Pydantic models for request/response patterns across MCP services."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseRequest(BaseModel):
    """Base class for all incoming request bodies.

    Enables population by field alias (e.g. camelCase JSON keys) while still
    allowing access via the Python attribute name.
    """

    model_config = ConfigDict(populate_by_name=True)


class BaseResponse(BaseModel):
    """Base class for all outgoing response bodies.

    Enables construction from ORM objects (``from_attributes=True``) and
    supports both attribute name and alias access.
    """

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HealthResponse(BaseResponse):
    """Standard health-check response returned by every service's ``/health`` endpoint."""

    status: str
    service: str


class ErrorResponse(BaseResponse):
    """Standard error response body emitted by :func:`mcp_shared.errors.register_error_handlers`."""

    error: str
    message: str
    detail: Any = None


class PaginatedResponse(BaseResponse, Generic[T]):
    """Generic wrapper for paginated list responses.

    Example::

        from mcp_shared.models import PaginatedResponse

        @router.get("/notes", response_model=PaginatedResponse[NoteResponse])
        async def list_notes(page: int = 1, page_size: int = 20):
            items, total = paginate(all_notes, page, page_size)
            return PaginatedResponse(
                items=items, total=total, page=page, page_size=page_size
            )
    """

    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        """Total number of pages given the current :attr:`page_size`."""
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
