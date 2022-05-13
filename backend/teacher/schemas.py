from pydantic import BaseModel

from backend.course.schemas import CoursePydantic


class TeacherBasePydantic(BaseModel):
    label: str


class TeacherPydantic(TeacherBasePydantic):
    id: int

    class Config:
        orm_mode = True


class TeacherWithCourses(TeacherPydantic):
    courses: CoursePydantic


class TeacherInCreatePydantic(TeacherBasePydantic):
    pass


class TeacherInUpdatePydantic(TeacherBasePydantic):
    pass


class TeacherListPydantic(BaseModel):
    teachers: list[TeacherPydantic]
    count: int
