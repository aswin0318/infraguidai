from infraguid_common.config.settings import get_settings
from infraguid_common.http.service_client import post_json


async def rag_search(query: str, top_k: int = 5) -> dict:
    """Call rag-service to retrieve knowledge base chunks (returns sources + previews)."""
    settings = get_settings()
    return await post_json(
        f"{settings.rag_service_url}/rag/search",
        {"query": query, "top_k": top_k},
    )
