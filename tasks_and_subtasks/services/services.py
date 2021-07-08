from db.db import db
from models.models import User, Project, ProjectUser, Task, SubTask, Assignee
from datetime import datetime, timedelta
from logger import MyLogger
from ps.publish import redis
from flask import json

logger = MyLogger.logger

class Services:

    def save(self,app, object):
        with app.app_context():
            db.session.add(object)
            db.session.commit()
            db.session.refresh(object)
            logger.info("Row Added from Channel")

    def commit_project(self,app, pro, is_active, pid):
        with app.app_context():
            pro.is_active = is_active
            tasks = Task.query.filter_by(project_id = pid).all()
            subtasks = SubTask.query.filter_by(project_id = pid).all()
            for task in tasks:
                task.is_active = is_active
            for subtask in subtasks:
                subtask.is_active = is_active
            db.session.merge(pro)
            db.session.commit()
            logger.info("Isactive changed from Channel - {}".format(pid))

    def commit_project_user(self,app, pu, is_active):
        with app.app_context():
            pu.is_active = is_active
            tasks = Task.query.filter_by(project_id = pu.project_id).all()
            for task in tasks:
                assignees = Assignee.query.filter_by(task_id = task.id).all()
                for assignee in assignees:
                    assignee.is_assigned = is_active
            db.session.merge(pu)
            db.session.commit()
    
    def project_query(self,app, pname):
        with app.app_context():
            pro = Project.query.filter_by(project_name = pname).first()
            return pro

    def query_service(self,app, pid, uid):
        with app.app_context():
            pu = ProjectUser.query.filter_by(user_id = uid, project_id = pid).first()
            return pu

    def assignee_timelog(self,app,user_id, task_id, sub_task_id, time):
        with app.app_context():
            assignee = Assignee.query.filter_by(user_id = user_id, task_id = task_id, sub_task_id = sub_task_id).first()
            assignee.time_spent = time+":00"
            db.session.merge(assignee)
            db.session.commit()
            logger.debug("assignee time added - {}".format(assignee.id))
            return "User Time Logged"
    
    def task_timelog(self,app,task_id,time):
        with app.app_context():
            task = Task.query.get(task_id)
            task.time_spent = time+":00"
            db.session.merge(task)
            db.session.commit()
            redis.publish('task',json.dumps(task.serialize()))
            logger.debug("task time added and published - {}".format(task.id))

    def subtask_timelog(self,app,subtask_id,time):
        with app.app_context():
            subtask = SubTask.query.get(subtask_id)
            subtask.time_spent = time+":00"
            db.session.merge(subtask)
            db.session.commit()
            logger.debug("subtask time added")
