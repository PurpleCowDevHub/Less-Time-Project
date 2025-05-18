from .database import Base
from sqlalchemy import Column, Integer, String

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    position = Column(String(100))