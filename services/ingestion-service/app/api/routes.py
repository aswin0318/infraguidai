from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.database.postgres_client import get_db_session, ping_db
from infraguid_common.database.repositories.document_repo import DocumentRepository
from infraguid_common.llm.bedrock import BedrockThrottlingError, map_bedrock_error
from infraguid_common.observability.logger import get_logger
from infraguid_common.vectorstore.pgvector_store import PgVectorStore

from app.ingestion.ingest import IngestionService

logger = get_logger(__name__)
router = APIRouter(tags=["ingestion"])


@router.get("/health")
async def health() -> dict:
    try:
        await ping_db()
        return {"status": "healthy", "service": "ingestion-service"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"ingestion-service unhealthy: {exc}") from exc


@router.post("/ingest")
async def ingest(session: AsyncSession = Depends(get_db_session)) -> dict:
    try:
        return await IngestionService().run(session, reset=True)
    except Exception as exc:
        mapped = map_bedrock_error(exc)
        if isinstance(mapped, BedrockThrottlingError):
            raise HTTPException(status_code=429, detail=f"Bedrock throttling limit reached: {mapped}") from exc
        logger.error("ingest_failed", error=str(mapped))
        raise HTTPException(status_code=503, detail=f"Ingestion failed: {mapped}") from exc


@router.get("/stats")
async def stats(session: AsyncSession = Depends(get_db_session)) -> dict:
    try:
        counts = await DocumentRepository(session).counts()
        vector_chunks = await PgVectorStore(session).count()
        return {
            "documents": counts["documents"],
            "chunks": counts["chunks"],
            "vector_chunks": vector_chunks,
            "last_ingestion": counts["last_ingestion"].isoformat() if counts["last_ingestion"] else None,
        }
    except Exception as exc:
        logger.error("ingestion_stats_failed", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Stats unavailable: {exc}") from exc
