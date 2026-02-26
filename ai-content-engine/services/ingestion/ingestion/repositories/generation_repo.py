"""Generation request repository."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import NotFoundError
from shared.models.generation import GenerationRequest


class GenerationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, request: GenerationRequest) -> GenerationRequest:
        self._session.add(request)
        await self._session.flush()
        return request

    async def get_by_id(self, request_id: uuid.UUID) -> GenerationRequest:
        result = await self._session.get(GenerationRequest, request_id)
        if result is None:
            raise NotFoundError(
                message=f"Generation request {request_id} not found",
                code="GENERATION_NOT_FOUND",
            )
        return result

    async def list_by_org(
        self, organization_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[GenerationRequest], int]:
        base = select(GenerationRequest).where(
            GenerationRequest.organization_id == organization_id,
            GenerationRequest.deleted_at.is_(None),
        )
        count_result = await self._session.execute(
            select(func.count()).select_from(base.subquery())
        )
        total = count_result.scalar_one()

        result = await self._session.execute(
            base.order_by(GenerationRequest.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars().all()), total
