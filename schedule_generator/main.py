import asyncio
import csv
import datetime

from pydantic import BaseModel
from sqlalchemy import select

from backend.course_teacher.models import course_teacher_table
from backend.bell.repository import BellRepository
from backend.bell.schemas import BellInCreatePydantic
from backend.classroom.models import Classroom  # noqa
from backend.classroom.repository import ClassroomRepository
from backend.classroom.schemas import ClassroomInCreatePydantic
from backend.core.database import async_session, Base
from backend.course.repository import CourseRepository
from backend.course.schemas import CourseInCreatePydantic
from backend.group.models import Subgroup
from backend.group.repository import GroupRepository, SubgroupRepository
from backend.group.schemas import GroupInCreatePydantic, SubgroupInCreatePydantic
from backend.schedule_item.repository import ScheduleItemRepository
from backend.schedule_item.schemas import ScheduleItemInCreatePydantic
from backend.teacher.repository import TeacherRepository
from backend.teacher.schemas import TeacherInCreatePydantic
from backend.teacher_wish.repository import TeacherWishRepository
from backend.teacher_wish.schemas import TeacherWishInCreatePydantic
from backend.type_schedule_item.repository import TypeScheduleItemRepository
from backend.type_schedule_item.schemas import TypeScheduleItemInCreatePydantic
from backend.week.repository import WeekRepository
from backend.week.schemas import WeekInCreatePydantic

WEEKS_COUNT = 18


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
        course = courses[int(row['course_id']) - 1]
        teacher = teachers[int(row['teacher_id']) - 1]
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
            day_of_week=int(row['day_of_week']) - 1
        ), commit=True)
    await session.commit()


async def division_into_subgroups(session, groups):
    rep = SubgroupRepository(session)
    for group in groups:
        sub_groups_count = group.count // 20
        i = 0
        for _ in range(sub_groups_count):
            await rep.create(SubgroupInCreatePydantic(
                group_id=group.id,
                label=f"{i + 1}",
                count=20
            ))
            i += 1
        remaining_count = group.count - sub_groups_count * 20
        if remaining_count > 0:
            await rep.create(SubgroupInCreatePydantic(
                group_id=group.id,
                label=f"{i + 1}",
                count=remaining_count
            ))


async def clear_data(session):
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        await session.execute(table.delete())
    await session.commit()


async def generate(session, teachers, bells, courses, groups, rooms, weeks, types_schedule_items):
    def create_week_object():
        result = dict()
        for i in range(6):
            result[i] = []
        return result

    def get_number_of_classes_per_weeks(a):
        return a // 9

    async def get_subgroups_of_group(group):
        return (await session.execute(select(Subgroup).where(Subgroup.group_id == group.id))).scalars().all()

    async def can_it_be_added(timetable_day, bell_id, room_id, group_id, subgroup_id, teacher_id):
        group_conflict = []
        if group_id:
            group_conflict = list(filter(lambda x: x.bell_id == bell_id and x.group_id == group_id and x.subgroup_id == None, timetable_day))
        subgroup_conflict = []
        if subgroup_id:
            subgroup_conflict = list(filter(lambda x: x.bell_id == bell_id and x.subgroup_id != None and x.subgroup_id == subgroup_id, timetable_day))
        teacher_conflict = list(filter(lambda x: x.bell_id == bell_id and x.teacher_id == teacher_id, timetable_day))
        room_conflict = list(filter(lambda x: x.bell_id == bell_id and x.classroom_id == room_id, timetable_day))
        teacher_limit = len(list(filter(lambda x: x.teacher_id == teacher_id, timetable_day))) >= 5
        group_limit = len(list(filter(lambda x: x.group_id == group_id, timetable_day))) >= 5

        return not (
            bool(group_conflict) or
            bool(subgroup_conflict) or
            bool(teacher_conflict) or
            bool(room_conflict) or
            teacher_limit or
            group_limit
        )

    timetable = {
        1: create_week_object(),
        2: create_week_object()
    }

    class ScheduleItemHuj(BaseModel):
        course_id: int
        group_id: int | None
        subgroup_id: int | None
        type_schedule_item_id: int
        teacher_id: int
        bell_id: int | None
        classroom_id: int | None
        week: int | None

    schedule_items_prepared: list[ScheduleItemHuj] = []

    group_course = get_rows_from_csv("schedule_generator/input_data/group_course.csv")

    for item in group_course:
        group = groups[int(item["group_id"]) - 1]
        course = courses[int(item["course_id"]) - 1]
        teacher = teachers[int(item["teacher_id"]) - 1]
        for i in range(get_number_of_classes_per_weeks(int(item["lecture_count"]))):
            schedule_items_prepared.append(ScheduleItemHuj(**{
                "course_id": course.id,
                "group_id": group.id,
                "teacher_id": teacher.id,
                "subgroup_id": None,
                "type_schedule_item_id": types_schedule_items[0].id,
                "week": i % 2
            }))
        for i in range(get_number_of_classes_per_weeks(int(item["practice_count"]))):
            subgroups = await get_subgroups_of_group(group)
            for subgroup in subgroups:
                schedule_items_prepared.append(ScheduleItemHuj(**{
                    "course_id": course.id,
                    "group_id": group.id,
                    "teacher_id": teacher.id,
                    "subgroup_id": subgroup.id,
                    "type_schedule_item_id": types_schedule_items[1].id,
                    "week": i % 2
                }))
        for i in range(get_number_of_classes_per_weeks(int(item["laboratory_count"]))):
            subgroups = await get_subgroups_of_group(group)
            for subgroup in subgroups:
                schedule_items_prepared.append(ScheduleItemHuj(**{
                    "course_id": course.id,
                    "group_id": group.id,
                    "teacher_id": teacher.id,
                    "subgroup_id": subgroup.id,
                    "type_schedule_item_id": types_schedule_items[2].id,
                    "week": i % 2
                }))

    for schedule_obj in schedule_items_prepared:
        added = False
        week = schedule_obj.week + 1
        for bell in bells:
            for day_of_week in timetable[week].keys():
                for room in rooms:
                    if added:
                        continue
                    check = await can_it_be_added(
                        timetable[week][day_of_week],
                        bell.id,
                        room.id,
                        schedule_obj.group_id,
                        schedule_obj.subgroup_id,
                        schedule_obj.teacher_id,
                    )
                    if check:
                        create_in = schedule_obj.dict()
                        create_in['bell_id'] = bell.id
                        create_in['classroom_id'] = room.id
                        timetable[week][day_of_week].append(
                            ScheduleItemHuj(
                               **create_in
                            )
                        )
                        added = True
        if not added:
            print(f"FAILED ADD, {schedule_obj.course_id}")

    rep = ScheduleItemRepository(session)
    start_date = datetime.datetime.strptime("2022-09-12", "%Y-%m-%d")
    start_week = 37
    for week in timetable.keys():
        for day_of_week in timetable[week].keys():
            for obj in timetable[week][day_of_week]:
                for i in range(0, 8):
                    start_date_ = start_date + datetime.timedelta(days=(14 * i))
                    create_in = obj.dict()
                    create_in["date"] = start_date_ + datetime.timedelta(days=day_of_week)
                    create_in["date"] += datetime.timedelta(days=(7 * (week - 1)))
                    create_in["week_id"] = weeks[week - 1].id
                    await rep.create(ScheduleItemInCreatePydantic(**create_in))

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
        types_schedule_items = await create_from_csv("schedule_generator/input_data/types_schedule_item.csv", session,
                                                     TypeScheduleItemRepository, TypeScheduleItemInCreatePydantic)
        groups = await create_from_csv("schedule_generator/input_data/groups.csv", session, GroupRepository,
                                       GroupInCreatePydantic)
        await create_course_teacher_relation_from_csv("schedule_generator/input_data/course_teacher.csv", session,
                                                      courses, teachers)
        weeks = await create_from_csv("schedule_generator/input_data/weeks.csv", session, WeekRepository,
                                      WeekInCreatePydantic)
        rooms = await create_from_csv("schedule_generator/input_data/classrooms.csv", session, ClassroomRepository,
                                      ClassroomInCreatePydantic)
        await create_teacher_wishes_from_csv("schedule_generator/input_data/teacher_wishes.csv",
                                             session, teachers=teachers, bells=bells, weeks=weeks)
        await division_into_subgroups(session, groups)
        await generate(session, teachers, bells, courses, groups, rooms, weeks, types_schedule_items)


if __name__ == "__main__":
    asyncio.run(main())
