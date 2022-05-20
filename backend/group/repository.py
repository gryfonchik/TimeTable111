from typing import Type

from backend.group import schemas, models
from backend.core.repository import BaseRepository


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
