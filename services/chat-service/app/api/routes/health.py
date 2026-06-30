from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.cache.redis_client import ping_redis
from infraguid_common.database.postgres_client import get_db_session, ping_db
from infraguid_common.vectorstore.pgvector_store import PgVectorStore

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health(session: AsyncSession = Depends(get_db_session)) -> dict:
    errors: list[str] = []

    pg_status = "healthy"
    vector_count = 0
    try:
        await ping_db()
        store = PgVectorStore(session)
        vector_count = await store.count()
    except Exception as exc:
        pg_status = f"unhealthy: {exc}"
        errors.append(pg_status)

    redis_status = "healthy"
    try:
        await ping_redis()
    except Exception as exc:
        redis_status = f"unhealthy: {exc}"
        errors.append(redis_status)

    if errors:
        raise HTTPException(
            status_code=503,
            detail={"postgresql": pg_status, "redis": redis_status, "vector_chunks": vector_count},
        )

    return {
        "status": "healthy",
        "postgresql": pg_status,
        "pgvector": "healthy",
        "redis": redis_status,
        "vector_chunks": vector_count,
    }
