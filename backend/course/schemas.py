from pydantic import BaseModel


class CourseBasePydantic(BaseModel):
    label: str


class CoursePydantic(CourseBasePydantic):
    id: int

    class Config:
        orm_mode = True


class CourseInCreatePydantic(CourseBasePydantic):
    pass


class CourseInUpdatePydantic(CourseBasePydantic):
    pass
