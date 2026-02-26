"""Generation request API endpoints."""

import uuid

from fastapi import APIRouter, Depends

from shared.schemas.responses import DataResponse, PaginatedResponse

from ingestion.dependencies import auth, get_generation_service
from ingestion.schemas.generation_schemas import (
    GenerationCreate,
    GenerationDetailResponse,
    GenerationResponse,
)
from ingestion.services.generation_service import GenerationService

router = APIRouter()


@router.post("/generations", response_model=DataResponse[GenerationResponse], status_code=201)
async def create_generation(
    body: GenerationCreate,
    token_payload: dict = Depends(auth),
    service: GenerationService = Depends(get_generation_service),
) -> DataResponse[GenerationResponse]:
    user_id = uuid.UUID(token_payload["sub"])
    org_id = uuid.UUID(token_payload["org_id"])
    result = await service.create(body, user_id=user_id, organization_id=org_id)
    return DataResponse(data=GenerationResponse.model_validate(result))


@router.get("/generations/{generation_id}", response_model=DataResponse[GenerationDetailResponse])
async def get_generation(
    generation_id: uuid.UUID,
    token_payload: dict = Depends(auth),
    service: GenerationService = Depends(get_generation_service),
) -> DataResponse[GenerationDetailResponse]:
    result = await service.get_by_id(generation_id)
    return DataResponse(data=GenerationDetailResponse.model_validate(result))


@router.get("/generations", response_model=PaginatedResponse[GenerationResponse])
async def list_generations(
    page: int = 1,
    page_size: int = 20,
    token_payload: dict = Depends(auth),
    service: GenerationService = Depends(get_generation_service),
) -> PaginatedResponse[GenerationResponse]:
    org_id = uuid.UUID(token_payload["org_id"])
    items, total = await service.list_by_org(org_id, page=page, page_size=page_size)
    from shared.schemas.responses import PaginationMeta
    return PaginatedResponse(
        data=[GenerationResponse.model_validate(i) for i in items],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=(total + page_size - 1) // page_size,
        ),
    )
