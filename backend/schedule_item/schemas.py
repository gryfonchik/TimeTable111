from pydantic import BaseModel


class ScheduleItemBasePydantic(BaseModel):
    label: str


class ScheduleItemPydantic(ScheduleItemBasePydantic):
    id: int

    class Config:
        orm_mode = True


class ScheduleItemInCreatePydantic(ScheduleItemBasePydantic):
    pass


class ScheduleItemInUpdatePydantic(ScheduleItemBasePydantic):
    pass


class ScheduleItemListPydantic(BaseModel):
    schedule_items: list[ScheduleItemPydantic]
    count: int
