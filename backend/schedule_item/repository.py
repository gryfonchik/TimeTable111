from typing import Type

from sqlalchemy import select, extract
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import selectable

from backend.classroom.models import Classroom
from backend.core.repository import BaseRepository
from backend.course.models import Course
from backend.group.models import Group, Subgroup
from backend.schedule_item import schemas, models
from backend.schedule_item.schemas import ScheduleItemFilterPydantic
from backend.teacher.models import Teacher


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
        return select(self._model).options(  # noqa
            selectinload(models.ScheduleItem.course),
            selectinload(models.ScheduleItem.teacher),
            selectinload(models.ScheduleItem.bell),
            selectinload(models.ScheduleItem.group),
            selectinload(models.ScheduleItem.subgroup),
            selectinload(models.ScheduleItem.type_schedule_item),
            selectinload(models.ScheduleItem.classroom),
            selectinload(models.ScheduleItem.week),
        )

    async def get_filtered(self, filter_in: ScheduleItemFilterPydantic):
        q = self.get_query()

        if filter_in.classroom_id:
            q = q.join(Classroom).filter(Classroom.id == filter_in.classroom_id)

        if filter_in.course_id:
            q = q.join(Course).filter(Course.id == filter_in.course_id)

        if filter_in.group_id:
            q = q.join(Group).filter(Group.id == filter_in.group_id)

        if filter_in.subgroup_id:
            q = q.join(Subgroup).filter(Subgroup.id == filter_in.subgroup_id)

        if filter_in.teacher_id:
            q = q.join(Teacher).filter(Teacher.id == filter_in.teacher_id)

        if filter_in.date_beg:
            q = q.filter(self._model.date >= filter_in.date_beg)

        if filter_in.date_end:
            q = q.filter(self._model.date <= filter_in.date_end)

        if filter_in.week_number:
            q = q.filter(extract('week', self._model.date) == filter_in.week_number)

        objs = await self.session.execute(q)
        return objs.scalars().all()
