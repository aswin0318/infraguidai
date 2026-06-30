import time
from functools import lru_cache
from typing import Any

import httpx
from fastapi import APIRouter, Depends, HTTPException, Header
from jose import JWTError, jwt

from infraguid_common.config.settings import get_settings
from infraguid_common.database.postgres_client import get_db_session
from infraguid_common.database.repositories.user_repo import UserRepository
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()

_jwks_cache: dict[str, Any] = {}
_jwks_cache_time: float = 0
_JWKS_CACHE_TTL = 3600  # 1 hour


def _get_jwks_url() -> str:
    region = settings.cognito_region
    pool_id = settings.cognito_user_pool_id
    return f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"


def _get_issuer() -> str:
    region = settings.cognito_region
    pool_id = settings.cognito_user_pool_id
    return f"https://cognito-idp.{region}.amazonaws.com/{pool_id}"


@lru_cache(maxsize=1)
def _fetch_jwks_cached(url: str) -> dict[str, Any]:
    """Fetch JWKS from Cognito and cache the result."""
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def _get_jwks() -> dict[str, Any]:
    """Get JWKS with TTL-based cache refresh."""
    global _jwks_cache, _jwks_cache_time
    now = time.time()
    if _jwks_cache and (now - _jwks_cache_time) < _JWKS_CACHE_TTL:
        return _jwks_cache
    url = _get_jwks_url()
    _jwks_cache = _fetch_jwks_cached.__wrapped__(url)
    _jwks_cache_time = now
    return _jwks_cache


def _find_key(kid: str) -> dict[str, Any] | None:
    jwks = _get_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None


def verify_cognito_token(token: str) -> dict[str, Any]:
    """Verify a Cognito JWT token and return the claims."""
    if not settings.cognito_configured:
        raise HTTPException(status_code=503, detail="Cognito is not configured")

    try:
        headers = jwt.get_unverified_headers(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Token missing key ID")

        key = _find_key(kid)
        if key is None:
            raise HTTPException(status_code=401, detail="Token key not found in JWKS")

        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.cognito_app_client_id,
            issuer=_get_issuer(),
            options={"verify_at_hash": False},
        )
        return claims
    except JWTError as exc:
        logger.warning("cognito_token_verification_failed", error=str(exc))
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format. Use: Bearer <token>")
    return parts[1]


async def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    """FastAPI dependency: extract and verify the Cognito token, return user claims."""
    token = _extract_bearer_token(authorization)
    claims = verify_cognito_token(token)
    return {
        "user_id": claims.get("sub", ""),
        "email": claims.get("email", ""),
        "name": claims.get("name", claims.get("cognito:username", "")),
        "role": claims.get("custom:role", "user"),
    }


@router.get("/me")
async def me(user: dict = Depends(get_current_user)) -> dict:
    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }


@router.post("/sync")
async def sync_user(
    user: dict = Depends(get_current_user),
    session=Depends(get_db_session),
) -> dict:
    """Sync the authenticated Cognito user to the local database.
    Called automatically by the frontend after login."""
    repo = UserRepository(session)
    db_user = await repo.upsert_user(
        user_id=user["user_id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
    )
    return {"status": "synced", "user": db_user}
