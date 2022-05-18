from pydantic import BaseModel


class ClassroomBasePydantic(BaseModel):
    number: str
    capacity: int


class ClassroomPydantic(ClassroomBasePydantic):
    id: int

    class Config:
        orm_mode = True


class ClassroomInCreatePydantic(ClassroomBasePydantic):
    pass


class ClassroomInUpdatePydantic(ClassroomBasePydantic):
    pass


class ClassroomListPydantic(BaseModel):
    classrooms: list[ClassroomPydantic]
    count: int
