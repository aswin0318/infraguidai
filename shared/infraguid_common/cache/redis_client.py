from __future__ import annotations

import redis.asyncio as aioredis

from infraguid_common.config.settings import get_settings
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)

_pool: aioredis.Redis | None = None


def _build_pool() -> aioredis.Redis:
    settings = get_settings()
    return aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=20,
        socket_connect_timeout=5,
        socket_timeout=5,
    )


def get_redis_client() -> aioredis.Redis:
    global _pool
    if _pool is None:
        _pool = _build_pool()
    return _pool


async def close_redis() -> None:
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None
        logger.info("redis_connection_closed")


async def ping_redis() -> dict:
    """Health-check ping; raises on failure."""
    client = get_redis_client()
    result = await client.ping()
    if not result:
        raise RuntimeError("Redis PING returned False")
    return {"status": "healthy"}
