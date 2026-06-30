from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from dao.database import Base


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True)
    input_number = Column(Integer)
    result = Column(Integer)
    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )