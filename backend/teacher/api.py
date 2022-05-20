from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator
from backend.teacher.repository import TeacherRepository
from backend.teacher.schemas import TeacherPydantic, TeacherFilterPydantic
from backend.core.schemas import ListPydantic


async def get_repository(session: AsyncSession = Depends(get_session)):
    return TeacherRepository(session)


async def get_filter(course_id: int | None = None):
    return TeacherFilterPydantic(course_id=course_id)


router = RouterGenerator(
    prefix="/teacher",
    get_repository_function=get_repository,
    response_model=TeacherPydantic,
    pagination=None
)


@router.get("/", response_model=ListPydantic[TeacherPydantic])
async def get_teachers(
    rep: TeacherRepository = Depends(get_repository),
    filter_in: TeacherFilterPydantic = Depends(get_filter)
):
    return ListPydantic[TeacherPydantic](
        items=(await rep.get_by_course(filter_in))
    )
