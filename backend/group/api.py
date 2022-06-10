from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator
from backend.core.schemas import ListPydantic
from backend.group.repository import GroupRepository, SubgroupRepository
from backend.group.schemas import GroupPydantic, SubgroupPydantic, SubgroupFilterPydantic


async def get_repository(session: AsyncSession = Depends(get_session)):
    return GroupRepository(session)


async def get_repository_subgroup(session: AsyncSession = Depends(get_session)):
    return SubgroupRepository(session)


async def get_subgroup_filter(group_id: int | None = None) -> SubgroupFilterPydantic:
    return SubgroupFilterPydantic(
        group_id=group_id
    )


router = APIRouter()

router.include_router(RouterGenerator(
    prefix="/group",
    get_repository_function=get_repository,
    response_model=GroupPydantic,
    pagination=None
))

subgroup_router = RouterGenerator(
    prefix="/subgroup",
    get_repository_function=get_repository_subgroup,
    response_model=SubgroupPydantic,
    pagination=None
)


@subgroup_router.get("/", response_model=ListPydantic[SubgroupPydantic])
async def get_subgroups(
    filter_in: SubgroupFilterPydantic = Depends(get_subgroup_filter),
    rep: SubgroupRepository = Depends(get_repository_subgroup),
):
    return ListPydantic(
        items=await rep.get_filtered(filter_in)
    )

router.include_router(subgroup_router)
