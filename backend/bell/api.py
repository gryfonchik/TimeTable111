from fastapi import APIRouter, Depends

from backend.bell.dependencies import get_repository
from backend.bell.repository import BellRepository
from backend.bell.schemas import BellPydantic, BellInCreatePydantic, BellListPydantic, BellInUpdatePydantic
from backend.core.dependencies import get_pagination_filter
from backend.core.exceptions import NotFoundException
from backend.core.schemas import PaginationPydantic

router = APIRouter(tags=["bell"])


@router.get("/bells", response_model=BellListPydantic)
async def get_bells(
    pagination: PaginationPydantic = Depends(get_pagination_filter),
    rep: BellRepository = Depends(get_repository)
):
    bells = await rep.get_multi(pagination)
    return BellListPydantic(
        bells=bells,
        count=len(bells)
    )


@router.get("/bell/{item_id}", response_model=BellPydantic)
async def get_bell(
    item_id: int,
    rep: BellRepository = Depends(get_repository)
):
    obj = await rep.get_by_id(item_id)
    if not obj:
        raise NotFoundException
    return obj
