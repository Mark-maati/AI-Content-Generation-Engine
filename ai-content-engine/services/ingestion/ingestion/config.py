"""Ingestion service configuration."""

from shared.config import BaseServiceSettings


class IngestionSettings(BaseServiceSettings):
    service_name: str = "ingestion"
    kafka_consumer_group: str = "ingestion-group"
    host: str = "0.0.0.0"
    port: int = 8001


settings = IngestionSettings()
