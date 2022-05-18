from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.bell.models import Bell
from backend.classroom.models import Classroom
from backend.core.database import Base
from backend.course.models import Course
from backend.group.models import Group, Subgroup
from backend.teacher.models import Teacher
from backend.type_schedule_item.models import TypeScheduleItem
from backend.week.models import Week


class ScheduleItem(Base):
    __tablename__ = "schedule_item"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id), nullable=False)
    course = relationship("Course")
    teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
    teacher = relationship("Teacher")
    classroom_id = Column(Integer, ForeignKey(Classroom.id), nullable=False)
    classroom = relationship("Classroom")
    bell_id = Column(Integer, ForeignKey(Bell.id), nullable=False)
    bell = relationship("Bell")
    week_id = Column(Integer, ForeignKey(Week.id), nullable=False)
    week = relationship("Week")
    group_id = Column(Integer, ForeignKey(Group.id), nullable=True)
    group = relationship("Group")
    subgroup_id = Column(Integer, ForeignKey(Subgroup.id), nullable=True)
    subgroup = relationship("Subgroup")
    type_schedule_item_id = Column(Integer, ForeignKey(TypeScheduleItem.id), nullable=True)
    type_schedule_item= relationship("TypeScheduleItem")
