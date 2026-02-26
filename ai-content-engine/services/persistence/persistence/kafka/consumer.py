"""Kafka consumer for ValidationComplete events."""

import structlog

from persistence.services.storage_service import StorageService
from pydantic import BaseModel, UUID4

logger = structlog.get_logger(__name__)

class ValidationCompletePayload(BaseModel):
    request_id: UUID4
    status: str
    parsed_output: dict | None = None
    raw_response: str
    error_message: str | None = None
    timing_ms: dict | None = None

async def handle_validation_complete(
    msg: dict, 
    storage_service: StorageService
) -> None:
    """Handle ValidationComplete event and store result."""
    logger.info("received_validation_complete_event", event_id=msg.get("event_id"))
    
    try:
        payload = ValidationCompletePayload.model_validate(msg.get("payload", {}))
        request_id_str = str(payload.request_id)
    except Exception as e:
        logger.error("invalid_event_payload_schema", error=str(e), event_id=msg.get("event_id"))
        return
        
    try:
        request_id = payload.request_id
        await storage_service.store_result(request_id, payload.model_dump())
        
        # In a complete implementation, this would also index to Elasticsearch
        # es_client.index(index="generation_results", id=str(request_id), document=payload)
        
    except Exception as e:
        logger.error("persistence_failed", error=str(e), request_id=request_id_str)
