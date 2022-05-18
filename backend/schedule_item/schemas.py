from pydantic import BaseModel

from backend.bell.schemas import BellPydantic
from backend.classroom.schemas import ClassroomPydantic
from backend.course.schemas import CoursePydantic
from backend.group.schemas import GroupPydantic, SubgroupPydantic
from backend.teacher.schemas import TeacherPydantic
from backend.type_schedule_item.schemas import TypeScheduleItemPydantic
from backend.week.schemas import WeekPydantic


class ScheduleItemBasePydantic(BaseModel):
    pass


class ScheduleItemPydantic(ScheduleItemBasePydantic):
    id: int
    course: CoursePydantic
    teacher: TeacherPydantic
    bell: BellPydantic
    group: GroupPydantic | None
    subgroup: SubgroupPydantic | None
    type_schedule_item: TypeScheduleItemPydantic
    classroom: ClassroomPydantic
    week: WeekPydantic

    class Config:
        orm_mode = True


class ScheduleItemInCreatePydantic(ScheduleItemBasePydantic):
    pass


class ScheduleItemInUpdatePydantic(ScheduleItemBasePydantic):
    pass


class ScheduleItemListPydantic(BaseModel):
    schedule_items: list[ScheduleItemPydantic]
    count: int
