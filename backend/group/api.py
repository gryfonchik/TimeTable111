from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator
from backend.group.repository import GroupRepository, SubgroupRepository
from backend.group.schemas import GroupPydantic, SubgroupPydantic


async def get_repository(session: AsyncSession = Depends(get_session)):
    return GroupRepository(session)


async def get_repository_subgroup(session: AsyncSession = Depends(get_session)):
    return SubgroupRepository(session)


router = APIRouter()

router.include_router(RouterGenerator(
    prefix="/group",
    get_repository_function=get_repository,
    response_model=GroupPydantic,
    pagination=None
))

router.include_router(RouterGenerator(
    prefix="/subgroup",
    get_repository_function=get_repository_subgroup,
    response_model=SubgroupPydantic,
    pagination=None
))
