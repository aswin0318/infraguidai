from infraguid_common.llm.bedrock import get_embeddings


class DocumentEmbedder:
    def __init__(self) -> None:
        self.embeddings = get_embeddings()

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return await self.embeddings.aembed_documents(texts)
