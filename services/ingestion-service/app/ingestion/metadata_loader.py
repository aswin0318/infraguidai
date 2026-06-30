import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from infraguid_common.config.settings import get_settings
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)


class MetadataLoader:
    """Load document metadata JSON from S3 or local filesystem fallback."""

    def __init__(self, knowledge_base_path: str | None = None) -> None:
        self.settings = get_settings()
        self._local_metadata_dir = Path(knowledge_base_path or self.settings.knowledge_base_path) / "metadata"

    def load(self, document_id: str) -> dict:
        try:
            return self._load_from_s3(document_id)
        except Exception:
            return self._load_from_local(document_id)

    def _load_from_s3(self, document_id: str) -> dict:
        s3 = boto3.client("s3", region_name=self.settings.aws_region)
        bucket = self.settings.s3_document_bucket
        key = f"knowledge-base/metadata/{document_id}.json"
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            return json.loads(response["Body"].read().decode("utf-8"))
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "NoSuchKey":
                return self._default_metadata(document_id)
            raise

    def _load_from_local(self, document_id: str) -> dict:
        path = self._local_metadata_dir / f"{document_id}.json"
        if not path.exists():
            return self._default_metadata(document_id)
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _default_metadata(document_id: str) -> dict:
        return {
            "document_id": document_id,
            "title": document_id.replace("_", " ").title(),
            "category": "uncategorized",
            "status": "Draft",
        }
