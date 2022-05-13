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
    def _model(self) -> Type[models.Bell]:
        return models.Bell
