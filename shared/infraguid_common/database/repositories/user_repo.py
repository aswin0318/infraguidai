from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infraguid_common.database.models import User
from infraguid_common.observability.logger import get_logger

logger = get_logger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_email(self, email: str) -> dict | None:
        stmt = select(User).where(User.email == email.lower().strip())
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            return None
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        }

    async def find_by_id(self, user_id: str) -> dict | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            return None
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        }

    async def upsert_user(self, user_id: str, name: str, email: str, role: str = "user") -> dict:
        user = User(id=user_id, name=name, email=email.lower().strip(), role=role)
        merged = await self._session.merge(user)
        await self._session.flush()
        logger.info("user_upserted", email=merged.email, role=merged.role)
        return {"id": merged.id, "name": merged.name, "email": merged.email, "role": merged.role}
