from typing import Any

from sqlalchemy import delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.database.models import DocumentChunk
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)


class PgVectorStore:
    """Vector store backed by PostgreSQL pgvector extension."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        document_id: str | None = None,
    ) -> None:
        if not ids:
            return
        for i, chunk_id in enumerate(ids):
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                document_id=document_id or metadatas[i].get("document_id", "unknown"),
                content=documents[i],
                embedding=embeddings[i],
                metadata_fields=metadatas[i],
            )
            await self._session.merge(chunk)
        await self._session.flush()

    async def query(self, embedding: list[float], top_k: int) -> list[dict[str, Any]]:
        """Cosine distance search using pgvector <=> operator."""
        embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
        stmt = text(
            """
            SELECT chunk_id, content, metadata_fields,
                   embedding <=> CAST(:embedding AS vector) AS distance
            FROM document_chunks
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :top_k
            """
        ).bindparams(embedding=embedding_str, top_k=int(top_k))

        result = await self._session.execute(stmt)
        rows = result.fetchall()
        return [
            {
                "id": row.chunk_id,
                "content": row.content,
                "metadata": row.metadata_fields,
                "distance": float(row.distance) if row.distance is not None else None,
            }
            for row in rows
        ]

    async def count(self) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(DocumentChunk)
        )
        return int(result.scalar() or 0)

    async def reset(self) -> None:
        await self._session.execute(delete(DocumentChunk))
        await self._session.flush()
        logger.info("pgvector_store_reset")
