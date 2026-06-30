from dataclasses import dataclass
from pathlib import Path

import boto3

from infraguid_common.config.settings import get_settings
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class LoadedDocument:
    document_id: str
    path: str
    relative_path: str
    content: str


class DocumentLoader:
    """Load Markdown documents from S3 bucket or local filesystem fallback."""

    def __init__(self, knowledge_base_path: str | None = None) -> None:
        self.settings = get_settings()
        self._local_path = knowledge_base_path or self.settings.knowledge_base_path

    def load(self) -> list[LoadedDocument]:
        """Try S3 first, fall back to local filesystem."""
        try:
            return self._load_from_s3()
        except Exception as exc:
            logger.warning("s3_load_fallback_to_local", error=str(exc))
            return self._load_from_local()

    def _load_from_s3(self) -> list[LoadedDocument]:
        s3 = boto3.client("s3", region_name=self.settings.aws_region)
        bucket = self.settings.s3_document_bucket
        documents: list[LoadedDocument] = []

        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix="knowledge-base/"):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if not key.endswith(".md"):
                    continue
                if "metadata/" in key:
                    continue

                response = s3.get_object(Bucket=bucket, Key=key)
                content = response["Body"].read().decode("utf-8")
                relative_path = key.replace("knowledge-base/", "", 1)
                document_id = Path(key).stem

                documents.append(
                    LoadedDocument(
                        document_id=document_id,
                        path=key,
                        relative_path=relative_path,
                        content=content,
                    )
                )

        logger.info("s3_documents_loaded", count=len(documents), bucket=bucket)
        return sorted(documents, key=lambda d: d.relative_path)

    def _load_from_local(self) -> list[LoadedDocument]:
        root = Path(self._local_path)
        documents: list[LoadedDocument] = []
        if not root.exists():
            logger.warning("local_knowledge_base_not_found", path=str(root))
            return documents
        for path in sorted(root.rglob("*.md")):
            if "metadata" in path.parts:
                continue
            relative = path.relative_to(root).as_posix()
            documents.append(
                LoadedDocument(
                    document_id=path.stem,
                    path=str(path),
                    relative_path=relative,
                    content=path.read_text(encoding="utf-8"),
                )
            )
        logger.info("local_documents_loaded", count=len(documents))
        return documents
