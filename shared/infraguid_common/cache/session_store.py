from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from infraguid_common.cache.redis_client import get_redis_client
from infraguid_common.config.settings import get_settings
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)

_MAX_MESSAGES = 50


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SessionStore:
    """
    Ephemeral session store backed by Redis.

    All conversation data lives only in Redis and expires automatically via
    TTL (default: SESSION_TTL_SECONDS, refreshed on each message). Nothing is
    written to PostgreSQL — no message content is persisted long-term.

    Key schema:  session:{session_id}  →  JSON blob
    TTL:         refreshed on every add_message / ensure_session call
    """

    def __init__(self) -> None:
        self._redis = get_redis_client()
        self._ttl: int = get_settings().session_ttl_seconds

    def _key(self, session_id: str) -> str:
        return f"session:{session_id}"

    async def ensure_session(
        self,
        session_id: str | None,
        first_message: str | None = None,
        user_id: str | None = None,
    ) -> str:
        resolved = session_id or str(uuid4())
        key = self._key(resolved)
        existing = await self._redis.get(key)
        if existing is None:
            title = (first_message or "InfraGuid chat").strip()[:120]
            blob = {
                "session_id": resolved,
                "title": title,
                "user_id": user_id,
                "created_at": _utc_iso(),
                "messages": [],
            }
            await self._redis.setex(key, self._ttl, json.dumps(blob))
            logger.info("session_created", session_id=resolved)
        else:
            # Refresh TTL on activity so idle sessions expire but active ones do not.
            await self._redis.expire(key, self._ttl)
        return resolved

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        sources: list | None = None,
        metadata: dict | None = None,
    ) -> None:
        key = self._key(session_id)
        raw = await self._redis.get(key)
        if raw is None:
            logger.warning("session_not_found_on_add", session_id=session_id)
            return
        blob = json.loads(raw)
        blob["messages"].append(
            {
                "role": role,
                "content": content,
                "sources": sources or [],
                # Store only routing metadata, never raw tool traces (privacy).
                "metadata": {k: v for k, v in (metadata or {}).items() if k in ("route", "tools_used")},
                "created_at": _utc_iso(),
            }
        )
        # Trim to keep memory bounded even for very long sessions.
        if len(blob["messages"]) > _MAX_MESSAGES:
            blob["messages"] = blob["messages"][-_MAX_MESSAGES:]
        await self._redis.setex(key, self._ttl, json.dumps(blob))

    async def history(self, session_id: str, limit: int = 20) -> list[dict]:
        key = self._key(session_id)
        raw = await self._redis.get(key)
        if raw is None:
            return []
        blob = json.loads(raw)
        return blob.get("messages", [])[-limit:]
