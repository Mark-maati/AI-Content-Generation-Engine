"""Template rendering and assembly service."""

import json
from typing import Any

import structlog
from jinja2 import Template

logger = structlog.get_logger(__name__)


def truncate_filter(text: str, max_tokens: int) -> str:
    """Mock truncate filter to limit tokens."""
    # Actual implementation would use tiktoken/provider tokenizer
    if len(text) > max_tokens * 4: # rough approximation
        return text[:max_tokens * 4] + "..."
    return text


class TemplateService:
    """Renders Prompt Templates with Jinja2 combining system and user prompts."""

    def __init__(self) -> None:
        pass

    async def assemble_prompt(
        self,
        template_id: str,
        template_version: str | None,
        parameters: dict[str, Any],
    ) -> dict[str, str]:
        """Fetch template from DB and render with parameters."""
        logger.debug("assembling_prompt", template=template_id, version=template_version)
        
        # In a real scenario, this fetches from the DB using a Repository
        # Mocking the template retrieval for the sake of the exercise
        system_prompt_raw = "You are a helpful AI assistant. {{ optional_instructions }}"
        user_prompt_raw = "Process this text: {{ text | truncate(1000) }}"
        
        sys_template = Template(system_prompt_raw)
        sys_template.environment.filters["truncate"] = truncate_filter
        
        user_template = Template(user_prompt_raw)
        user_template.environment.filters["truncate"] = truncate_filter
        
        try:
            rendered_system = sys_template.render(**parameters)
            rendered_user = user_template.render(**parameters)
            
            return {
                "system_prompt": rendered_system,
                "user_prompt": rendered_user
            }
        except Exception as e:
            logger.error("template_rendering_failed", error=str(e))
            raise ValueError(f"Failed to render template: {e}") from e

