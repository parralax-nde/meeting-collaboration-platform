"""Custom exception hierarchy and FastAPI error handlers for MCP services."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


class MCPError(Exception):
    """Base exception for all MCP service errors.

    Subclasses should set :attr:`status_code` and :attr:`default_message` at
    the class level to describe the HTTP semantics of the error.
    """

    status_code: int = 500
    default_message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None, *, detail: Any = None) -> None:
        """Initialise the error.

        Args:
            message: Human-readable description of the error.  Falls back to
                :attr:`default_message` when *None*.
            detail: Optional machine-readable context (e.g. validation errors).
        """
        self.message = message or self.default_message
        self.detail = detail
        super().__init__(self.message)


class NotFoundError(MCPError):
    """Raised when a requested resource cannot be found (HTTP 404)."""

    status_code = 404
    default_message = "The requested resource was not found."


class ValidationError(MCPError):
    """Raised when input fails business-logic validation (HTTP 422)."""

    status_code = 422
    default_message = "Validation failed."


class AuthenticationError(MCPError):
    """Raised when a request lacks valid credentials (HTTP 401)."""

    status_code = 401
    default_message = "Authentication required."


class AuthorizationError(MCPError):
    """Raised when a caller lacks permission to perform an action (HTTP 403)."""

    status_code = 403
    default_message = "You do not have permission to perform this action."


class ConflictError(MCPError):
    """Raised when a state conflict prevents the operation (HTTP 409)."""

    status_code = 409
    default_message = "A conflict occurred with the current state of the resource."


class ServiceUnavailableError(MCPError):
    """Raised when a downstream dependency is unavailable (HTTP 503)."""

    status_code = 503
    default_message = "The service is temporarily unavailable. Please try again later."


# ---------------------------------------------------------------------------
# FastAPI integration (requires the ``web`` optional dependency)
# ---------------------------------------------------------------------------

if TYPE_CHECKING:
    from fastapi.responses import JSONResponse


def _build_error_body(exc: MCPError) -> dict[str, Any]:
    """Return a JSON-serialisable dict describing *exc*."""
    return {
        "error": type(exc).__name__,
        "message": exc.message,
        "detail": exc.detail,
    }


def register_error_handlers(app: Any) -> None:
    """Register MCP exception handlers on a FastAPI *app*.

    After calling this function every :class:`MCPError` (and its subclasses)
    raised inside a route handler will be converted to a structured JSON
    response with the appropriate HTTP status code.

    Args:
        app: A :class:`fastapi.FastAPI` application instance.

    Example::

        from fastapi import FastAPI
        from mcp_shared.errors import register_error_handlers

        app = FastAPI()
        register_error_handlers(app)
    """
    try:
        from fastapi.responses import JSONResponse
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "register_error_handlers() requires FastAPI. "
            "Install it with: pip install 'mcp-shared[web]'"
        ) from exc

    async def _handler(request: object, exc: MCPError) -> JSONResponse:  # noqa: ARG001
        return JSONResponse(
            status_code=exc.status_code,
            content=_build_error_body(exc),
        )

    app.add_exception_handler(MCPError, _handler)
