from backend.core.router_generator import RouterGenerator
from backend.schedule_item.dependencies import get_repository
from backend.schedule_item.schemas import ScheduleItemPydantic

router = RouterGenerator(
    prefix="/schedule-item",
    get_repository_function=get_repository,
    response_model=ScheduleItemPydantic,
    pagination=None
)
