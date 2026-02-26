"""Pydantic schemas for prompt templates."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TemplateCreate(BaseModel):
    name: str
    system_prompt: str
    user_prompt: str
    few_shot_examples: dict | None = None
    metadata: dict = Field(default_factory=dict)
    parent_template_id: uuid.UUID | None = None


class TemplateUpdate(BaseModel):
    name: str | None = None
    system_prompt: str | None = None
    user_prompt: str | None = None
    few_shot_examples: dict | None = None
    metadata: dict | None = None
    status: str | None = None


class TemplateResponse(BaseModel):
    id: uuid.UUID
    name: str
    version: str
    status: str
    content_hash: str
    parent_template_id: uuid.UUID | None = None
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TemplateDetailResponse(TemplateResponse):
    system_prompt: str
    user_prompt: str
    few_shot_examples: dict | None = None
    metadata_: dict = Field(default_factory=dict, alias="metadata_")
