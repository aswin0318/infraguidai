from infraguid_common.llm.bedrock import get_chat_model
from infraguid_common.observability.logger import get_logger

from app.rag.prompt_builder import PromptBuilder
from app.rag.retriever import KnowledgeRetriever

logger = get_logger(__name__)


def message_text(message) -> str:
    """Extract plain text from a LangChain AIMessage (string or content-block list)."""
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(p for p in parts if p).strip()
    return str(content).strip()


class RagPipeline:
    def __init__(self) -> None:
        self.retriever = KnowledgeRetriever()
        self.prompt_builder = PromptBuilder()

    async def answer(self, question: str) -> dict:
        chunks = await self.retriever.retrieve(question)
        if not chunks:
            return {
                "answer": "I could not find relevant knowledge base content for that question. Re-ingest the knowledge base or ask about company standards, AWS guides, Terraform, deployments, or incidents.",
                "sources": [],
            }
        prompt = self.prompt_builder.build_rag_prompt(question, chunks)
        response = await get_chat_model(temperature=0.2, max_tokens=4096).ainvoke(prompt)
        return {"answer": message_text(response), "sources": self.prompt_builder.sources(chunks)}

    async def terraform(self, question: str) -> dict:
        query = f"Terraform standards AWS provider module catalog reference architectures {question}"
        chunks = await self.retriever.retrieve(query, top_k=5)
        prompt = self.prompt_builder.build_terraform_prompt(question, chunks)
        response = await get_chat_model(temperature=0.2, max_tokens=4096).ainvoke(prompt)
        return {"answer": message_text(response), "sources": self.prompt_builder.sources(chunks)}
