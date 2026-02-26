"""Kafka consumer for PromptAssembled events."""

import structlog

from shared.events.envelope import EventEnvelope
from shared.kafka.producer import AsyncKafkaProducer
from model_layer.services.routing_service import RoutingService
# Replace with actual provider factory
from model_layer.providers.base import LLMProvider
from shared.models.generation import GenerationRequest
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

GENERATION_COMPLETE_TOPIC = "content.generation.complete"

class PromptAssembledPayload(BaseModel):
    request_id: str
    system_prompt: str
    user_prompt: str
    priority: str = "normal"
    options: dict = {}
    parameters: dict = {}
    schema_id: str | None = None

async def handle_prompt_assembled(
    msg: dict, 
    producer: AsyncKafkaProducer, 
    router: RoutingService,
    provider_registry: dict[str, LLMProvider]
) -> None:
    """Handle PromptAssembled event, invoke LLM, publish GenerationComplete."""
    logger.info("received_prompt_assembled_event", event_id=msg.get("event_id"))
    
    try:
        payload = PromptAssembledPayload.model_validate(msg.get("payload", {}))
        request_id = payload.request_id
        system_prompt = payload.system_prompt
        user_prompt = payload.user_prompt
    except Exception as e:
        logger.error("invalid_event_payload_schema", error=str(e), event_id=msg.get("event_id"))
        return
        
    # Mocking request object construction from dict for routing
    request = GenerationRequest(
        priority=payload.priority,
        options=payload.options
    )

    try:
        provider_name, model_id = await router.select_model(request)
        provider = provider_registry.get(provider_name)
        
        if not provider:
            raise ValueError(f"Provider {provider_name} not found")
            
        full_prompt = f"{system_prompt}\n{user_prompt}"
        
        result = await provider.generate(
            model_id=model_id,
            prompt=full_prompt,
            parameters=payload.parameters
        )
        
        event_payload = {
            "request_id": request_id,
            "status": "success",
            "raw_response": result.raw_response,
            "tokens_used": result.tokens_used,
            "cost_estimated": result.cost_estimated,
            "schema_id": payload.schema_id,
            "timing_ms": {"inference": 100} # Mock timing
        }
        
    except Exception as e:
        logger.error("model_generation_failed", error=str(e), request_id=request_id)
        event_payload = {
            "request_id": request_id,
            "status": "failed",
            "error_message": str(e)
        }

    envelope = EventEnvelope(
        event_type="generation.complete",
        correlation_id=msg.get("correlation_id"),
        source_service="model_layer",
        payload=event_payload,
    )

    await producer.send(
        GENERATION_COMPLETE_TOPIC,
        value=envelope.to_kafka_value(),
        key=envelope.kafka_key,
    )
