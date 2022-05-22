import asyncio
import csv

from backend.bell.repository import BellRepository
from backend.bell.schemas import BellInCreatePydantic
from backend.classroom.models import Classroom  # noqa
from backend.classroom.repository import ClassroomRepository
from backend.classroom.schemas import ClassroomInCreatePydantic
from backend.core.database import async_session, Base
from backend.course.repository import CourseRepository
from backend.course.schemas import CourseInCreatePydantic
from backend.group.repository import GroupRepository, SubgroupRepository
from backend.group.schemas import GroupInCreatePydantic, SubgroupInCreatePydantic
from backend.teacher.repository import TeacherRepository
from backend.teacher.schemas import TeacherInCreatePydantic
from backend.teacher_wish.repository import TeacherWishRepository
from backend.teacher_wish.schemas import TeacherWishInCreatePydantic
from backend.type_schedule_item.repository import TypeScheduleItemRepository
from backend.type_schedule_item.schemas import TypeScheduleItemInCreatePydantic
from backend.week.repository import WeekRepository
from backend.week.schemas import WeekInCreatePydantic


def get_rows_from_csv(filename):
    rows = []
    with open(filename) as file:
        for row in csv.DictReader(file):
            rows.append(row)
    return rows


async def create_from_csv(filename, session, rep_class, in_create_class):
    result = []
    rep = rep_class(session)
    for row in get_rows_from_csv(filename):
        obj_in = in_create_class(**row)
        obj = await rep.create(schema_in=obj_in)
        result.append(obj)
    return result


async def create_course_teacher_relation_from_csv(filename, session, courses, teachers):
    for row in get_rows_from_csv(filename):
        course = courses[int(row['id_course']) - 1]
        teacher = teachers[int(row['id_teacher']) - 1]
        teacher.courses.append(course)
        session.add(teacher)
    await session.commit()


async def create_teacher_wishes_from_csv(filename, session, teachers, bells, weeks):
    rep = TeacherWishRepository(session)
    for row in get_rows_from_csv(filename):
        teacher = teachers[int(row['teacher_id']) - 1]
        bell = bells[int(row['bell_id']) - 1]
        week = weeks[int(row["week_id"]) - 1]
        await rep.create(TeacherWishInCreatePydantic(
            teacher_id=teacher.id,
            bell_id=bell.id,
            week_id=week.id,
            day_of_week=int(row['day_of_week'])
        ), commit=True)
    await session.commit()


async def division_into_subgroups(session, groups):
    rep = SubgroupRepository(session)
    for group in groups:
        sub_groups_count = group.count // 20
        for _ in range(sub_groups_count):
            await rep.create(SubgroupInCreatePydantic(
                group_id=group.id,
                count=20
            ))
        remaining_count = group.count - sub_groups_count * 20
        if remaining_count > 0:
            await rep.create(SubgroupInCreatePydantic(
                group_id=group.id,
                count=remaining_count
            ))


async def clear_data(session):
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        await session.execute(table.delete())
    await session.commit()


async def generate(teachers, bells, courses, groups, weeks):
    def create_week_object():
        result = dict()
        for i in range(6):
            result[i] = dict()
        return result

    timetable = {
        1: create_week_object(),
        2: create_week_object()
    }

    return timetable


async def main():
    async with async_session() as session:
        await clear_data(session)
        teachers = await create_from_csv("schedule_generator/input_data/teachers.csv", session, TeacherRepository,
                                         TeacherInCreatePydantic)
        bells = await create_from_csv("schedule_generator/input_data/bells.csv", session, BellRepository,
                                      BellInCreatePydantic)
        courses = await create_from_csv("schedule_generator/input_data/courses.csv", session, CourseRepository,
                                        CourseInCreatePydantic)
        await create_from_csv("schedule_generator/input_data/types_schedule_item.csv", session,
                              TypeScheduleItemRepository, TypeScheduleItemInCreatePydantic)
        groups = await create_from_csv("schedule_generator/input_data/groups.csv", session, GroupRepository,
                                       GroupInCreatePydantic)
        await create_course_teacher_relation_from_csv("schedule_generator/input_data/course_teacher.csv", session,
                                                      courses, teachers)
        weeks = await create_from_csv("schedule_generator/input_data/weeks.csv", session, WeekRepository,
                                      WeekInCreatePydantic)
        await create_from_csv("schedule_generator/input_data/classrooms.csv", session, ClassroomRepository,
                              ClassroomInCreatePydantic)
        await create_teacher_wishes_from_csv("schedule_generator/input_data/teacher_wishes.csv",
                                             session, teachers=teachers, bells=bells, weeks=weeks)
        await division_into_subgroups(session, groups)
        await generate(teachers, bells, courses, groups, weeks)


if __name__ == "__main__":
    asyncio.run(main())
