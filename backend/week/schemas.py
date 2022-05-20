from pydantic import BaseModel


class WeekBasePydantic(BaseModel):
    label: str


class WeekPydantic(WeekBasePydantic):
    id: int

    class Config:
        orm_mode = True


class WeekInCreatePydantic(WeekBasePydantic):
    pass


class WeekInUpdatePydantic(WeekBasePydantic):
    pass
