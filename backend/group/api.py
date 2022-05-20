from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.group.repository import GroupRepository
from backend.group.schemas import GroupPydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator


async def get_repository(session: AsyncSession = Depends(get_session)):
    return GroupRepository(session)


router = RouterGenerator(
    prefix="/group",
    get_repository_function=get_repository,
    response_model=GroupPydantic,
    pagination=None
)
