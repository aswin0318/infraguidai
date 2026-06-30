from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from infraguid_common.llm.bedrock import (
    BedrockNotConfiguredError,
    BedrockThrottlingError,
    map_bedrock_error,
)
from infraguid_common.observability.logger import get_logger

from app.agent.graph import get_agent
from app.tools.agent_tools import available_agent_capabilities

logger = get_logger(__name__)
router = APIRouter(tags=["agent"])


class AgentRunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    history: list[dict] = []


class AgentRunResponse(BaseModel):
    answer: str
    sources: list[dict] = []
    route: str = "multi_step_agent"
    tools_used: list[str] = []
    trace: list[dict] = []


@router.get("/health")
async def health() -> dict:
    return {"status": "healthy", "service": "agent-service"}


@router.get("/agent/tools")
async def agent_tools() -> dict:
    tools = available_agent_capabilities()
    return {"tools": tools, "count": len(tools)}


@router.post("/agent/run", response_model=AgentRunResponse)
async def agent_run(request: AgentRunRequest) -> AgentRunResponse:
    try:
        result = await get_agent().run(request.message, request.history)
        return AgentRunResponse(**result)
    except Exception as exc:
        mapped = map_bedrock_error(exc)
        if isinstance(mapped, BedrockNotConfiguredError):
            raise HTTPException(status_code=503, detail=str(mapped)) from exc
        if isinstance(mapped, BedrockThrottlingError):
            raise HTTPException(status_code=429, detail=f"Bedrock throttling limit reached: {mapped}") from exc
        logger.error("agent_run_failed", error=str(exc))
        raise HTTPException(status_code=502, detail=f"Agent run failed: {mapped}") from exc
