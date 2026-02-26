"""Model generation events."""

import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class GenerationCompletedEvent(BaseModel):
    """Published when model inference completes successfully."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    model_provider: str
    model_id: str
    model_version: str | None = None
    raw_response: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: Decimal = Decimal("0")
    latency_ms: int = 0


class GenerationFailedEvent(BaseModel):
    """Published when model inference fails after retries."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    error_code: str
    error_message: str
    provider: str
    attempts: int = 1
