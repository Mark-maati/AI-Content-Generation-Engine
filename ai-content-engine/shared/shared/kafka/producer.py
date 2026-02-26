"""Async Kafka producer wrapper."""

import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from aiokafka import AIOKafkaProducer

logger = structlog.get_logger(__name__)


class AsyncKafkaProducer:
    """Async Kafka producer with JSON serialization."""

    def __init__(self, bootstrap_servers: str) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
            acks="all",
            enable_idempotence=True,
        )
        await self._producer.start()
        logger.info("kafka_producer_started", servers=self._bootstrap_servers)

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()
            logger.info("kafka_producer_stopped")

    async def send(self, topic: str, value: dict, key: str | None = None) -> None:
        if not self._producer:
            raise RuntimeError("Producer not started. Call start() first.")
        await self._producer.send_and_wait(topic, value=value, key=key)
        logger.debug("kafka_message_sent", topic=topic, key=key)

    @asynccontextmanager
    async def lifespan(self) -> AsyncGenerator[None, None]:
        await self.start()
        try:
            yield
        finally:
            await self.stop()
