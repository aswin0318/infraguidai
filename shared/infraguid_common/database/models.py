from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)


# ChatSession and ChatMessage are intentionally absent.
# Conversation history is stored only in Redis (SessionStore) with a TTL,
# ensuring no message content is persisted to long-term storage.


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    document_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, default="uncategorized")
    path = Column(String, nullable=False)
    chunk_count = Column(Integer, nullable=False, default=0)
    metadata_fields = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)


class IngestionLog(Base):
    __tablename__ = "ingestion_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    documents_processed = Column(Integer, nullable=False, default=0)
    chunks_created = Column(Integer, nullable=False, default=0)
    error_message = Column(Text, nullable=True)
    metadata_fields = Column(JSON, nullable=False, default=dict)
    ingested_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(String, primary_key=True)
    document_id = Column(
        String,
        ForeignKey("knowledge_documents.document_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1024))
    metadata_fields = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
