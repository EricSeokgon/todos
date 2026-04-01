from sqlalchemy import Column, Integer, String, Boolean
from database.orm import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, default=False)
