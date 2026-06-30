import time
from collections.abc import Callable

from fastapi import Request, Response
from structlog.contextvars import bind_contextvars, clear_contextvars

from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)


async def request_logging_middleware(request: Request, call_next: Callable) -> Response:
    clear_contextvars()
    bind_contextvars(method=request.method, path=request.url.path)
    started = time.perf_counter()
    try:
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info("request_complete", status_code=response.status_code, elapsed_ms=elapsed_ms)
        return response
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.error("request_failed", elapsed_ms=elapsed_ms, error=str(exc))
        raise
    finally:
        clear_contextvars()
