import json
from typing import Any

from app.rag.prompt_builder import PromptBuilder


def to_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, default=str)


def chunk_payload(chunks: list[dict]) -> dict[str, Any]:
    """Build the search payload returned to the agent service (sources + previews)."""
    builder = PromptBuilder()
    return {
        "sources": builder.sources(chunks),
        "chunks": [
            {
                "title": chunk.get("metadata", {}).get("title"),
                "path": chunk.get("metadata", {}).get("source_path"),
                "category": chunk.get("metadata", {}).get("category"),
                "preview": chunk.get("content", "")[:1200],
                "distance": chunk.get("distance"),
            }
            for chunk in chunks
        ],
    }
