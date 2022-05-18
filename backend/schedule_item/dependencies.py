from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.schedule_item.repository import ScheduleItemRepository


async def get_repository(session: AsyncSession = Depends(get_session)):
    return ScheduleItemRepository(session)
