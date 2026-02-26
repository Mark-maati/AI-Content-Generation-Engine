import structlog
from shared.events.envelope import EventEnvelope
from shared.kafka.producer import AsyncKafkaProducer
from output_validation.services.validation_service import ValidationService

from pydantic import BaseModel

logger = structlog.get_logger(__name__)

VALIDATION_COMPLETE_TOPIC = "content.validation.complete"

class GenerationCompletePayload(BaseModel):
    request_id: str
    raw_response: str
    schema_id: str | None = None
    timing_ms: dict | None = None

async def handle_generation_complete(msg: dict, producer: AsyncKafkaProducer, validator: ValidationService) -> None:
    """Handle incoming GenerationComplete events, run validation, and publish ValidationComplete."""
    logger.info("received_generation_complete_event", event_id=msg.get("event_id"))
    
    try:
        # Schema Validation Boundary Layer
        payload = GenerationCompletePayload.model_validate(msg.get("payload", {}))
        raw_response = payload.raw_response
        request_id = payload.request_id
        schema_id = payload.schema_id
    except Exception as e:
        logger.error("invalid_event_payload", error=str(e), event_id=msg.get("event_id"))
        return

    try:
        # Step 1 & 2: Parse and Validate
        parsed_data = await validator.validate_output(raw_response, schema_id)
        
        # Step 3: Publish ValidationComplete Success
        event_payload = {
            "request_id": request_id,
            "status": "success",
            "parsed_output": parsed_data,
            "raw_response": raw_response,
            "timing_ms": payload.timing_ms or {}
        }
    except Exception as e:
        logger.error("validation_failed", error=str(e), request_id=request_id)
        # Step 3: Publish ValidationComplete Error
        event_payload = {
            "request_id": request_id,
            "status": "failed",
            "error_message": str(e),
            "raw_response": raw_response
        }

    envelope = EventEnvelope(
        event_type="validation.complete",
        correlation_id=msg.get("correlation_id"),
        source_service="output_validation",
        payload=event_payload,
    )

    await producer.send(
        VALIDATION_COMPLETE_TOPIC,
        value=envelope.to_kafka_value(),
        key=envelope.kafka_key,
    )
