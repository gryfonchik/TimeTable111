from typing import Type

from backend.core.repository import BaseRepository
from backend.type_schedule_item import schemas, models


class TypeScheduleItemRepository(
    BaseRepository[
        models.TypeScheduleItem,
        schemas.TypeScheduleItemPydantic,
        schemas.TypeScheduleItemInCreatePydantic,
        schemas.TypeScheduleItemInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.TypeScheduleItem]:
        return models.TypeScheduleItem
