"""Publish the incident summary to SNS (notify-only)."""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()

TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")

_sns = None


def _client():
    global _sns
    if _sns is None:
        _sns = boto3.client("sns")
    return _sns


def _fmt_ts(ms: int | None) -> str:
    if not ms:
        return "unknown"
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def publish_alert(summary: dict, incident: dict) -> None:
    if not TOPIC_ARN:
        logger.error("SNS_TOPIC_ARN not set; cannot publish alert")
        return

    severity = summary["severity"]
    subject = f"[{severity}] {incident['error_type']} in {incident['pod']}"[:100]

    body = f"""InfraGuid Kubernetes Log Intelligence Agent

Severity:    {severity}
Error:       {incident['error_type']}
Namespace:   {incident['namespace']}
Pod:         {incident['pod']}
Container:   {incident['container']}
First seen:  {_fmt_ts(incident.get('first_timestamp'))}
Last seen:   {_fmt_ts(incident.get('last_timestamp'))}

Root cause:  {summary['root_cause']}

Summary:
{summary['summary']}

Suggested fix:
{summary['suggested_fix']}

— Triggered automatically from CloudWatch pod logs. Notify-only; remediate manually.
"""

    _client().publish(TopicArn=TOPIC_ARN, Subject=subject, Message=body)
    logger.info("Published %s alert for pod %s", severity, incident["pod"])
