"""Pydantic schemas for generation requests and responses."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class GenerationCreate(BaseModel):
    template_id: uuid.UUID
    template_version: str | None = None
    parameters: dict = Field(default_factory=dict)
    options: dict = Field(default_factory=dict)
    mode: str = "async"
    priority: str = "normal"


class GenerationResponse(BaseModel):
    id: uuid.UUID
    correlation_id: uuid.UUID
    status: str
    mode: str
    priority: str
    template_id: uuid.UUID
    template_version: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class GenerationDetailResponse(GenerationResponse):
    parameters: dict = Field(default_factory=dict)
    options: dict = Field(default_factory=dict)
    user_id: uuid.UUID
    organization_id: uuid.UUID
    project_id: uuid.UUID | None = None
