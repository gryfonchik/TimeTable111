from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import selectable

from backend.core.repository import BaseRepository
from backend.schedule_item import schemas, models


class ScheduleItemRepository(
    BaseRepository[
        models.ScheduleItem,
        schemas.ScheduleItemPydantic,
        schemas.ScheduleItemInCreatePydantic,
        schemas.ScheduleItemInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.ScheduleItem]:
        return models.ScheduleItem

    def get_query(self) -> selectable:
        return select(models.ScheduleItem).options(  # noqa
            selectinload(models.ScheduleItem.course),
            selectinload(models.ScheduleItem.teacher),
            selectinload(models.ScheduleItem.bell),
            selectinload(models.ScheduleItem.group),
            selectinload(models.ScheduleItem.subgroup),
            selectinload(models.ScheduleItem.type_schedule_item),
            selectinload(models.ScheduleItem.classroom),
            selectinload(models.ScheduleItem.week),
        )
