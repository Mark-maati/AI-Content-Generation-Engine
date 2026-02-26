"""Output schema business logic."""

import uuid

from shared.models.schema import OutputSchema

from ingestion.repositories.schema_repo import SchemaRepository
from ingestion.schemas.schema_schemas import OutputSchemaCreate, OutputSchemaUpdate


class SchemaService:
    def __init__(self, repo: SchemaRepository) -> None:
        self._repo = repo

    async def create(self, data: OutputSchemaCreate) -> OutputSchema:
        schema = OutputSchema(
            name=data.name,
            json_schema=data.json_schema,
            semantic_rules=data.semantic_rules,
            quality_rules=data.quality_rules,
        )
        return await self._repo.create(schema)

    async def get_by_id(self, schema_id: uuid.UUID) -> OutputSchema:
        return await self._repo.get_by_id(schema_id)

    async def update(self, schema_id: uuid.UUID, data: OutputSchemaUpdate) -> OutputSchema:
        schema = await self._repo.get_by_id(schema_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(schema, field, value)
        return await self._repo.update(schema)
