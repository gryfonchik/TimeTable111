from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.course_teacher.models import course_teacher_table
from backend.core.database import Base


class Course(Base):
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    teachers = relationship("Teacher", secondary=course_teacher_table,
                            back_populates="courses")
