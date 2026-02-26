"""Output schema API endpoints."""

import uuid

from fastapi import APIRouter, Depends

from shared.schemas.responses import DataResponse

from ingestion.dependencies import auth, get_schema_service
from ingestion.schemas.schema_schemas import (
    OutputSchemaCreate,
    OutputSchemaDetailResponse,
    OutputSchemaResponse,
    OutputSchemaUpdate,
)
from ingestion.services.schema_service import SchemaService

router = APIRouter()


@router.post("/schemas", response_model=DataResponse[OutputSchemaResponse], status_code=201)
async def create_schema(
    body: OutputSchemaCreate,
    token_payload: dict = Depends(auth),
    service: SchemaService = Depends(get_schema_service),
) -> DataResponse[OutputSchemaResponse]:
    result = await service.create(body)
    return DataResponse(data=OutputSchemaResponse.model_validate(result))


@router.get("/schemas/{schema_id}", response_model=DataResponse[OutputSchemaDetailResponse])
async def get_schema(
    schema_id: uuid.UUID,
    token_payload: dict = Depends(auth),
    service: SchemaService = Depends(get_schema_service),
) -> DataResponse[OutputSchemaDetailResponse]:
    result = await service.get_by_id(schema_id)
    return DataResponse(data=OutputSchemaDetailResponse.model_validate(result))


@router.patch("/schemas/{schema_id}", response_model=DataResponse[OutputSchemaResponse])
async def update_schema(
    schema_id: uuid.UUID,
    body: OutputSchemaUpdate,
    token_payload: dict = Depends(auth),
    service: SchemaService = Depends(get_schema_service),
) -> DataResponse[OutputSchemaResponse]:
    result = await service.update(schema_id, body)
    return DataResponse(data=OutputSchemaResponse.model_validate(result))
