from sqlalchemy import Column, Integer, String

from backend.core.database import Base


class Classroom(Base):
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
