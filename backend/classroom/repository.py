from typing import Type

from backend.classroom import schemas, models
from backend.core.repository import BaseRepository


class ClassroomRepository(
    BaseRepository[
        models.Classroom,
        schemas.ClassroomPydantic,
        schemas.ClassroomInCreatePydantic,
        schemas.ClassroomInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Classroom]:
        return models.Classroom
