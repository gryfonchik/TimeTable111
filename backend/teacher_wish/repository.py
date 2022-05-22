from typing import Type

from backend.core.repository import BaseRepository
from backend.teacher_wish import schemas, models


class TeacherWishRepository(
    BaseRepository[
        models.TeacherWish,
        schemas.TeacherWishPydantic,
        schemas.TeacherWishInCreatePydantic,
        schemas.TeacherWishInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.TeacherWish]:
        return models.TeacherWish
