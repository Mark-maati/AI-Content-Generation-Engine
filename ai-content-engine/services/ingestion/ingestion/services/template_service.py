"""Prompt template business logic."""

import hashlib
import uuid

from shared.models.template import PromptTemplate, TemplateStatus

from ingestion.repositories.template_repo import TemplateRepository
from ingestion.schemas.template_schemas import TemplateCreate, TemplateUpdate


class TemplateService:
    def __init__(self, repo: TemplateRepository) -> None:
        self._repo = repo

    def _compute_hash(self, system_prompt: str, user_prompt: str) -> str:
        content = f"{system_prompt}||{user_prompt}"
        return hashlib.sha256(content.encode()).hexdigest()

    async def create(self, data: TemplateCreate, created_by: uuid.UUID) -> PromptTemplate:
        content_hash = self._compute_hash(data.system_prompt, data.user_prompt)
        template = PromptTemplate(
            name=data.name,
            system_prompt=data.system_prompt,
            user_prompt=data.user_prompt,
            few_shot_examples=data.few_shot_examples,
            metadata_=data.metadata,
            content_hash=content_hash,
            created_by=created_by,
            parent_template_id=data.parent_template_id,
            status=TemplateStatus.DRAFT,
        )
        return await self._repo.create(template)

    async def get_by_id(self, template_id: uuid.UUID) -> PromptTemplate:
        return await self._repo.get_by_id(template_id)

    async def update(self, template_id: uuid.UUID, data: TemplateUpdate) -> PromptTemplate:
        template = await self._repo.get_by_id(template_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "metadata":
                setattr(template, "metadata_", value)
            elif field == "status" and value is not None:
                setattr(template, field, TemplateStatus(value))
            else:
                setattr(template, field, value)
        if "system_prompt" in update_data or "user_prompt" in update_data:
            template.content_hash = self._compute_hash(
                template.system_prompt, template.user_prompt
            )
        return await self._repo.update(template)

    async def list_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[PromptTemplate], int]:
        return await self._repo.list_all(page=page, page_size=page_size)
