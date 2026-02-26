"""Redis-backed content-addressable template cache."""

import hashlib
import json

import structlog
from redis.asyncio import Redis

logger = structlog.get_logger(__name__)


class TemplateCache:
    """Cache rendered templates using content-addressable hashing."""

    def __init__(self, redis: Redis, ttl: int = 3600) -> None:
        self._redis = redis
        self._ttl = ttl

    def _make_key(self, template_hash: str, parameters: dict) -> str:
        param_hash = hashlib.sha256(
            json.dumps(parameters, sort_keys=True).encode()
        ).hexdigest()[:16]
        return f"prompt_cache:{template_hash}:{param_hash}"

    async def get(self, template_hash: str, parameters: dict) -> str | None:
        key = self._make_key(template_hash, parameters)
        result = await self._redis.get(key)
        if result:
            logger.debug("template_cache_hit", key=key)
            return result.decode("utf-8")
        logger.debug("template_cache_miss", key=key)
        return None

    async def set(self, template_hash: str, parameters: dict, rendered: str) -> None:
        key = self._make_key(template_hash, parameters)
        await self._redis.setex(key, self._ttl, rendered.encode("utf-8"))
        logger.debug("template_cache_set", key=key)
