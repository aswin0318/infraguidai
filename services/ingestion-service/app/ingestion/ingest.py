import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.config.settings import get_settings
from infraguid_common.database.repositories.document_repo import DocumentRepository
from infraguid_common.llm.bedrock import BedrockNotConfiguredError, map_bedrock_error
from infraguid_common.observability.logger import get_logger
from infraguid_common.vectorstore.pgvector_store import PgVectorStore

from app.ingestion.chunker import MarkdownChunker
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.embedder import DocumentEmbedder
from app.ingestion.metadata_loader import MetadataLoader

logger = get_logger(__name__)


class IngestionService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.loader = DocumentLoader(self.settings.knowledge_base_path)
        self.metadata_loader = MetadataLoader(self.settings.knowledge_base_path)
        self.chunker = MarkdownChunker(self.settings.chunk_size, self.settings.chunk_overlap)
        self.embedder = DocumentEmbedder()

    async def _embed_with_backoff(self, texts: list[str], max_retries: int = 8) -> list[list[float]]:
        """Embed a batch, retrying with exponential backoff on Bedrock throttling."""
        delay = 2.0
        for attempt in range(max_retries):
            try:
                return await self.embedder.embed(texts)
            except Exception as exc:
                message = str(exc)
                throttled = "Throttl" in message or "Too many requests" in message
                if not throttled or attempt == max_retries - 1:
                    raise
                logger.warning("embed_throttled_retry", attempt=attempt + 1, delay=delay)
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30.0)
        raise RuntimeError("unreachable")

    async def run(self, session: AsyncSession, reset: bool = True) -> dict:
        repo = DocumentRepository(session)
        store = PgVectorStore(session)
        documents_processed = 0
        chunks_created = 0
        try:
            loaded_documents = self.loader.load()
            if reset:
                await store.reset()
            for document in loaded_documents:
                metadata = self.metadata_loader.load(document.document_id)
                chunks = self.chunker.split(document.document_id, document.content, metadata, document.relative_path)
                ids = [chunk.chunk_id for chunk in chunks]
                texts = [chunk.content for chunk in chunks]
                metadatas = [chunk.metadata for chunk in chunks]
                await repo.upsert_document(
                    document_id=document.document_id,
                    title=metadata.get("title", document.document_id.replace("_", " ").title()),
                    category=metadata.get("category", "uncategorized"),
                    path=document.relative_path,
                    chunk_count=len(chunks),
                    metadata=metadata,
                )
                batch_size = 3
                for start in range(0, len(texts), batch_size):
                    batch_texts = texts[start : start + batch_size]
                    batch_ids = ids[start : start + batch_size]
                    batch_metadatas = metadatas[start : start + batch_size]
                    embeddings = await self._embed_with_backoff(batch_texts)
                    await store.upsert(
                        batch_ids,
                        batch_texts,
                        embeddings,
                        batch_metadatas,
                        document_id=document.document_id,
                    )
                    # Pace requests to stay under low (new-account) Bedrock quotas.
                    await asyncio.sleep(1.0)
                # Commit per document so progress persists even if a later
                # document throttles — re-running resumes the rest.
                await session.commit()
                documents_processed += 1
                chunks_created += len(chunks)
            await repo.add_ingestion_log("success", documents_processed, chunks_created)
            logger.info("ingestion_complete", documents=documents_processed, chunks=chunks_created)
            return {"status": "success", "documents_processed": documents_processed, "chunks_created": chunks_created}
        except Exception as exc:
            mapped = map_bedrock_error(exc)
            if isinstance(mapped, BedrockNotConfiguredError):
                await repo.add_ingestion_log("bedrock_not_configured", documents_processed, chunks_created, error_message=str(mapped))
                logger.warning("ingestion_skipped_bedrock_not_configured", error=str(mapped))
                return {
                    "status": "bedrock_not_configured",
                    "message": str(mapped),
                    "documents_processed": documents_processed,
                    "chunks_created": chunks_created,
                }
            await repo.add_ingestion_log("failed", documents_processed, chunks_created, error_message=str(mapped))
            logger.error("ingestion_failed", error=str(mapped), documents=documents_processed, chunks=chunks_created)
            raise mapped
