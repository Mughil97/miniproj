from config import db
from Model.models import User,Task,MilestoneTime,Role,Project,Milestone
from Exceptions.exceptions import ProjectNotFound,TaskNotFound,MilestoneNotFound

class DbService():
    def save(self,obj):
        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)

    def save_from_channel(self,app,object):
        with app.app_context():
            db.session.add(object)
            db.session.commit()

    def search_task(self,app,pid,tid):
        with app.app_context():
            return db.session.query(Task).filter(Task.projectId==pid,Task.taskId==tid).first()
    
    def is_project_exist(self,proj_id):
        p_obj=db.session.query(Project).filter(Project.id==proj_id,Project.isActive==True).first()
        if p_obj==None:
            raise ProjectNotFound

    def is_milestone_exist(self,milestone_id):
        m_obj=db.session.query(Milestone).filter(Milestone.id==milestone_id).first()
        if m_obj == None:
            raise MilestoneNotFound
        return m_obj
    
    def is_task_exist(self,task_id,project_id):
        task_obj=db.session.query(Task).filter(Task.taskId==task_id,Task.projectId==project_id).first()
        if task_obj == None:
            raise TaskNotFound
    
    def is_tasks_exist_in_project(self,project_id,tasks):
        for task in tasks:
            DbService.is_task_exist(self,task['taskId'],project_id)

    def search_milestone_time(self,app,mid):
        with app.app_context():
            return db.session.query(MilestoneTime).filter(MilestoneTime.milestoneId==mid).first()

    def search_role(self,app,rid):
        with app.app_context():
            return db.session.query(Role).filter(Role.roleId==rid).first()

    def commit_changes(self,app,obj,status,name,e_time,time):
        with app.app_context():
            obj.status=status
            obj.taskName=name
            obj.estimatedTime=e_time
            obj.time=time
            db.session.merge(obj)
            db.session.commit()
    
    def commit_milestone_time_changes(self,app,obj,time):
        with app.app_context():
            obj.time=time
            db.session.merge(obj)
            db.session.commit()

    def commit_role_changes(self,app,obj,name):
        with app.app_context():
            obj.roleName=name
            db.session.merge(obj)
            db.session.commit()
            