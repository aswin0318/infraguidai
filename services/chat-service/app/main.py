from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infraguid_common.cache.redis_client import close_redis
from infraguid_common.config.settings import get_settings
from infraguid_common.database.postgres_client import dispose_engine, init_db
from infraguid_common.observability.logger import configure_logging, get_logger

from app.api.middleware.request_logging import request_logging_middleware
from app.api.routes import admin, auth, chat, documents, health

configure_logging()
settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception as exc:
        logger.warning("database_initialization_error", error=str(exc))
    yield
    await close_redis()
    await dispose_engine()


app = FastAPI(
    title="InfraGuidAI Chat Service",
    description="Public entry service: chat, auth (Cognito), documents, and admin. Delegates reasoning to the agent-service.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_logging_middleware)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(admin.router)


@app.get("/")
async def root() -> dict:
    return {"service": "InfraGuidAI", "status": "running", "version": "2.0.0", "docs": "/api/docs"}
