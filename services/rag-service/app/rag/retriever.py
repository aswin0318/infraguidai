from infraguid_common.config.settings import get_settings
from infraguid_common.database.postgres_client import _get_session_factory
from infraguid_common.llm.bedrock import get_embeddings
from infraguid_common.vectorstore.pgvector_store import PgVectorStore


class KnowledgeRetriever:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.embeddings = get_embeddings()
        self._session_factory = _get_session_factory()

    async def retrieve(self, query: str, top_k: int | None = None) -> list[dict]:
        """Embed the query (Bedrock) and run a pgvector similarity search."""
        embedding = await self.embeddings.aembed_query(query)
        async with self._session_factory() as session:
            store = PgVectorStore(session)
            return await store.query(embedding, top_k or self.settings.rag_top_k)
