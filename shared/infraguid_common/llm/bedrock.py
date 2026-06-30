"""LangChain AWS factories for Bedrock chat + embedding models.

Replaces the hand-written boto3 Converse wrapper. Credentials follow the same
rule as before: explicit keys are used when present (local dev), otherwise the
default boto3 credential chain is used (IAM role on the compute instance).
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from langchain_aws import BedrockEmbeddings, ChatBedrockConverse

from infraguid_common.config.settings import get_settings

BEDROCK_NOT_CONFIGURED_MESSAGE = "AWS Bedrock is not configured. Please check your AWS credentials."


class BedrockNotConfiguredError(RuntimeError):
    pass


class BedrockThrottlingError(RuntimeError):
    pass


class BedrockInvocationError(RuntimeError):
    pass


def _bedrock_runtime_client():
    settings = get_settings()
    session_kwargs: dict = {"region_name": settings.aws_region}
    # Only pass explicit credentials when provided (local dev). When empty,
    # boto3 uses its credential chain (IAM role on the compute instance).
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = settings.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = settings.aws_secret_access_key
    if settings.aws_session_token:
        session_kwargs["aws_session_token"] = settings.aws_session_token
    session = boto3.Session(**session_kwargs)
    return session.client("bedrock-runtime")


def get_chat_model(temperature: float = 0.2, max_tokens: int = 4096) -> ChatBedrockConverse:
    """Return a ChatBedrockConverse model bound to the configured chat model id."""
    settings = get_settings()
    return ChatBedrockConverse(
        client=_bedrock_runtime_client(),
        model_id=settings.bedrock_chat_model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def get_embeddings() -> BedrockEmbeddings:
    """Return a BedrockEmbeddings model bound to the configured embedding model id."""
    settings = get_settings()
    return BedrockEmbeddings(
        client=_bedrock_runtime_client(),
        model_id=settings.bedrock_embedding_model_id,
        normalize=True,
    )


def map_bedrock_error(exc: Exception) -> Exception:
    """Map a botocore error to an InfraGuid Bedrock error for consistent handling."""
    if isinstance(exc, NoCredentialsError):
        return BedrockNotConfiguredError(BEDROCK_NOT_CONFIGURED_MESSAGE)
    if isinstance(exc, ClientError):
        code = exc.response.get("Error", {}).get("Code", "")
        if "Throttl" in code or code in {"TooManyRequestsException", "ServiceQuotaExceededException"}:
            return BedrockThrottlingError(str(exc))
        if code in {"AccessDeniedException", "UnrecognizedClientException", "InvalidSignatureException"}:
            return BedrockNotConfiguredError(BEDROCK_NOT_CONFIGURED_MESSAGE)
        return BedrockInvocationError(str(exc))
    return exc
