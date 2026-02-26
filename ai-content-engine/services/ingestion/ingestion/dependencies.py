"""Dependency injection for the Ingestion Service."""

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import get_session
from shared.kafka import AsyncKafkaProducer
from shared.middleware.auth import JWTAuthMiddleware

from ingestion.config import settings
from ingestion.repositories.generation_repo import GenerationRepository
from ingestion.repositories.template_repo import TemplateRepository
from ingestion.repositories.schema_repo import SchemaRepository
from ingestion.services.generation_service import GenerationService
from ingestion.services.template_service import TemplateService
from ingestion.services.schema_service import SchemaService

auth = JWTAuthMiddleware(secret=settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_kafka_producer(request: Request) -> AsyncKafkaProducer:
    return request.app.state.kafka_producer


def get_generation_repo(session: AsyncSession = Depends(get_session)) -> GenerationRepository:
    return GenerationRepository(session)


def get_template_repo(session: AsyncSession = Depends(get_session)) -> TemplateRepository:
    return TemplateRepository(session)


def get_schema_repo(session: AsyncSession = Depends(get_session)) -> SchemaRepository:
    return SchemaRepository(session)


def get_generation_service(
    repo: GenerationRepository = Depends(get_generation_repo),
    producer: AsyncKafkaProducer = Depends(get_kafka_producer),
) -> GenerationService:
    return GenerationService(repo, producer)


def get_template_service(
    repo: TemplateRepository = Depends(get_template_repo),
) -> TemplateService:
    return TemplateService(repo)


def get_schema_service(
    repo: SchemaRepository = Depends(get_schema_repo),
) -> SchemaService:
    return SchemaService(repo)
