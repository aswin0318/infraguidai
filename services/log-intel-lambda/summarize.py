"""Summarize an incident and classify severity using Bedrock Claude."""
from __future__ import annotations

import json
import logging
import os

import boto3

logger = logging.getLogger()

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")

_bedrock = None


def _client():
    global _bedrock
    if _bedrock is None:
        _bedrock = boto3.client("bedrock-runtime")
    return _bedrock


_SYSTEM = (
    "You are InfraGuid's Kubernetes SRE assistant. Given raw pod log evidence for "
    "a detected anomaly, produce a concise post-deployment incident summary for an "
    "on-call engineer. Be specific and actionable."
)

_PROMPT = """A Kubernetes anomaly was detected.

Error type: {error_type}
Namespace: {namespace}
Pod: {pod}
Container: {container}
Default severity (heuristic): {default_severity}

Recent log evidence:
{evidence}

Respond ONLY with a JSON object (no markdown) with these keys:
  "severity": one of "P1","P2","P3","P4"
  "root_cause": one sentence likely root cause
  "summary": 2-3 sentence human summary
  "suggested_fix": one concrete remediation step
"""


def _build_evidence(incident: dict) -> str:
    lines = incident.get("samples", []) + incident.get("context_lines", [])
    # De-dupe while preserving order, cap total size.
    seen, out = set(), []
    for line in lines:
        if line not in seen:
            seen.add(line)
            out.append(f"- {line}")
        if len(out) >= 25:
            break
    return "\n".join(out) or "(no log lines captured)"


def summarize_incident(incident: dict) -> dict:
    """Return {severity, root_cause, summary, suggested_fix}. Falls back to a
    heuristic summary if Bedrock is unavailable."""
    prompt = _PROMPT.format(
        error_type=incident["error_type"],
        namespace=incident["namespace"],
        pod=incident["pod"],
        container=incident["container"],
        default_severity=incident["default_severity"],
        evidence=_build_evidence(incident),
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 600,
        "temperature": 0,
        "system": _SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        resp = _client().invoke_model(modelId=MODEL_ID, body=json.dumps(body))
        payload = json.loads(resp["body"].read())
        text = payload["content"][0]["text"].strip()
        # Claude may wrap JSON in prose/fences; extract the object.
        start, end = text.find("{"), text.rfind("}")
        parsed = json.loads(text[start:end + 1])
        return {
            "severity": parsed.get("severity", incident["default_severity"]),
            "root_cause": parsed.get("root_cause", "unknown"),
            "summary": parsed.get("summary", ""),
            "suggested_fix": parsed.get("suggested_fix", ""),
        }
    except Exception as exc:  # noqa: BLE001 - never fail the alert on LLM errors
        logger.warning("Bedrock summarization failed, using heuristic: %s", exc)
        return {
            "severity": incident["default_severity"],
            "root_cause": f"{incident['error_type']} detected",
            "summary": (
                f"{incident['error_type']} in pod {incident['pod']} "
                f"(namespace {incident['namespace']}). Review recent deploy."
            ),
            "suggested_fix": "Inspect pod events and recent rollout; consider rollback.",
        }
