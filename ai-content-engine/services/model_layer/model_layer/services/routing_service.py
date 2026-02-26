"""Routing policy logic for the LLM Model Layer."""

import random
from typing import Any

import structlog

from shared.models.generation import GenerationRequest, RequestPriority

logger = structlog.get_logger(__name__)


class RoutingService:
    """Intelligent Model Selection and Routing Engine."""

    def __init__(self, provider_registry: dict[str, Any]) -> None:
        self.registry = provider_registry

    async def select_model(self, request: GenerationRequest) -> tuple[str, str]:
        """
        Determine the most appropriate LLM provider and model alias
        based on cost, complexity, and latency configurations as per the ECC Cost-Aware pattern.
        """
        # Determine task complexity implicitly derived from options/parameters.
        options = request.options or {}
        max_tokens = options.get("max_tokens", 500)
        priority = request.priority

        # Simple thresholding logic based on PRD cost routing
        # Critical tasks (forced by config -> Opus)
        if priority == RequestPriority.HIGH:
            return "anthropic", "claude-3-opus-20240229"

        # Complex tasks -> Sonnet
        if max_tokens > 2000 or options.get("complex", False):
            return "anthropic", "claude-3-5-sonnet-20240620"

        # Simple tasks -> Haiku (Fallback)
        # Using A/B traffic split logic for Gemini vs Haiku demonstration on simple queries
        if random.random() > 0.5:
            return "google", "gemini-1.5-flash"
        return "anthropic", "claude-3-haiku-20240307"

