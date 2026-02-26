"""Persistence events."""

import uuid

from pydantic import BaseModel


class ResultPersistedEvent(BaseModel):
    """Published when a generation result has been persisted."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    result_id: uuid.UUID
    status: str = "completed"
    webhook_url: str | None = None
