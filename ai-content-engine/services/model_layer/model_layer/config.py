"""Model layer service configuration."""

from shared.config import BaseServiceSettings


class ModelLayerSettings(BaseServiceSettings):
    service_name: str = "model_layer"
    kafka_consumer_group: str = "model-layer-group"
    input_topic: str = "content.prompt.assembled"
    output_topic: str = "content.generation.completed"
    host: str = "0.0.0.0"
    port: int = 8003
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_provider: str = "mock"
    default_model: str = "mock-model"
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60


settings = ModelLayerSettings()
