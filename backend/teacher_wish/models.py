from sqlalchemy import Column, Integer, ForeignKey

from backend.bell.models import Bell
from backend.core.database import Base
from backend.teacher.models import Teacher
from backend.week.models import Week


class TeacherWish(Base):
    __tablename__ = "teacher_wish"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
    bell_id = Column(Integer, ForeignKey(Bell.id), nullable=False)
    week_id = Column(Integer, ForeignKey(Week.id), nullable=False)
    day_of_week = Column(Integer)
