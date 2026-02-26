"""Generation request business logic."""

import hashlib
import uuid

import structlog

from shared.events.envelope import EventEnvelope
from shared.events.input_events import InputReceivedEvent
from shared.kafka import AsyncKafkaProducer
from shared.models.generation import GenerationRequest, GenerationStatus, RequestMode, RequestPriority

from ingestion.repositories.generation_repo import GenerationRepository
from ingestion.schemas.generation_schemas import GenerationCreate

logger = structlog.get_logger(__name__)

INPUT_RECEIVED_TOPIC = "content.input.received"


class GenerationService:
    def __init__(self, repo: GenerationRepository, producer: AsyncKafkaProducer) -> None:
        self._repo = repo
        self._producer = producer

    async def create(
        self,
        data: GenerationCreate,
        user_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> GenerationRequest:
        correlation_id = uuid.uuid4()
        request = GenerationRequest(
            correlation_id=correlation_id,
            user_id=user_id,
            organization_id=organization_id,
            template_id=data.template_id,
            template_version=data.template_version,
            parameters=data.parameters,
            options=data.options,
            status=GenerationStatus.PENDING,
            mode=RequestMode(data.mode),
            priority=RequestPriority(data.priority),
        )
        request = await self._repo.create(request)

        event = InputReceivedEvent(
            request_id=request.id,
            correlation_id=correlation_id,
            user_id=user_id,
            organization_id=organization_id,
            template_id=data.template_id,
            template_version=data.template_version,
            parameters=data.parameters,
            options=data.options,
        )
        envelope = EventEnvelope(
            event_type="input.received",
            correlation_id=correlation_id,
            source_service="ingestion",
            payload=event.model_dump(mode="json"),
        )
        await self._producer.send(
            INPUT_RECEIVED_TOPIC,
            value=envelope.to_kafka_value(),
            key=envelope.kafka_key,
        )
        logger.info("generation_request_created", request_id=str(request.id), correlation_id=str(correlation_id))
        return request

    async def get_by_id(self, request_id: uuid.UUID) -> GenerationRequest:
        return await self._repo.get_by_id(request_id)

    async def list_by_org(
        self, organization_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[GenerationRequest], int]:
        return await self._repo.list_by_org(organization_id, page=page, page_size=page_size)
