from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.classroom.repository import ClassroomRepository
from backend.classroom.schemas import ClassroomPydantic, ClassroomFilterPydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator


async def get_repository(session: AsyncSession = Depends(get_session)):
    return ClassroomRepository(session)


async def get_filter(
    group_id: int | None = None,
    subgroup_id: int | None = None
) -> ClassroomFilterPydantic:
    return ClassroomFilterPydantic(group_id=group_id, subgroup_id=subgroup_id)


router = RouterGenerator(
    prefix="/classroom",
    get_repository_function=get_repository,
    response_model=ClassroomPydantic,
    pagination=100
)


@router.get("/")
async def get_classroom(
    rep: ClassroomRepository = Depends(get_repository),
    filter_in: ClassroomFilterPydantic = Depends(get_filter)
):
    return await rep.get_for_group_or_subgroup(filter_in)
