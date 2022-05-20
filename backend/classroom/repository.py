from typing import Type

from sqlalchemy import select

from backend.classroom import schemas, models
from backend.classroom.schemas import ClassroomFilterPydantic
from backend.core.repository import BaseRepository
from backend.group.models import Group, Subgroup


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

    async def get_for_group_or_subgroup(self, filter_in: ClassroomFilterPydantic):
        q = select(self._model) # noqa
        if filter_in.group_id:
            count: int = (await self.session.execute(
                select(Group.count).filter(Group.id == filter_in.group_id)
            )).scalars().first()
            q = q.filter(self._model.capacity >= count)
        if filter_in.subgroup_id:
            count = (await self.session.execute(
                select(Subgroup.count).filter(Subgroup.id == filter_in.subgroup_id)
            )).scalars().first()
            q = q.filter(self._model.capacity >= count)
        objs = await self.session.execute(q)
        return objs.scalars().all()
