"""Datetime utility helpers."""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current UTC datetime with timezone info."""
    return datetime.now(timezone.utc)
