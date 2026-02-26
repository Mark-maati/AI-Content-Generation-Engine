"""Async Kafka consumer wrapper with graceful shutdown."""

import asyncio
import json
from collections.abc import Awaitable, Callable

import structlog
from aiokafka import AIOKafkaConsumer

logger = structlog.get_logger(__name__)

MessageHandler = Callable[[dict], Awaitable[None]]


class AsyncKafkaConsumer:
    """Async Kafka consumer with manual commit and graceful shutdown."""

    def __init__(
        self,
        topic: str,
        bootstrap_servers: str,
        group_id: str,
        handler: MessageHandler,
    ) -> None:
        self._topic = topic
        self._bootstrap_servers = bootstrap_servers
        self._group_id = group_id
        self._handler = handler
        self._consumer: AIOKafkaConsumer | None = None
        self._running = False

    async def start(self) -> None:
        self._consumer = AIOKafkaConsumer(
            self._topic,
            bootstrap_servers=self._bootstrap_servers,
            group_id=self._group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            enable_auto_commit=False,
            auto_offset_reset="earliest",
        )
        await self._consumer.start()
        self._running = True
        logger.info(
            "kafka_consumer_started",
            topic=self._topic,
            group_id=self._group_id,
        )

    async def stop(self) -> None:
        self._running = False
        if self._consumer:
            await self._consumer.stop()
            logger.info("kafka_consumer_stopped", topic=self._topic)

    async def run(self) -> None:
        if not self._consumer:
            raise RuntimeError("Consumer not started. Call start() first.")

        try:
            async for message in self._consumer:
                if not self._running:
                    break
                try:
                    logger.info(
                        "kafka_message_received",
                        topic=message.topic,
                        partition=message.partition,
                        offset=message.offset,
                    )
                    await self._handler(message.value)
                    await self._consumer.commit()
                except Exception:
                    logger.exception(
                        "kafka_message_processing_failed",
                        topic=message.topic,
                        offset=message.offset,
                    )
        except asyncio.CancelledError:
            logger.info("kafka_consumer_cancelled", topic=self._topic)
        finally:
            await self.stop()
