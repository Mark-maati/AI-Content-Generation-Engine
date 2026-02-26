"""Base Provider Abstraction Interface."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ProviderCapabilities(BaseModel):
    modalities: list[str]
    context_window_size: int
    output_format_support: list[str]
    specialized_skills: list[str]


class GenerationResult(BaseModel):
    raw_response: str
    tokens_used: int
    cost_estimated: float


class LLMProvider(ABC):
    """Abstract interface for all language model providers."""

    @abstractmethod
    async def get_capabilities(self) -> ProviderCapabilities:
        """Return the capabilities supported by this provider."""
        pass

    @abstractmethod
    async def generate(self, model_id: str, prompt: str, parameters: dict[str, Any]) -> GenerationResult:
        """Submit a generation request to the provider."""
        pass

    @abstractmethod
    async def estimate_tokens(self, text: str) -> int:
        """Estimate the token count prior to submission."""
        pass

