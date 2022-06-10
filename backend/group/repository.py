from typing import Type

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import selectable, select

from backend.core.repository import BaseRepository
from backend.group import schemas, models
from backend.group.schemas import SubgroupFilterPydantic


class GroupRepository(
    BaseRepository[
        models.Group,
        schemas.GroupPydantic,
        schemas.GroupInCreatePydantic,
        schemas.GroupInUpdatePydantic
    ]
):

    @property
    def _model(self) -> Type[models.Group]:
        return models.Group


class SubgroupRepository(
    BaseRepository[
        models.Subgroup,
        schemas.SubgroupPydantic,
        schemas.SubgroupInCreatePydantic,
        schemas.SubgroupInUpdatePydantic
    ]
):

    def get_query(self) -> selectable:
        return select(self._model).options(  # noqa
            selectinload(self._model.group),
        )

    @property
    def _model(self) -> Type[models.Subgroup]:
        return models.Subgroup

    async def get_filtered(self, filter_in: SubgroupFilterPydantic):
        q = self.get_query()

        if filter_in.group_id:
            q = q.join(models.Group).filter(models.Group.id == filter_in.group_id)

        objs = await self.session.execute(q)
        return objs.scalars().all()
