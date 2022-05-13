from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from backend.core.database import Base


class Teacher(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)

    @hybrid_property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
