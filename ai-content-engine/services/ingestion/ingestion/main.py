"""FastAPI application factory for the Ingestion Service."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from shared.database import init_database
from shared.kafka import AsyncKafkaProducer
from shared.logging import setup_logging
from shared.middleware.correlation import CorrelationIDMiddleware
from shared.middleware.error_handler import register_error_handlers

from ingestion.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging(settings.service_name, settings.log_level, settings.environment)
    init_database(settings.database_url, settings.database_pool_size, settings.database_max_overflow)

    producer = AsyncKafkaProducer(settings.kafka_bootstrap_servers)
    await producer.start()
    app.state.kafka_producer = producer

    yield

    await producer.stop()


app = FastAPI(
    title="AI Content Engine - Ingestion Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(CorrelationIDMiddleware)
register_error_handlers(app)

from ingestion.api.v1 import generations, templates, schemas, health  # noqa: E402

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(generations.router, prefix="/api/v1", tags=["generations"])
app.include_router(templates.router, prefix="/api/v1", tags=["templates"])
app.include_router(schemas.router, prefix="/api/v1", tags=["schemas"])
