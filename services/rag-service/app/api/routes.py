from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from infraguid_common.database.postgres_client import ping_db
from infraguid_common.observability.logger import get_logger

from app.rag.payload import chunk_payload
from app.rag.rag_pipeline import RagPipeline
from app.rag.retriever import KnowledgeRetriever

logger = get_logger(__name__)
router = APIRouter(tags=["rag"])


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)


@router.get("/health")
async def health() -> dict:
    try:
        await ping_db()
        return {"status": "healthy", "service": "rag-service"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"rag-service unhealthy: {exc}") from exc


@router.post("/rag/search")
async def rag_search(request: SearchRequest) -> dict:
    try:
        chunks = await KnowledgeRetriever().retrieve(request.query, top_k=request.top_k)
        return chunk_payload(chunks)
    except Exception as exc:
        logger.error("rag_search_failed", error=str(exc))
        raise HTTPException(status_code=502, detail=f"RAG search failed: {exc}") from exc


@router.post("/rag/answer")
async def rag_answer(request: QuestionRequest) -> dict:
    try:
        return await RagPipeline().answer(request.question)
    except Exception as exc:
        logger.error("rag_answer_failed", error=str(exc))
        raise HTTPException(status_code=502, detail=f"RAG answer failed: {exc}") from exc


@router.post("/rag/terraform")
async def rag_terraform(request: QuestionRequest) -> dict:
    try:
        return await RagPipeline().terraform(request.question)
    except Exception as exc:
        logger.error("rag_terraform_failed", error=str(exc))
        raise HTTPException(status_code=502, detail=f"RAG terraform failed: {exc}") from exc
