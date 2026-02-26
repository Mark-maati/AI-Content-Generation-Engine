"""Prompt assembly events."""

import uuid

from pydantic import BaseModel, Field


class PromptAssembledEvent(BaseModel):
    """Published when a prompt has been assembled from template + parameters."""

    request_id: uuid.UUID
    correlation_id: uuid.UUID
    template_id: uuid.UUID
    template_version: str
    system_prompt: str
    user_prompt: str
    model_requirements: dict = Field(default_factory=dict)
    estimated_input_tokens: int = 0
    content_hash: str = ""
