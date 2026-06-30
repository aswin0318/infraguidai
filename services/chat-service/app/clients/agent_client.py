from infraguid_common.config.settings import get_settings
from infraguid_common.http.service_client import get_json, post_json


async def run_agent(message: str, history: list[dict]) -> dict:
    """Call agent-service to run the LangGraph DevOps agent."""
    settings = get_settings()
    return await post_json(
        f"{settings.agent_service_url}/agent/run",
        {"message": message, "history": history},
        timeout=180.0,
    )


async def list_agent_tools() -> dict:
    settings = get_settings()
    return await get_json(f"{settings.agent_service_url}/agent/tools")
