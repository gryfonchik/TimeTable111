from typing import Type

from backend.core.repository import BaseRepository
from backend.teacher import schemas, models


class TeacherRepository(
    BaseRepository[
        models.Teacher,
        schemas.TeacherPydantic,
        schemas.TeacherInCreatePydantic,
        schemas.TeacherInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Teacher]:
        return models.Teacher
