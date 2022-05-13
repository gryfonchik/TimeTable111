from sqlalchemy import Column, Integer, String

from backend.core.database import Base


class TypeScheduleItem(Base):
    __tablename__ = "type_schedule_item"

    id = Column(Integer, primary_key=True)
    label = Column(String)
