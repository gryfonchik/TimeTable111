from sqlalchemy import Column, Integer, String

from backend.core.database import Base


class Bell(Base):
    id = Column(Integer, primary_key=True)
    time_beg = Column(String, nullable=False)
    time_end = Column(String, nullable=False)
