from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    metadata: dict


class MarkdownChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, document_id: str, content: str, metadata: dict, relative_path: str) -> list[DocumentChunk]:
        normalized = content.replace("\r\n", "\n").strip()
        chunks: list[DocumentChunk] = []
        start = 0
        index = 0
        while start < len(normalized):
            end = min(start + self.chunk_size, len(normalized))
            if end < len(normalized):
                boundary = max(normalized.rfind("\n\n", start, end), normalized.rfind("\n", start, end), normalized.rfind(". ", start, end))
                if boundary > start + int(self.chunk_size * 0.55):
                    end = boundary + 1
            chunk_text = normalized[start:end].strip()
            if chunk_text:
                chunk_metadata = dict(metadata)
                chunk_metadata.update(
                    {
                        "document_id": document_id,
                        "chunk_index": index,
                        "source_path": relative_path,
                        "title": metadata.get("title", document_id),
                        "category": metadata.get("category", "uncategorized"),
                    }
                )
                chunks.append(DocumentChunk(f"{document_id}:{index}", document_id, index, chunk_text, chunk_metadata))
                index += 1
            if end >= len(normalized):
                break
            start = max(end - self.overlap, start + 1)
        return chunks
