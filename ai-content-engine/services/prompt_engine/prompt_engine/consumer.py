"""Kafka consumer handler for input.received events."""

import structlog

from shared.database import get_session
from shared.events.envelope import EventEnvelope
from shared.events.input_events import InputReceivedEvent
from shared.events.prompt_events import PromptAssembledEvent
from shared.models.template import PromptTemplate

from prompt_engine.services.template_compiler import TemplateCompiler
from prompt_engine.services.prompt_assembler import PromptAssembler

logger = structlog.get_logger(__name__)

compiler = TemplateCompiler()
assembler = PromptAssembler()


async def handle_input_received(message: dict) -> None:
    envelope = EventEnvelope(**message)
    event = InputReceivedEvent(**envelope.payload)

    logger.info(
        "processing_input_received",
        request_id=str(event.request_id),
        correlation_id=str(event.correlation_id),
        template_id=str(event.template_id),
    )

    async for session in get_session():
        template = await session.get(PromptTemplate, event.template_id)
        if template is None:
            logger.error("template_not_found", template_id=str(event.template_id))
            return

        system_prompt = compiler.render(template.system_prompt, event.parameters)
        user_prompt = compiler.render(template.user_prompt, event.parameters)

        assembled = assembler.assemble(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            few_shot_examples=template.few_shot_examples,
        )

        prompt_event = PromptAssembledEvent(
            request_id=event.request_id,
            correlation_id=event.correlation_id,
            template_id=event.template_id,
            template_version=template.version,
            system_prompt=assembled["system_prompt"],
            user_prompt=assembled["user_prompt"],
            model_requirements=event.options.get("model_requirements", {}),
            content_hash=template.content_hash,
        )

        out_envelope = EventEnvelope(
            event_type="prompt.assembled",
            correlation_id=event.correlation_id,
            source_service="prompt_engine",
            payload=prompt_event.model_dump(mode="json"),
        )

        from prompt_engine.main import producer
        if producer:
            await producer.send(
                "content.prompt.assembled",
                value=out_envelope.to_kafka_value(),
                key=out_envelope.kafka_key,
            )

        logger.info("prompt_assembled", request_id=str(event.request_id))
