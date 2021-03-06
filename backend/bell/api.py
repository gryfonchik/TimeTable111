from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.bell.repository import BellRepository
from backend.bell.schemas import BellPydantic
from backend.core.database import get_session
from backend.core.router_generator import RouterGenerator


async def get_repository(session: AsyncSession = Depends(get_session)):
    return BellRepository(session)


router = RouterGenerator(
    prefix="/bell",
    get_repository_function=get_repository,
    response_model=BellPydantic,
    pagination=None
)
