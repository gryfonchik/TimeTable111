from sqlalchemy import Column, Table, ForeignKey

from backend.core.database import Base

course_teacher_table = Table(
    'course_teacher',
    Base.metadata,
    Column('teacher_id', ForeignKey('teacher.id', ondelete="CASCADE"), primary_key=True),
    Column('course_id', ForeignKey('course.id', ondelete="CASCADE"), primary_key=True)
)
