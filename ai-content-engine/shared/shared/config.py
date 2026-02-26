"""Shared configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Base settings for all microservices."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 10
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_consumer_group: str = ""
    redis_url: str = "redis://localhost:6379/0"
    elasticsearch_url: str = "http://localhost:9200"
    jwt_secret: str = "dev-secret-change-in-production-minimum-32-chars"
    jwt_algorithm: str = "HS256"
    log_level: str = "INFO"
    environment: str = "development"
    service_name: str = ""
