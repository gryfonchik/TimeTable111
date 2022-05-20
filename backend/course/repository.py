from typing import Type

from backend.course import schemas, models
from backend.core.repository import BaseRepository


class CourseRepository(
    BaseRepository[
        models.Course,
        schemas.CoursePydantic,
        schemas.CourseInCreatePydantic,
        schemas.CourseInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Course]:
        return models.Course
