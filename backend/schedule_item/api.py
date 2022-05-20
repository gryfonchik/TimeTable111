from datetime import date

from fastapi import Depends

from backend.core.router_generator import RouterGenerator
from backend.core.schemas import ListPydantic
from backend.schedule_item.dependencies import get_repository
from backend.schedule_item.repository import ScheduleItemRepository
from backend.schedule_item.schemas import ScheduleItemPydantic, ScheduleItemFilterPydantic


def get_filter(
    classroom_id: int | None = None,
    course_id: int | None = None,
    group_id: int | None = None,
    subgroup_id: int | None = None,
    teacher_id: int | None = None,
    date_beg: date | None = None,
    date_end: date | None = None,
):
    return ScheduleItemFilterPydantic(
        classroom_id=classroom_id,
        course_id=course_id,
        group_id=group_id,
        subgroup_id=subgroup_id,
        teacher_id=teacher_id,
        date_beg=date_beg,
        date_end=date_end
    )


router = RouterGenerator(
    prefix="/schedule-item",
    get_repository_function=get_repository,
    response_model=ScheduleItemPydantic,
    pagination=None
)


@router.get("/", response_model=ListPydantic[ScheduleItemPydantic])
async def get_schedule_items(
    rep: ScheduleItemRepository = Depends(get_repository),
    filter_in: ScheduleItemFilterPydantic = Depends(get_filter)
):
    return ListPydantic(
        items=(await rep.get_filtered(filter_in))
    )
