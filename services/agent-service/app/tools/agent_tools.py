import asyncio
import json
from typing import Any

import boto3
from botocore.exceptions import ClientError
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field

from infraguid_common.config.settings import get_settings

from app.clients.rag_client import rag_search


def _json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, default=str)


class SearchKnowledgeArgs(BaseModel):
    query: str = Field(description="Specific question or search phrase for the internal knowledge base.")
    top_k: int = Field(default=5, ge=1, le=10, description="Number of chunks to retrieve.")


class TerraformArgs(BaseModel):
    request: str = Field(description="Terraform generation request, including AWS service, environment, and constraints.")


class CatalogArgs(BaseModel):
    category: str | None = Field(default=None, description="Optional category filter: company, security, aws, platform, or operations.")


class TopicArgs(BaseModel):
    topic: str = Field(description="Incident, runbook, security, AWS, cost, or platform topic to inspect.")
    top_k: int = Field(default=5, ge=1, le=10, description="Number of chunks to retrieve.")


@tool("search_knowledge_base", args_schema=SearchKnowledgeArgs)
async def search_knowledge_base(query: str, top_k: int = 5) -> str:
    """Retrieve relevant chunks from the internal knowledge base. Use for company standards, AWS guides, platform policies, and general questions."""
    return _json(await rag_search(query, top_k))


@tool("generate_terraform", args_schema=TerraformArgs)
async def generate_terraform(request: str) -> str:
    """Generate Terraform code using approved internal standards and module references. Use only for infrastructure-as-code generation requests."""
    query = f"Terraform standards AWS provider module catalog reference architectures {request}"
    return _json(await rag_search(query, top_k=5))


@tool("list_document_catalog", args_schema=CatalogArgs)
async def list_document_catalog(category: str | None = None) -> str:
    """List available knowledge base documents and metadata. Use when deciding what sources or domains are available."""
    settings = get_settings()

    def _fetch_s3() -> list[dict[str, Any]]:
        s3 = boto3.client("s3", region_name=settings.aws_region)
        bucket = settings.s3_document_bucket
        prefix = "knowledge-base/metadata/"
        paginator = s3.get_paginator("list_objects_v2")
        results: list[dict[str, Any]] = []
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if not key.endswith(".json"):
                    continue
                response = s3.get_object(Bucket=bucket, Key=key)
                metadata = json.loads(response["Body"].read().decode("utf-8"))
                if category and metadata.get("category") != category:
                    continue
                results.append(
                    {
                        "document_id": metadata.get("document_id"),
                        "title": metadata.get("title"),
                        "category": metadata.get("category"),
                        "subcategory": metadata.get("subcategory"),
                        "document_type": metadata.get("document_type"),
                        "criticality": metadata.get("criticality"),
                        "key_topics": metadata.get("key_topics", []),
                    }
                )
        return results

    docs: list[dict[str, Any]] = []
    try:
        docs = await asyncio.to_thread(_fetch_s3)
    except (ClientError, Exception):
        from pathlib import Path

        metadata_dir = Path(settings.knowledge_base_path) / "metadata"
        if metadata_dir.exists():
            for path in sorted(metadata_dir.glob("*.json")):
                metadata = json.loads(path.read_text(encoding="utf-8"))
                if category and metadata.get("category") != category:
                    continue
                docs.append(
                    {
                        "document_id": metadata.get("document_id"),
                        "title": metadata.get("title"),
                        "category": metadata.get("category"),
                        "subcategory": metadata.get("subcategory"),
                        "document_type": metadata.get("document_type"),
                        "criticality": metadata.get("criticality"),
                        "key_topics": metadata.get("key_topics", []),
                    }
                )

    return _json({"documents": docs, "count": len(docs)})


@tool("lookup_incident_history", args_schema=TopicArgs)
async def lookup_incident_history(topic: str, top_k: int = 6) -> str:
    """Retrieve RCA and incident-history details, including timelines, root causes, corrective actions, and lessons learned."""
    query = f"production incident RCA root cause timeline corrective actions {topic}"
    return _json(await rag_search(query, top_k=top_k))


@tool("lookup_runbook", args_schema=TopicArgs)
async def lookup_runbook(topic: str, top_k: int = 6) -> str:
    """Retrieve operational runbook or SOP procedures for deployments, incidents, rollbacks, validation, and escalation."""
    query = f"deployment runbook incident response SOP operations procedure checklist {topic}"
    return _json(await rag_search(query, top_k=top_k))


@tool("lookup_security_guidance", args_schema=TopicArgs)
async def lookup_security_guidance(topic: str, top_k: int = 5) -> str:
    """Retrieve security standards for IAM, encryption, network controls, secrets, compliance, and production guardrails."""
    query = f"security standards IAM encryption network access secrets compliance {topic}"
    return _json(await rag_search(query, top_k=top_k))


@tool("lookup_cost_guidance", args_schema=TopicArgs)
async def lookup_cost_guidance(topic: str, top_k: int = 5) -> str:
    """Retrieve cost optimization standards, budget guidance, and service-specific savings recommendations."""
    query = f"cost optimization savings plans reserved instances budget alerts cost allocation {topic}"
    return _json(await rag_search(query, top_k=top_k))


@tool("check_bedrock_configuration")
async def check_bedrock_configuration() -> str:
    """Check whether Bedrock credentials and model IDs are configured in the application environment."""
    settings = get_settings()
    return _json(
        {
            "configured": settings.bedrock_configured,
            "region": settings.aws_region,
            "chat_model": settings.bedrock_chat_model_id,
            "embedding_model": settings.bedrock_embedding_model_id,
            "message": "Credentials are present." if settings.bedrock_configured else "AWS credentials are missing.",
        }
    )


def get_agent_tools() -> list[BaseTool]:
    return [
        search_knowledge_base,
        generate_terraform,
        list_document_catalog,
        lookup_incident_history,
        lookup_runbook,
        lookup_security_guidance,
        lookup_cost_guidance,
        check_bedrock_configuration,
    ]


def available_agent_capabilities() -> list[dict]:
    return [{"name": tool.name, "description": tool.description} for tool in get_agent_tools()]
