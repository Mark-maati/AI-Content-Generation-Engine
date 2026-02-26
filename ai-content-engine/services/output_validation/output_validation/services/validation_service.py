"""Output Parsing and Validation business logic."""

import json
import re
from typing import Any

import structlog
from jsonschema import validate
from jsonschema.exceptions import ValidationError

logger = structlog.get_logger(__name__)


def extract_json(raw_text: str) -> dict[str, Any]:
    """Pass 1 and 2: Direct Parsing and Regex Markdown Extraction."""
    try:
        # Pass 1: Direct JSON parsing
        return json.loads(raw_text)
    except json.JSONDecodeError:
        logger.debug("direct_json_parse_failed, trying_regex")

    # Pass 2: Extract from Markdown code blocks
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Pass 3: In an actual implementation, issue a 'Repair Model Invocation'
    raise ValueError("Failed to extract valid JSON from LLM response")


class ValidationService:
    """Service to validate structured data against JSON schemas and semantic rules."""

    def __init__(self) -> None:
        # Simulating external schema registry retrieval
        self.schemas: dict[str, dict[str, Any]] = {}

    def register_schema(self, schema_id: str, schema_def: dict[str, Any]) -> None:
        self.schemas[schema_id] = schema_def

    async def validate_output(self, raw_output: str, schema_id: str | None) -> dict[str, Any]:
        """Parse raw text to structured format and validate against registered rules."""
        parsed_data = extract_json(raw_output)

        if not schema_id:
            # Flexible validation if no explicit schema provided
            return parsed_data

        schema = self.schemas.get(schema_id)
        if not schema:
            logger.warning("schema_not_found", schema_id=schema_id)
            return parsed_data

        try:
            # Stage 1 - Syntactic Validation
            validate(instance=parsed_data, schema=schema)
            # Future: Stage 2 - Semantic Validation (custom Javascript evaluation sandbox)
            # Future: Stage 3 - Quality Validation
            return parsed_data
        except ValidationError as e:
            logger.error("output_validation_failed", error=str(e))
            raise ValueError(f"Output failed syntactic validation: {e.message}") from e

