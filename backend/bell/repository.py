from typing import Type

from backend.bell import schemas, models
from backend.core.repository import BaseRepository


class BellRepository(
    BaseRepository[
        models.Bell,
        schemas.BellPydantic,
        schemas.BellInCreatePydantic,
        schemas.BellInUpdatePydantic
    ]
):
    @property
    def _create_schema(self) -> Type[schemas.BellInCreatePydantic]:
        return schemas.BellInCreatePydantic

    @property
    def _update_schema(self) -> Type[schemas.BellInUpdatePydantic]:
        return schemas.BellInUpdatePydantic

    @property
    def _schema(self) -> Type[schemas.BellPydantic]:
        return schemas.BellPydantic

    @property
    def _model(self) -> Type[models.Bell]:
        return models.Bell
