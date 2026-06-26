from database import SessionLocal
from models import Task


def save_task(task_id, number, result):

    db = SessionLocal()

    task = Task(
        task_id=task_id,
        input_number=number,
        result=result,
        status="completed"
    )

    db.add(task)
    db.commit()
    db.close()