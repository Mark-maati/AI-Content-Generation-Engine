"""Storage service for persisting Generation Results."""

import uuid
from typing import Any

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.generation import GenerationRequest, GenerationResult, GenerationStatus

logger = structlog.get_logger(__name__)


class StorageService:
    """Handles insertions of Generation Results into PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def store_result(self, request_id: uuid.UUID, event_payload: dict[str, Any]) -> None:
        """Update request status and create result record."""
        # 1. Update the Request Status
        request = await self.session.get(GenerationRequest, request_id)
        if not request:
            logger.error("generation_request_not_found", request_id=str(request_id))
            return

        status_str = event_payload.get("status")
        if status_str == "success":
            request.status = GenerationStatus.COMPLETED
            
            # 2. Store the Generation Result Context
            result = GenerationResult(
                request_id=request_id,
                raw_response=event_payload.get("raw_response", ""),
                parsed_output=event_payload.get("parsed_output", {}),
                validation_results={"status": "passed"},
                token_usage={}, # To be populated by model layer in future
                cost_usd=0.0,
                latency_ms=event_payload.get("timing_ms", {}),
            )
            self.session.add(result)
            
        else:
            request.status = GenerationStatus.FAILED
            # Handle failure storing details...

        await self.session.commit()
        logger.info("generation_result_stored", request_id=str(request_id), status=status_str)

