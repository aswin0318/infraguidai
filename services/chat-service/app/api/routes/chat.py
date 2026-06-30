import httpx
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from infraguid_common.cache.session_store import SessionStore
from infraguid_common.observability.logger import get_logger

from app.clients.agent_client import run_agent

logger = get_logger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    session_id: str | None = None
    user_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    route: str
    sources: list[dict]
    tools_used: list[str] = []
    trace: list[dict] = []


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    store = SessionStore()
    try:
        session_id = await store.ensure_session(
            request.session_id, request.message, request.user_id
        )
        history = await store.history(session_id, limit=12)
        await store.add_message(session_id, "user", request.message)

        result = await run_agent(request.message, history)

        await store.add_message(
            session_id,
            "assistant",
            result["answer"],
            sources=result.get("sources", []),
            metadata={
                "route": result.get("route"),
                "tools_used": result.get("tools_used", []),
            },
        )
        # trace is returned to the caller but NOT stored — it can contain verbose
        # tool observations and must not be persisted anywhere (privacy principle).
        return ChatResponse(
            session_id=session_id,
            answer=result["answer"],
            route=result.get("route", "multi_step_agent"),
            sources=result.get("sources", []),
            tools_used=result.get("tools_used", []),
            trace=result.get("trace", []),
        )
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        detail = exc.response.text
        logger.error("agent_service_error", status_code=status_code)
        raise HTTPException(status_code=status_code, detail=f"Agent service error: {detail}") from exc
    except httpx.HTTPError as exc:
        logger.error("agent_service_unreachable", error=str(exc))
        raise HTTPException(status_code=503, detail=f"Agent service unreachable: {exc}") from exc
    except Exception as exc:
        logger.error("chat_request_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Chat request failed: {exc}") from exc
