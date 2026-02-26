"""Custom Jinja2 filters for prompt templates."""

import json

from jinja2 import Environment


def truncate_tokens(text: str, max_tokens: int = 1000) -> str:
    words = text.split()
    estimated_tokens = len(words) * 1.3
    if estimated_tokens <= max_tokens:
        return text
    target_words = int(max_tokens / 1.3)
    return " ".join(words[:target_words]) + "..."


def format_json(value: dict | list, indent: int = 2) -> str:
    return json.dumps(value, indent=indent, ensure_ascii=False)


def if_section(value: str | None, label: str = "") -> str:
    if not value:
        return ""
    if label:
        return f"\n## {label}\n{value}\n"
    return f"\n{value}\n"


def register_filters(env: Environment) -> None:
    env.filters["truncate_tokens"] = truncate_tokens
    env.filters["format_json"] = format_json
    env.filters["if_section"] = if_section
