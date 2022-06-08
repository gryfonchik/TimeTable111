from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.course_teacher.models import course_teacher_table
from backend.core.database import Base


class Teacher(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    courses = relationship("Course", secondary=course_teacher_table,
                           lazy='joined',
                           uselist=True,
                           back_populates="teachers")

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
