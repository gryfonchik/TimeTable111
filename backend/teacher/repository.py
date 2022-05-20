from typing import Type

from sqlalchemy import select

from backend.core.repository import BaseRepository
from backend.course_teacher.models import course_teacher_table
from backend.teacher import schemas, models
from backend.teacher.schemas import TeacherFilterPydantic


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

    async def get_by_course(self, filter_in: TeacherFilterPydantic):
        q = select(self._model)
        if filter_in.course_id:
            q = q. \
                join(course_teacher_table). \
                filter(course_teacher_table.columns.course_id == filter_in.course_id)
        objs = await self.session.execute(q)
        return objs.scalars().all()
