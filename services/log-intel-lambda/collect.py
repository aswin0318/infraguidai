"""Anomaly extraction and context enrichment for the Log Intelligence Agent.

Fluent Bit ships pod logs to CloudWatch; this module turns the matching log
events into structured incidents and (best effort) gathers surrounding context.
Relies only on the Lambda runtime's bundled boto3 + stdlib.
"""
from __future__ import annotations

import json
import logging

import boto3

logger = logging.getLogger()

# Anomaly classes the agent recognises, mapped to a default P-severity. The LLM
# may refine severity, but this guarantees a sensible floor if the LLM is skipped.
ANOMALY_PATTERNS: dict[str, str] = {
    "OOMKilled": "P1",
    "CrashLoopBackOff": "P1",
    "ImagePullBackOff": "P2",
    "ErrImagePull": "P2",
    "Liveness probe failed": "P2",
    "Readiness probe failed": "P3",
    "Back-off restarting failed container": "P2",
}

_logs_client = None


def _logs():
    global _logs_client
    if _logs_client is None:
        _logs_client = boto3.client("logs")
    return _logs_client


def _parse_message(raw: str) -> tuple[str, dict]:
    """Return (text, k8s_metadata). Fluent Bit records may be JSON with a
    `kubernetes` block, or plain text."""
    raw = (raw or "").strip()
    if raw.startswith("{"):
        try:
            doc = json.loads(raw)
            k8s = doc.get("kubernetes", {}) or {}
            text = doc.get("log") or doc.get("message") or raw
            return text, k8s
        except json.JSONDecodeError:
            pass
    return raw, {}


def _pod_from_stream(log_stream: str) -> str:
    # Fluent Bit stream prefix is "pod-"; the remainder usually holds pod info.
    return log_stream[len("pod-"):] if log_stream.startswith("pod-") else log_stream


def extract_incidents(log_events: list[dict], log_stream: str) -> list[dict]:
    """Group matching log lines into one incident per (pod, error_type)."""
    grouped: dict[tuple, dict] = {}
    for event in log_events:
        text, k8s = _parse_message(event.get("message", ""))
        error_type = next((name for name in ANOMALY_PATTERNS if name in text), None)
        if not error_type:
            continue

        pod = k8s.get("pod_name") or _pod_from_stream(log_stream)
        namespace = k8s.get("namespace_name") or "unknown"
        container = k8s.get("container_name") or "unknown"
        key = (namespace, pod, error_type)

        incident = grouped.setdefault(key, {
            "error_type": error_type,
            "default_severity": ANOMALY_PATTERNS[error_type],
            "namespace": namespace,
            "pod": pod,
            "container": container,
            "first_timestamp": event.get("timestamp"),
            "last_timestamp": event.get("timestamp"),
            "samples": [],
        })
        incident["last_timestamp"] = event.get("timestamp")
        if len(incident["samples"]) < 15:
            incident["samples"].append(text[:1000])
    return list(grouped.values())


def enrich_context(incident: dict, log_group: str) -> None:
    """Best-effort: pull a few more recent lines for the pod from CloudWatch."""
    if not log_group:
        return
    try:
        resp = _logs().filter_log_events(
            logGroupName=log_group,
            filterPattern=f'"{incident["pod"]}"',
            limit=20,
        )
        incident["context_lines"] = [e["message"][:500] for e in resp.get("events", [])]
    except Exception as exc:  # noqa: BLE001 - enrichment is optional
        logger.warning("context enrichment failed: %s", exc)
        incident["context_lines"] = []
