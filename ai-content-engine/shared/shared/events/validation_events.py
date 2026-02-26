"""Output validation events."""

import uuid

from pydantic import BaseModel, Field


class ValidationCompletedEvent(BaseModel):
    """Published when output parsing and validation succeeds."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    parsed_output: dict
    validation_results: dict = Field(default_factory=dict)
    schema_id: uuid.UUID | None = None
    schema_version: str | None = None


class ValidationFailedEvent(BaseModel):
    """Published when output validation fails."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    raw_response: str
    errors: list[dict] = Field(default_factory=list)
    stage: str = ""
