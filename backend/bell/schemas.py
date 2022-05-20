from pydantic import BaseModel


class BellBasePydantic(BaseModel):
    time_beg: str
    time_end: str


class BellPydantic(BellBasePydantic):
    id: int

    class Config:
        orm_mode = True


class BellInCreatePydantic(BellBasePydantic):
    pass


class BellInUpdatePydantic(BellBasePydantic):
    pass
