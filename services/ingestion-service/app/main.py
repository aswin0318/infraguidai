from contextlib import asynccontextmanager

from fastapi import FastAPI

from infraguid_common.database.postgres_client import dispose_engine, init_db
from infraguid_common.observability.logger import configure_logging, get_logger

from app.api.routes import router

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ingestion-service owns the schema: ensure tables + pgvector extension exist.
    try:
        await init_db()
    except Exception as exc:
        logger.warning("database_initialization_error", error=str(exc))
    yield
    await dispose_engine()


app = FastAPI(
    title="InfraGuidAI Ingestion Service",
    description="Document load, chunk, embed (LangChain AWS), and pgvector upsert.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
async def root() -> dict:
    return {"service": "ingestion-service", "status": "running"}
