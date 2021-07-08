from db.db import db
from sqlalchemy import Date, Time, Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Base(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

#subscribe
class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, unique=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    assignees = relationship('Assignee', backref = 'user')

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

#subscribe
class Project(Base):

    __tablename__ = 'project'
    id = Column(Integer, primary_key = True)
    project_id = Column(Integer, unique=True, nullable=False)
    project_name = Column(String(100), unique = True, nullable=False)
    is_active = Column(Boolean)
    tasks = relationship('Task', backref = 'project')
    sub_tasks = relationship('SubTask', backref = 'project')

    def __init__(self,project_id, project_name, is_active):
        self.project_id = project_id
        self.project_name = project_name
        self.is_active = is_active

#subscribe
class ProjectUser(Base):

    __tablename__ = 'project_user'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer , nullable = False)
    project_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable = False)

    def __init__(self, user_id, project_id, is_active):
        self.user_id = user_id
        self.project_id = project_id
        self.is_active = is_active
        
class Task(Base):

    __tablename__ = 'task'
    id = Column(Integer, primary_key = True)
    project_id = Column(Integer, ForeignKey('project.project_id'),  nullable = False)
    task_name = Column(String(100), nullable=False, unique = True)
    due_date = Column(Date, nullable=False)
    estimated_time = Column(String, nullable=False)
    status = Column(String(100), nullable=False)
    created_by = Column(Integer)
    time_spent = Column(String)
    is_active = Column(Boolean)
    assignees = relationship('Assignee', backref = 'task')
    
    def __init__(self,project_id,task_name, due_date, estimated_time, status):
        self.project_id = project_id
        self.task_name = task_name
        self.due_date = due_date
        self.estimated_time = estimated_time
        self.status = status

    def serialize(self):
        return {"id": self.id,
                "project_id": self.project_id,
                "task_name": self.task_name,
                "due_date": str(self.due_date),
                "estimated_time" : str(self.estimated_time),
                "status" : self.status,
                "created_by" : self.created_by,
                "time_spent" : self.time_spent}

class SubTask(Base):

    __tablename__ = 'sub_task'
    id = Column(Integer, primary_key = True)
    project_id = Column(Integer, ForeignKey('project.project_id'),  nullable = False)
    task_id = Column(Integer, ForeignKey('task.id'),  nullable = False)
    sub_task_name = Column(String(100), nullable=False, unique = True)
    due_date = Column(Date, nullable=False)
    estimated_time = Column(String, nullable=False)
    status = Column(String(100), nullable=False)
    created_by = Column(Integer)
    time_spent = Column(String)
    is_active = Column(Boolean)
    assignees = relationship('Assignee', backref = 'sub_task')

    def __init__(self,task_id, project_id, sub_task_name, due_date, estimated_time,status):
        self.task_id = task_id
        self.project_id = project_id
        self.sub_task_name = sub_task_name
        self.due_date = due_date
        self.estimated_time = estimated_time
        self.status = status

class Assignee(Base):

    __tablename__ = "assignee"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable = False)
    task_type = Column(String(50), nullable = False)
    task_id = Column(Integer, ForeignKey('task.id'))
    sub_task_id = Column(Integer, ForeignKey('sub_task.id'))
    is_assigned = Column(Boolean, default = True)
    assigned_by = Column(Integer)
    time_spent = Column(String, default = "00:00:00")

    def serialize(self, project_id, task_name, sub_task_name):
        return {"id": self.id,
                "user_id" : self.user_id,
                "project_id" : project_id,
                "task_type" : self.task_type,
                "task_id" : self.task_id,
                "sub_task_id" : self.sub_task_id,
                "is_assigned" : self.is_assigned,
                "task_name" : task_name,
                "sub_task_name" : sub_task_name}