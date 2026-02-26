"""Output schema repository."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from shared.exceptions import NotFoundError
from shared.models.schema import OutputSchema


class SchemaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, schema: OutputSchema) -> OutputSchema:
        self._session.add(schema)
        await self._session.flush()
        return schema

    async def get_by_id(self, schema_id: uuid.UUID) -> OutputSchema:
        result = await self._session.get(OutputSchema, schema_id)
        if result is None:
            raise NotFoundError(
                message=f"Schema {schema_id} not found",
                code="SCHEMA_NOT_FOUND",
            )
        return result

    async def update(self, schema: OutputSchema) -> OutputSchema:
        await self._session.flush()
        return schema
