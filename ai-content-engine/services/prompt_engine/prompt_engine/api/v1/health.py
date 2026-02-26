"""Health check endpoint."""

from fastapi import APIRouter

from shared.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(service="prompt_engine")
