from fastapi import APIRouter, Depends

from backend.core.dependencies import get_pagination_filter
from backend.core.exceptions import NotFoundException
from backend.core.schemas import PaginationPydantic
from backend.schedule_item.dependencies import get_repository
from backend.schedule_item.repository import ScheduleItemRepository
from backend.schedule_item.schemas import ScheduleItemPydantic, ScheduleItemListPydantic

router = APIRouter(tags=["schedule-items"])


@router.get("/schedule-item", response_model=ScheduleItemListPydantic)
async def get_schedule_items(
    pagination: PaginationPydantic = Depends(get_pagination_filter),
    rep: ScheduleItemRepository = Depends(get_repository),
):
    schedule_items = await rep.get_multi(pagination)
    return ScheduleItemListPydantic(
        schedule_items=schedule_items,
        count=len(schedule_items)
    )


@router.get("/schedule-item/{item_id}", response_model=ScheduleItemPydantic)
async def get_schedule_items(
    item_id: int,
    rep: ScheduleItemRepository = Depends(get_repository),
):
    schedule_item = await rep.get_by_id(item_id)
    if not schedule_item:
        raise NotFoundException
    return schedule_item
