from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.bell.repository import BellRepository
from backend.core.database import get_session


async def get_repository(session: AsyncSession = Depends(get_session)):
    return BellRepository(session)
