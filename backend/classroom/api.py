from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.classroom.repository import ClassroomRepository
from backend.classroom.schemas import ClassroomPydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator


async def get_repository(session: AsyncSession = Depends(get_session)):
    return ClassroomRepository(session)


router = RouterGenerator(
    prefix="/classroom",
    get_repository_function=get_repository,
    response_model=ClassroomPydantic,
    pagination=100
)
