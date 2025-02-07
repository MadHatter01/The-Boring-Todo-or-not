from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import sys


DATABASE_URL = "sqlite:///boring_todo.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    completed = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, description={self.description}, completed={self.completed})>"

Base.metadata.create_all(engine)
dbsession = Session()

def add_task(description):
    task = Task(description = description)
    dbsession.add(task)
    dbsession.commit()
    print(f" Task Added: {description}.")

def list_tasks():
    tasks = dbsession.query(Task).all()
    if not tasks:
        print(f"Nothing to do")
        return
    
    for task in tasks:
        status = "done" if task.completed else "todo"
        print(f"[{status}] {task.id} : {task.description}")


if len(sys.argv) > 1:
    action = sys.argv[1]
    if action == "add":
        add_task(" ".join(sys.argv[2:]))
    elif action == "list":
        list_tasks()

else:
    print("Usage: python main.py [add|list] [task description]")