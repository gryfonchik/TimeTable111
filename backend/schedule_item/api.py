from datetime import date

from fastapi import Depends, HTTPException, status

from backend.bell.repository import BellRepository
from backend.core.exceptions import NotFoundException
from backend.core.router_generator import RouterGenerator
from backend.core.schemas import ListPydantic
from backend.schedule_item.dependencies import get_repository
from backend.schedule_item.repository import ScheduleItemRepository, CollisionException
from backend.schedule_item.schemas import ScheduleItemPydantic, ScheduleItemFilterPydantic, ScheduleItemInUpdatePydantic
from backend.bell.api import get_repository as get_bell_repository


def get_filter(
    year: int,
    week_number: int,
    group_id: int | None = None,
    teacher_id: int | None = None,
):
    return ScheduleItemFilterPydantic(
            group_id=group_id,
            teacher_id=teacher_id,
            year=year,
            week_number=week_number
        )


router = RouterGenerator(
    prefix="/schedule-item",
    get_repository_function=get_repository,
    response_model=ScheduleItemPydantic,
    pagination=None
)


@router.get("/", response_model=dict[str, dict[str, list[ScheduleItemPydantic]]])
async def get_schedule_items(
    rep: ScheduleItemRepository = Depends(get_repository),
    rep_bell: BellRepository = Depends(get_bell_repository),
    filter_in: ScheduleItemFilterPydantic = Depends(get_filter)
):
    bells = {
        item.time_beg: i + 1
        for i, item in enumerate(await rep_bell.get_multi())
    }
    res = {
        str(date.fromisocalendar(filter_in.year, filter_in.week_number, day_of_week)): {
            int(bell): [] for bell in range(1, 9)
        } for day_of_week in range(1, 7)
    }
    schedule_items = await rep.get_filtered(None, filter_in=filter_in)
    for schedule_item in schedule_items:
        res[str(schedule_item.date)][bells[schedule_item.bell.time_beg]].append(schedule_item)
    return res


@router.put("/{item_id}")
async def update_schedule_item(
    item_id: int,
    obj_in: ScheduleItemInUpdatePydantic,
    rep: ScheduleItemRepository = Depends(get_repository)
):
    obj = await rep.get_by_id(item_id)
    if not obj:
        raise NotFoundException
    try:
        return await rep.update(obj, obj_in)
    except CollisionException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.__class__.__name__
        )
