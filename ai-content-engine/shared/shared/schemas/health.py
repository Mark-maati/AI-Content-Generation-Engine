"""Health check response schema."""

from pydantic import BaseModel, Field


class DependencyHealth(BaseModel):
    name: str
    status: str
    latency_ms: float | None = None


class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    service: str
    version: str = "0.1.0"
    dependencies: list[DependencyHealth] = Field(default_factory=list)
