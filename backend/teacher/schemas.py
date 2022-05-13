from pydantic import BaseModel


class TeacherBasePydantic(BaseModel):
    label: str


class TeacherPydantic(TeacherBasePydantic):
    id: int

    class Config:
        orm_mode = True


class TeacherInCreatePydantic(TeacherBasePydantic):
    pass


class TeacherInUpdatePydantic(TeacherBasePydantic):
    pass


class TeacherListPydantic(BaseModel):
    teachers: list[TeacherPydantic]
    count: int
