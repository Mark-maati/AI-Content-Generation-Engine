"""Prompt template API endpoints."""

import uuid

from fastapi import APIRouter, Depends

from shared.schemas.responses import DataResponse, PaginatedResponse

from ingestion.dependencies import auth, get_template_service
from ingestion.schemas.template_schemas import (
    TemplateCreate,
    TemplateDetailResponse,
    TemplateResponse,
    TemplateUpdate,
)
from ingestion.services.template_service import TemplateService

router = APIRouter()


@router.post("/templates", response_model=DataResponse[TemplateResponse], status_code=201)
async def create_template(
    body: TemplateCreate,
    token_payload: dict = Depends(auth),
    service: TemplateService = Depends(get_template_service),
) -> DataResponse[TemplateResponse]:
    user_id = uuid.UUID(token_payload["sub"])
    result = await service.create(body, created_by=user_id)
    return DataResponse(data=TemplateResponse.model_validate(result))


@router.get("/templates/{template_id}", response_model=DataResponse[TemplateDetailResponse])
async def get_template(
    template_id: uuid.UUID,
    token_payload: dict = Depends(auth),
    service: TemplateService = Depends(get_template_service),
) -> DataResponse[TemplateDetailResponse]:
    result = await service.get_by_id(template_id)
    return DataResponse(data=TemplateDetailResponse.model_validate(result))


@router.patch("/templates/{template_id}", response_model=DataResponse[TemplateResponse])
async def update_template(
    template_id: uuid.UUID,
    body: TemplateUpdate,
    token_payload: dict = Depends(auth),
    service: TemplateService = Depends(get_template_service),
) -> DataResponse[TemplateResponse]:
    result = await service.update(template_id, body)
    return DataResponse(data=TemplateResponse.model_validate(result))


@router.get("/templates", response_model=PaginatedResponse[TemplateResponse])
async def list_templates(
    page: int = 1,
    page_size: int = 20,
    token_payload: dict = Depends(auth),
    service: TemplateService = Depends(get_template_service),
) -> PaginatedResponse[TemplateResponse]:
    items, total = await service.list_all(page=page, page_size=page_size)
    from shared.schemas.responses import PaginationMeta
    return PaginatedResponse(
        data=[TemplateResponse.model_validate(i) for i in items],
        meta=PaginationMeta(
            page=page, page_size=page_size, total_items=total,
            total_pages=(total + page_size - 1) // page_size,
        ),
    )
