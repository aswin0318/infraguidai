import json
from functools import lru_cache
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from infraguid_common.llm.bedrock import get_chat_model
from infraguid_common.llm.prompt_templates import SYSTEM_PROMPT
from infraguid_common.observability.logger import get_logger

from app.tools.agent_tools import get_agent_tools

logger = get_logger(__name__)

AGENT_SYSTEM_PROMPT = (
    f"{SYSTEM_PROMPT}\n\nCRITICAL DIRECTIVE: You MUST use the available tools "
    "(e.g. 'search_knowledge_base', 'lookup_runbook') to ground your answer before "
    "responding to any technical question about company policies, AWS standards, "
    "incidents, or Terraform. Never fabricate tool calls as text or code blocks — "
    "use the native tool-calling interface."
)


def _message_text(message: Any) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(p for p in parts if p).strip()
    return str(content).strip()


def _tool_message_str(message: ToolMessage) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            else:
                parts.append(str(block))
        return "\n".join(parts)
    return str(content)


class DevOpsAgent:
    """LangGraph ReAct agent replacing the hand-written Bedrock Converse tool loop."""

    def __init__(self) -> None:
        self._agent = create_react_agent(
            get_chat_model(temperature=0.1, max_tokens=5120),
            tools=get_agent_tools(),
            prompt=AGENT_SYSTEM_PROMPT,
        )

    async def run(self, message: str, history: list[dict] | None = None) -> dict:
        messages: list[Any] = []
        for h in history or []:
            role = h.get("role")
            content = str(h.get("content", ""))
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=message))

        result = await self._agent.ainvoke({"messages": messages})
        out_messages = result.get("messages", [])

        final_answer = ""
        for m in reversed(out_messages):
            if isinstance(m, AIMessage):
                text = _message_text(m)
                if text:
                    final_answer = text
                    break

        trace, tools_used, sources = self._build_trace(out_messages)
        return {
            "answer": final_answer,
            "sources": self._dedupe_sources(sources),
            "route": "multi_step_agent",
            "tools_used": tools_used,
            "trace": trace,
        }

    def _build_trace(self, out_messages: list[Any]) -> tuple[list[dict], list[str], list[dict]]:
        trace: list[dict[str, Any]] = []
        tools_used: list[str] = []
        sources: list[dict[str, Any]] = []
        pending: dict[str, dict] = {}
        step = 0

        for m in out_messages:
            if isinstance(m, AIMessage):
                tool_calls = getattr(m, "tool_calls", None) or []
                for tc in tool_calls:
                    pending[tc.get("id")] = {"name": tc.get("name"), "args": tc.get("args", {})}
                text = _message_text(m)
                if text and not tool_calls:
                    step += 1
                    trace.append({"step": step, "type": "final", "answer_preview": text[:500]})
            elif isinstance(m, ToolMessage):
                step += 1
                observation = _tool_message_str(m)
                meta = pending.get(m.tool_call_id, {})
                name = meta.get("name") or m.name
                tools_used.append(name)
                trace.append(
                    {
                        "step": step,
                        "type": "tool",
                        "tool": name,
                        "tool_input": meta.get("args", {}),
                        "observation_preview": observation[:900],
                    }
                )
                sources.extend(self._extract_sources(observation))

        return trace, tools_used, sources

    def _extract_sources(self, observation: str) -> list[dict[str, Any]]:
        try:
            payload = json.loads(observation)
        except (json.JSONDecodeError, TypeError):
            return []
        if not isinstance(payload, dict):
            return []
        sources = payload.get("sources", [])
        if isinstance(sources, list):
            return [source for source in sources if isinstance(source, dict)]
        return []

    def _dedupe_sources(self, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[tuple[str, str]] = set()
        unique: list[dict[str, Any]] = []
        for source in sources:
            key = (str(source.get("document_id", "")), str(source.get("path", "")))
            if key in seen:
                continue
            seen.add(key)
            unique.append(source)
        return unique[:10]


@lru_cache(maxsize=1)
def get_agent() -> DevOpsAgent:
    return DevOpsAgent()
