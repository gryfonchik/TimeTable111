from typing import Type

from sqlalchemy import select, extract, distinct, func
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import selectable, or_
from sqlalchemy.dialects.postgresql import array_agg

from backend.bell.models import Bell
from backend.classroom.models import Classroom
from backend.core.repository import BaseRepository
from backend.core.schemas import PaginationPydantic
from backend.course.models import Course
from backend.group.models import Group, Subgroup
from backend.schedule_item import schemas, models
from backend.schedule_item.schemas import ScheduleItemFilterPydantic
from backend.teacher.models import Teacher


class CollisionException(Exception):
    pass


class CollisionTeacherException(CollisionException):
    pass


class CollisionGroupException(CollisionException):
    pass


class CollisionSubgroupException(CollisionException):
    pass


class CollisionClassroomException(CollisionException):
    pass


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

    async def update(
        self,
        obj: models.ScheduleItem,
        obj_in: schemas.ScheduleItemInUpdatePydantic,
        commit: bool = True
    ) -> models.ScheduleItem:
        query = self.get_query().join(Bell). \
            filter(self._model.id != obj.id). \
            filter(self._model.date == obj_in.date). \
            filter(Bell.id == obj_in.bell_id)

        if (
            obj_in.teacher_id and
            (await self.session.execute(query.join(Teacher).filter(Teacher.id == obj_in.teacher_id))).
                scalars().first()
        ):
            raise CollisionTeacherException()

        if (
            obj_in.group_id and
            (await self.session.execute(query.join(Group).filter(Group.id == obj_in.group_id))).
                scalars().first()
        ):
            raise CollisionGroupException()

        if (
            obj_in.subgroup_id and
            (await self.session.execute(query.join(Subgroup).filter(Subgroup.id == obj_in.subgroup_id))).
                scalars().first()
        ):
            raise CollisionSubgroupException()

        if (
            obj_in.classroom_id and
            (await self.session.execute(query.join(Classroom).filter(Classroom.id == obj_in.classroom_id))).
                scalars().first()
        ):
            raise CollisionClassroomException()

        return await super().update(obj, obj_in)

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

    async def get_filtered(self, pagination: PaginationPydantic | None, filter_in: ScheduleItemFilterPydantic
                           ) -> list[models.ScheduleItem]:
        q = self.get_query()

        if filter_in.group_id:
            q = q.join(Group).join(Subgroup).filter(or_(
                Group.id == filter_in.group_id,
                Subgroup.group_id == filter_in.group_id
            ))

        if filter_in.teacher_id:
            q = q.join(Teacher).filter(Teacher.id == filter_in.teacher_id)

        if filter_in.week_number:
            q = q.filter(extract('week', self._model.date) == filter_in.week_number)

        if filter_in.year:
            q = q.filter(extract('year', self._model.date) == filter_in.year)

        if pagination:
            q = q.offset(pagination.offset).limit(pagination.limit)

        q = q.distinct()

        objs = await self.session.execute(q)
        return objs.scalars().all()
