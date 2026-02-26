"""Pydantic schemas for output schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class OutputSchemaCreate(BaseModel):
    name: str
    json_schema: dict
    semantic_rules: dict | None = None
    quality_rules: dict | None = None


class OutputSchemaUpdate(BaseModel):
    name: str | None = None
    json_schema: dict | None = None
    semantic_rules: dict | None = None
    quality_rules: dict | None = None


class OutputSchemaResponse(BaseModel):
    id: uuid.UUID
    name: str
    version: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OutputSchemaDetailResponse(OutputSchemaResponse):
    json_schema: dict
    semantic_rules: dict | None = None
    quality_rules: dict | None = None
