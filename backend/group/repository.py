from typing import Type

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import selectable, select

from backend.core.repository import BaseRepository
from backend.group import schemas, models


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
