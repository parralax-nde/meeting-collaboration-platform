"""Health-check router."""

from fastapi import APIRouter

from mcp_shared.models import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    """Return a simple liveness indicator."""
    return HealthResponse(status="ok", service="action_items")
