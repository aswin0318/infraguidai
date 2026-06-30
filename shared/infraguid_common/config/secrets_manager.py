"""
AWS Secrets Manager client for InfraGuidAI.

Fetches and caches application secrets at startup. In production, the compute
instance's IAM role grants access to the secret. The secret name is passed via
the AWS_SECRET_NAME environment variable.

Expected secret JSON structure:
{
    "POSTGRES_URI": "postgresql+asyncpg://user:pass@rds-host:5432/infraguid",
    "COGNITO_USER_POOL_ID": "us-east-1_XXXXXXXXX",
    "COGNITO_APP_CLIENT_ID": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
    "S3_DOCUMENT_BUCKET": "infraguidai-documents",
    "BEDROCK_CHAT_MODEL_ID": "us.meta.llama3-1-70b-instruct-v1:0",
    "BEDROCK_EMBEDDING_MODEL_ID": "amazon.titan-embed-text-v2:0"
}

Terraform provisions this secret and the IAM role policy that grants
`secretsmanager:GetSecretValue` on the specific secret ARN.
"""

import json
import logging
import os
from functools import lru_cache
from typing import Any

# Use stdlib logging — this module runs BEFORE structlog is configured
logger = logging.getLogger(__name__)


def _get_secrets_client():
    """Create a Secrets Manager client using the default credential chain (IAM role)."""
    import boto3

    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region)


@lru_cache(maxsize=1)
def fetch_secrets(secret_name: str) -> dict[str, Any]:
    """
    Fetch a secret from AWS Secrets Manager and return parsed JSON.
    Result is cached for the lifetime of the process.
    """
    try:
        client = _get_secrets_client()
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get("SecretString")
        if not secret_string:
            raise RuntimeError(f"Secret '{secret_name}' has no SecretString value")
        parsed = json.loads(secret_string)
        logger.info("Secrets Manager loaded secret '%s' with keys: %s", secret_name, list(parsed.keys()))
        return parsed
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Secret '{secret_name}' is not valid JSON: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch secret '{secret_name}': {exc}") from exc


def get_secret_value(key: str, default: str = "") -> str:
    """
    Get a specific key from the cached secret.
    Returns the default if Secrets Manager is not configured (local dev).
    """
    secret_name = os.environ.get("AWS_SECRET_NAME", "")
    if not secret_name:
        return default
    try:
        secrets = fetch_secrets(secret_name)
        return str(secrets.get(key, default))
    except RuntimeError:
        return default


def load_secrets_into_env() -> None:
    """
    Load secrets from AWS Secrets Manager into environment variables.
    This is called BEFORE Settings() is initialized, so pydantic-settings
    picks up the values from os.environ.

    Only sets env vars that are NOT already set, so explicit env vars
    (e.g., from .env file in development) take precedence.
    """
    secret_name = os.environ.get("AWS_SECRET_NAME", "")
    if not secret_name:
        logger.info("Secrets Manager skipped — AWS_SECRET_NAME not set (local development mode)")
        return

    try:
        secrets = fetch_secrets(secret_name)
        injected = []
        for key, value in secrets.items():
            if key not in os.environ:
                os.environ[key] = str(value)
                injected.append(key)
        logger.info(
            "Secrets Manager injected %d/%d keys from '%s': %s",
            len(injected), len(secrets), secret_name, injected,
        )
    except RuntimeError as exc:
        logger.error("Secrets Manager failed: %s", exc)
        raise
