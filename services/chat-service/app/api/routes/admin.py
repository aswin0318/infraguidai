import boto3
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.config.settings import get_settings
from infraguid_common.database.postgres_client import get_db_session
from infraguid_common.database.repositories.document_repo import DocumentRepository
from infraguid_common.observability.logger import get_logger
from infraguid_common.vectorstore.pgvector_store import PgVectorStore

from app.clients.agent_client import list_agent_tools
from app.clients.ingestion_client import trigger_ingest

logger = get_logger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/ingest")
async def ingest() -> dict:
    """Proxy to ingestion-service to (re)ingest the knowledge base."""
    try:
        return await trigger_ingest()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Ingestion failed: {exc.response.text}") from exc
    except httpx.HTTPError as exc:
        logger.error("ingestion_service_unreachable", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Ingestion service unreachable: {exc}") from exc


@router.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only Markdown (.md) files are supported.")

    settings = get_settings()
    try:
        s3 = boto3.client("s3", region_name=settings.aws_region)
        safe_filename = file.filename.replace("\\", "/").split("/")[-1]
        key = f"knowledge-base/{safe_filename}"
        s3.upload_fileobj(file.file, settings.s3_document_bucket, key)
        logger.info("admin_upload_s3_success", filename=safe_filename, bucket=settings.s3_document_bucket)
        return {"status": "success", "filename": safe_filename, "s3_key": key}
    except Exception as exc:
        logger.error("admin_upload_failed", filename=file.filename, error=str(exc))
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {exc}") from exc


@router.get("/stats")
async def stats(session: AsyncSession = Depends(get_db_session)) -> dict:
    try:
        counts = await DocumentRepository(session).counts()
        vector_store = PgVectorStore(session)
        vector_chunks = await vector_store.count()
        return {
            "documents": counts["documents"],
            "chunks": counts["chunks"],
            "vector_chunks": vector_chunks,
            "last_ingestion": counts["last_ingestion"].isoformat() if counts["last_ingestion"] else None,
        }
    except Exception as exc:
        logger.error("admin_stats_failed", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Stats unavailable: {exc}") from exc


@router.get("/documents")
async def documents(session: AsyncSession = Depends(get_db_session)) -> list[dict]:
    try:
        rows = await DocumentRepository(session).list_documents()
        return [
            {
                "document_id": row["document_id"],
                "title": row["title"],
                "category": row["category"],
                "path": row["path"],
                "chunk_count": row["chunk_count"],
                "status": row.get("metadata", {}).get("status"),
                "owner": row.get("metadata", {}).get("owner"),
                "updated_at": row["updated_at"].isoformat() if row.get("updated_at") else None,
            }
            for row in rows
        ]
    except Exception as exc:
        logger.error("admin_documents_failed", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Document list unavailable: {exc}") from exc


@router.get("/chunks")
async def chunks(
    limit: int = Query(default=25, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    try:
        from sqlalchemy import select
        from infraguid_common.database.models import DocumentChunk

        stmt = select(DocumentChunk).limit(limit)
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return {
            "chunks": [
                {
                    "id": row.chunk_id,
                    "metadata": row.metadata_fields,
                    "preview": row.content[:500] if row.content else "",
                }
                for row in rows
            ]
        }
    except Exception as exc:
        logger.error("admin_chunks_failed", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Chunk explorer unavailable: {exc}") from exc


@router.get("/agent/tools")
async def agent_tools() -> dict:
    """Proxy to agent-service for the list of LangGraph tool capabilities."""
    try:
        return await list_agent_tools()
    except httpx.HTTPError as exc:
        logger.error("agent_service_unreachable", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Agent tool list unavailable: {exc}") from exc
