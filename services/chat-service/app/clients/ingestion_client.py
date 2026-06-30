from infraguid_common.config.settings import get_settings
from infraguid_common.http.service_client import post_json


async def trigger_ingest() -> dict:
    """Call ingestion-service to (re)ingest the knowledge base."""
    settings = get_settings()
    return await post_json(
        f"{settings.ingestion_service_url}/ingest",
        {},
        timeout=600.0,
    )
