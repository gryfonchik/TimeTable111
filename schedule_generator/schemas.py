from pydantic import BaseModel

from backend.course.schemas import CoursePydantic
from backend.group.schemas import GroupBasePydantic
from backend.teacher.schemas import TeacherPydantic


class PlanItem(BaseModel):
    course: CoursePydantic
    lecture_teacher: TeacherPydantic
    practice_teacher: TeacherPydantic
    laboratory_teacher: TeacherPydantic
    exam_teacher: TeacherPydantic
    group: GroupBasePydantic
    lecture_count: int
    practice_count: int
    laboratory_count: int
    independent_count: int
    exam_count: int
