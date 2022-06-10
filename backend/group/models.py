from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Group(Base):
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    count = Column(Integer)


class Subgroup(Base):
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE"))
    group = relationship('Group')
    label = Column(String, nullable=False)
    count = Column(Integer)
