from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
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
    date = Column(Date, nullable=False)
    course_id = Column(Integer, ForeignKey(Course.id, ondelete="CASCADE"), nullable=False)
    course = relationship("Course")
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete="CASCADE"), nullable=False)
    teacher = relationship("Teacher")
    classroom_id = Column(Integer, ForeignKey(Classroom.id, ondelete="CASCADE"), nullable=False)
    classroom = relationship("Classroom")
    bell_id = Column(Integer, ForeignKey(Bell.id, ondelete="CASCADE"), nullable=False)
    bell = relationship("Bell")
    week_id = Column(Integer, ForeignKey(Week.id, ondelete="CASCADE"), nullable=False)
    week = relationship("Week")
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE"), nullable=True)
    group = relationship("Group")
    subgroup_id = Column(Integer, ForeignKey(Subgroup.id, ondelete="CASCADE"), nullable=True)
    subgroup = relationship("Subgroup")
    type_schedule_item_id = Column(Integer, ForeignKey(TypeScheduleItem.id, ondelete="CASCADE"), nullable=True)
    type_schedule_item = relationship("TypeScheduleItem")
    check_collision = Column(Boolean, default=True, nullable=True)
