from contextlib import asynccontextmanager

from fastapi import FastAPI

from infraguid_common.database.postgres_client import dispose_engine
from infraguid_common.observability.logger import configure_logging, get_logger

from app.api.routes import router

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("rag_service_starting")
    yield
    await dispose_engine()


app = FastAPI(
    title="InfraGuidAI RAG Service",
    description="Embedding + pgvector retrieval and RAG generation (LangChain AWS).",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
async def root() -> dict:
    return {"service": "rag-service", "status": "running"}
