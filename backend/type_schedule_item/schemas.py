from pydantic import BaseModel


class TypeScheduleItemBasePydantic(BaseModel):
    label: str


class TypeScheduleItemPydantic(TypeScheduleItemBasePydantic):
    id: int

    class Config:
        orm_mode = True


class TypeScheduleItemInCreatePydantic(TypeScheduleItemBasePydantic):
    pass


class TypeScheduleItemInUpdatePydantic(TypeScheduleItemBasePydantic):
    pass
