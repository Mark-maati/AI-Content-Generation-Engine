"""Shared API response schemas."""

from shared.schemas.health import HealthCheckResponse
from shared.schemas.responses import DataResponse, ErrorResponse, PaginatedResponse

__all__ = [
    "DataResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "HealthCheckResponse",
]
