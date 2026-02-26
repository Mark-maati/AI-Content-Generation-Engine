"""Prompt engine service configuration."""

from shared.config import BaseServiceSettings


class PromptEngineSettings(BaseServiceSettings):
    service_name: str = "prompt_engine"
    kafka_consumer_group: str = "prompt-engine-group"
    input_topic: str = "content.input.received"
    output_topic: str = "content.prompt.assembled"
    host: str = "0.0.0.0"
    port: int = 8002
    template_cache_ttl: int = 3600


settings = PromptEngineSettings()
