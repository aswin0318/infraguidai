import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from infraguid_common.config.settings import get_settings
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("/{path:path}")
async def get_document(path: str):
    settings = get_settings()
    # SSE-KMS objects require SigV4 presigned URLs (s3v4), otherwise S3 returns
    # "Requests specifying Server Side Encryption with AWS KMS managed keys
    # require AWS Signature Version 4".
    s3_client = boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        aws_session_token=settings.aws_session_token,
        config=Config(signature_version="s3v4"),
    )
    s3_key = path if path.startswith("knowledge-base/") else f"knowledge-base/{path}"
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.s3_document_bucket, "Key": s3_key},
            ExpiresIn=3600,
        )
        return RedirectResponse(url=url)
    except ClientError as e:
        logger.error("s3_presign_error", error=str(e), path=path)
        raise HTTPException(status_code=500, detail="Could not generate document link")
