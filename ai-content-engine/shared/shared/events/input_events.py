"""Input ingestion events."""

import uuid

from pydantic import BaseModel, Field


class InputReceivedEvent(BaseModel):
    """Published when a new generation request is validated and accepted."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID
    template_id: uuid.UUID
    template_version: str | None = None
    parameters: dict = Field(default_factory=dict)
    options: dict = Field(default_factory=dict)
