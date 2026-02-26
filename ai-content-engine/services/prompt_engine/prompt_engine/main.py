"""Prompt Engine application entry point."""

import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
import uvicorn

from shared.database import init_database
from shared.kafka import AsyncKafkaConsumer, AsyncKafkaProducer
from shared.logging import setup_logging
from shared.middleware.correlation import CorrelationIDMiddleware
from shared.middleware.error_handler import register_error_handlers

from prompt_engine.config import settings
from prompt_engine.consumer import handle_input_received


producer: AsyncKafkaProducer | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global producer
    setup_logging(settings.service_name, settings.log_level, settings.environment)
    init_database(settings.database_url, settings.database_pool_size, settings.database_max_overflow)

    producer = AsyncKafkaProducer(settings.kafka_bootstrap_servers)
    await producer.start()
    app.state.kafka_producer = producer

    consumer = AsyncKafkaConsumer(
        topic=settings.input_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_consumer_group,
        handler=handle_input_received,
    )
    await consumer.start()
    consumer_task = asyncio.create_task(consumer.run())

    yield

    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    await producer.stop()


app = FastAPI(
    title="AI Content Engine - Prompt Engine",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(CorrelationIDMiddleware)
register_error_handlers(app)

from prompt_engine.api.v1 import health  # noqa: E402
app.include_router(health.router, prefix="/api/v1", tags=["health"])


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
