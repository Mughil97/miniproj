from db.db import db
from models.base import Base

class Task(Base):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String, nullable =False)
    sub_task_id = db.Column(db.Integer)
    sub_task_name = db.Column(db.String)
    
    