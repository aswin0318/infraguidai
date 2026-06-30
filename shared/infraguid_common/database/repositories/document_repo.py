from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.database.models import IngestionLog, KnowledgeDocument, utc_now


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_document(
        self,
        document_id: str,
        title: str,
        category: str,
        path: str,
        chunk_count: int,
        metadata: dict,
    ) -> None:
        stmt = select(KnowledgeDocument).where(KnowledgeDocument.document_id == document_id)
        result = await self._session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing is not None:
            existing.title = title
            existing.category = category
            existing.path = path
            existing.chunk_count = chunk_count
            existing.metadata_fields = metadata
            existing.updated_at = utc_now()
        else:
            doc = KnowledgeDocument(
                document_id=document_id,
                title=title,
                category=category,
                path=path,
                chunk_count=chunk_count,
                metadata_fields=metadata,
            )
            self._session.add(doc)
        await self._session.flush()

    async def add_ingestion_log(
        self,
        status: str,
        documents_processed: int,
        chunks_created: int,
        document_id: str | None = None,
        error_message: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        log = IngestionLog(
            document_id=document_id,
            status=status,
            documents_processed=documents_processed,
            chunks_created=chunks_created,
            error_message=error_message,
            metadata_fields=metadata or {},
        )
        self._session.add(log)
        await self._session.flush()

    async def list_documents(self) -> list[dict]:
        stmt = select(KnowledgeDocument).order_by(
            KnowledgeDocument.category, KnowledgeDocument.title
        )
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return [
            {
                "document_id": row.document_id,
                "title": row.title,
                "category": row.category,
                "path": row.path,
                "chunk_count": row.chunk_count,
                "metadata": row.metadata_fields,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
            }
            for row in rows
        ]

    async def counts(self) -> dict:
        doc_count_result = await self._session.execute(
            select(func.count()).select_from(KnowledgeDocument)
        )
        documents = doc_count_result.scalar() or 0

        chunk_sum_result = await self._session.execute(
            select(func.coalesce(func.sum(KnowledgeDocument.chunk_count), 0))
        )
        chunks = int(chunk_sum_result.scalar() or 0)

        last_result = await self._session.execute(
            select(IngestionLog.ingested_at)
            .order_by(IngestionLog.ingested_at.desc())
            .limit(1)
        )
        last_row = last_result.scalar_one_or_none()

        return {
            "documents": int(documents),
            "chunks": chunks,
            "last_ingestion": last_row,
        }
