from pydantic import BaseModel


class TeacherWishBasePydantic(BaseModel):
    pass


class TeacherWishPydantic(BaseModel):
    id: int
    teacher_id: int
    bell_id: int
    week_id: int
    day_of_week: int

    class Config:
        orm_mode = True


class TeacherWishInCreatePydantic(TeacherWishBasePydantic):
    teacher_id: int
    bell_id: int
    week_id: int
    day_of_week: int


class TeacherWishInUpdatePydantic(TeacherWishBasePydantic):
    teacher_id: int
    bell_id: int
    week_id: int
    day_of_week: int
