"""Prompt template repository."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import NotFoundError
from shared.models.template import PromptTemplate


class TemplateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, template: PromptTemplate) -> PromptTemplate:
        self._session.add(template)
        await self._session.flush()
        return template

    async def get_by_id(self, template_id: uuid.UUID) -> PromptTemplate:
        result = await self._session.get(PromptTemplate, template_id)
        if result is None:
            raise NotFoundError(
                message=f"Template {template_id} not found",
                code="TEMPLATE_NOT_FOUND",
            )
        return result

    async def update(self, template: PromptTemplate) -> PromptTemplate:
        await self._session.flush()
        return template

    async def list_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[PromptTemplate], int]:
        base = select(PromptTemplate).where(PromptTemplate.deleted_at.is_(None))
        count_result = await self._session.execute(
            select(func.count()).select_from(base.subquery())
        )
        total = count_result.scalar_one()

        result = await self._session.execute(
            base.order_by(PromptTemplate.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars().all()), total
