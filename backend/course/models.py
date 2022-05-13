from sqlalchemy import Column, Integer, String

from backend.core.database import Base


class Course(Base):
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
