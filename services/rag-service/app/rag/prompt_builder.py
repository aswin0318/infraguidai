from infraguid_common.llm.prompt_templates import RAG_PROMPT, SYSTEM_PROMPT, TERRAFORM_PROMPT


class PromptBuilder:
    def build_context(self, chunks: list[dict]) -> str:
        if not chunks:
            return "No matching knowledge base context was retrieved."
        sections: list[str] = []
        for index, chunk in enumerate(chunks, start=1):
            metadata = chunk.get("metadata", {})
            title = metadata.get("title", "Unknown document")
            path = metadata.get("source_path", "unknown")
            sections.append(f"[{index}] {title} ({path})\n{chunk.get('content', '')}")
        return "\n\n---\n\n".join(sections)

    def build_rag_prompt(self, question: str, chunks: list[dict]) -> str:
        return RAG_PROMPT.format(system_prompt=SYSTEM_PROMPT, context=self.build_context(chunks), question=question)

    def build_terraform_prompt(self, question: str, chunks: list[dict]) -> str:
        return TERRAFORM_PROMPT.format(system_prompt=SYSTEM_PROMPT, context=self.build_context(chunks), question=question)

    def sources(self, chunks: list[dict]) -> list[dict]:
        sources: list[dict] = []
        seen: set[tuple[str, str]] = set()
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            key = (str(metadata.get("document_id", "")), str(metadata.get("source_path", "")))
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                {
                    "document_id": metadata.get("document_id", ""),
                    "title": metadata.get("title", "Unknown document"),
                    "path": metadata.get("source_path", ""),
                    "category": metadata.get("category", ""),
                }
            )
        return sources
