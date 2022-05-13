from typing import Type

from backend.core.repository import BaseRepository
from backend.week import schemas, models


class WeekRepository(
    BaseRepository[
        models.Week,
        schemas.WeekPydantic,
        schemas.WeekInCreatePydantic,
        schemas.WeekInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Week]:
        return models.Week
