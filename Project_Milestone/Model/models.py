from config import db
from Model.base import  Base

class Project(Base):
    __tablename__ = 'project'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    projectName=db.Column('project_name',db.String(80))
    isActive=db.Column('is_active',db.Boolean,default=True)

class ProjectUser(Base): #Bridge class for Project and User
    __tablename__ = 'projectUser'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    projectId=db.Column('project_id',db.Integer,db.ForeignKey('project.id')) 
    userId=db.Column('user_id',db.Integer)    
    roleId=db.Column('role_id',db.Integer) 
    isActive=db.Column('is_active',db.Boolean,default=True)
    dateCreated=db.Column('date_created',db.DateTime, default=db.func.now())
    dateEnd=db.Column('date_end',db.DateTime, default=None)

class User(Base):
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId=db.Column('user_id',db.Integer)
    userName=db.Column('user_name',db.String(80))

class Role(Base):
    __tablename__ = 'role'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    roleId=db.Column('role_id',db.Integer)
    roleName=db.Column('role_name',db.String(80))

class Milestone(Base):
    __tablename__ = 'milestone'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    projectId=db.Column('project_id',db.Integer,db.ForeignKey('project.id')) 
    completion=db.Column('completion',db.Float,default=0)    
    dueDate=db.Column('due_date',db.Date)
    isActive=db.Column('is_active',db.Boolean,default=True)

class MilestoneTask(Base):
    __tablename__ = 'milestoneTask'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    milestoneId=db.Column('milestone_id',db.Integer,db.ForeignKey('milestone.id')) 
    taskId=db.Column('task_id',db.Integer) 
    
class Task(Base):
    __tablename__ = 'task'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    taskId=db.Column('task_id',db.Integer)
    taskName=db.Column('task_name',db.String(80))
    projectId=db.Column('project_id',db.Integer) 
    status=db.Column('status',db.String(80))
    estimatedTime=db.Column('estimated_time',db.String(80),default="00:00:00")
    time=db.Column('logged_time',db.String(80),default="00:00:00")

class MilestoneTime(Base):
    __tablename__ = 'milestoneTime'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    milestoneId=db.Column('milestone_id',db.Integer)
    time=db.Column('time',db.String(80))