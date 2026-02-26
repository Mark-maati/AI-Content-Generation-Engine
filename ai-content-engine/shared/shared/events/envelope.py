"""Event envelope for all Kafka events."""

import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """Standard envelope wrapping all Kafka events."""

    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    event_type: str
    correlation_id: uuid.UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_service: str
    payload: dict

    def to_kafka_value(self) -> dict:
        return self.model_dump(mode="json")

    @property
    def kafka_key(self) -> str:
        return str(self.correlation_id)
