from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from infraguid_common.config.settings import get_settings
from infraguid_common.database.models import Base
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)

_engine = None
_async_session_factory = None


def _get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.postgres_uri,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30,
            echo=False,
        )
    return _engine


def _get_session_factory():
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(
            bind=_get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


async def init_db() -> None:
    """Create all tables and enable pgvector extension."""
    engine = _get_engine()
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    logger.info("postgresql_tables_ready")


async def dispose_engine() -> None:
    """Dispose the engine connection pool on shutdown."""
    global _engine, _async_session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
        logger.info("postgresql_engine_disposed")


async def get_db_session():
    """FastAPI dependency that yields an async database session."""
    factory = _get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def ping_db() -> dict:
    """Health check ping for PostgreSQL."""
    engine = _get_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        result.fetchone()
    return {"status": "healthy"}
