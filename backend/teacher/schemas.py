from pydantic import BaseModel

from backend.course.schemas import CoursePydantic


class TeacherBasePydantic(BaseModel):
    first_name: str
    last_name: str
    middle_name: str


class TeacherPydantic(BaseModel):
    id: int
    full_name: str

    class Config:
        orm_mode = True


class TeacherWithCourses(TeacherPydantic):
    courses: CoursePydantic


class TeacherInCreatePydantic(TeacherBasePydantic):
    pass


class TeacherInUpdatePydantic(TeacherBasePydantic):
    pass


class TeacherFilterPydantic(BaseModel):
    course_id: int | None