from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.course.repository import CourseRepository
from backend.course.schemas import CoursePydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator


async def get_repository(session: AsyncSession = Depends(get_session)):
    return CourseRepository(session)


router = RouterGenerator(
    prefix="/course",
    get_repository_function=get_repository,
    response_model=CoursePydantic,
    pagination=None
)
