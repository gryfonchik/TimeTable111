from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator
from backend.type_schedule_item.repository import TypeScheduleItemRepository
from backend.type_schedule_item.schemas import TypeScheduleItemPydantic


async def get_repository(session: AsyncSession = Depends(get_session)):
    return TypeScheduleItemRepository(session)


router = RouterGenerator(
    prefix="/type-schedule-item",
    get_repository_function=get_repository,
    response_model=TypeScheduleItemPydantic,
    pagination=None
)
