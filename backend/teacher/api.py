from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator
from backend.teacher.repository import TeacherRepository
from backend.teacher.schemas import TeacherPydantic


async def get_repository(session: AsyncSession = Depends(get_session)):
    return TeacherRepository(session)


router = RouterGenerator(
    prefix="/teacher",
    get_repository_function=get_repository,
    response_model=TeacherPydantic,
    pagination=None
)
