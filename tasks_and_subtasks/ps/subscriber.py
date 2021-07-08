import redis
from services.services import Services
from models.models import User, Project, ProjectUser, Task, SubTask,Assignee
from db.db import db
import threading
from flask import json
import time
from logger import MyLogger

logger = MyLogger.logger

class Listener(threading.Thread):
    channel_name = ""
    app = ""
    def __init__(self,app, r, channels):
        self.channel_name = channels
        threading.Thread.__init__(self)
        self.daemon = True
        self.app = app
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)
        
    def work(self,item): 
        if item['data'] == "KILL":
            self.pubsub.unsubscribe()
        if item['type'] == 'message':
            obj = json.loads(item['data'])
            subscribe_method(self,obj, self.channel_name, self.app)

def subscribe_method(self,obj,channel_name, app):
    if channel_name == "user":
        user = User(obj['user_id'], obj['full_name'])
        Services().save(app,user)
        logger.info("User Added from Channel")
        return user.id

    elif channel_name == "project":
        project = Project(obj['id'], obj['projectName'], obj['isActive'])
        pro = Services.project_query(self,app, obj['projectName'])
        if pro == None:
            Services().save(app,project)
            logger.info("Project Added from Channel")
            return project.id
        else:
            Services.commit_project(self,app, pro ,obj['isActive'], pro.project_id)
            logger.info("Project updated from Channel")
            return pro.id
    elif channel_name == "ProjectUser":
        project_user = ProjectUser(obj['user_id'], obj['project_id'], obj['is_active'])
        pu = Services.query_service(self,app, obj['project_id'],obj['user_id'])
        if pu == None:
            Services().save(app,project_user)
            logger.info("ProjectUser Added from Channel")
            return project_user.id
        else:
            Services.commit_project_user(self,app, pu ,obj['is_active'])
            logger.info("ProjectUser Updated from Channel")
            return pu.id
    else:
        Services.assignee_timelog(self,app, obj['user_id'], obj['task_id'], obj['sub_task_id'], obj['user_time'])
        Services.task_timelog(self,app,obj['task_id'],obj['task_time'])
        if obj['sub_task_id'] != None:
            Services.subtask_timelog(self,app,obj['sub_task_id'],obj['sub_task_time'])
            return "Time Logged"
