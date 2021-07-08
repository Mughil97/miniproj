import redis
from models.user import User
from models.task import Task
from helpers.logger import logging
from models.project import Project
from models.milestone import Milestone
from services.services import Services
import logging
import threading
from flask import json
import time

logger = logging.getLogger(__name__)


class UserListener(threading.Thread):
    def __init__(self,app, r, channels):
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
            user = User()
            user.user_id = obj['user_id']
            user.fullname = obj['full_name']
            logging.info("User Added from channel")
            Services().save(self.app,user)

class ProjectListener(threading.Thread):
    def __init__(self,app, r, channels):
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
            project = Project()
            project.project_id = obj['project_id']
            project.user_id = obj['user_id']
            project.project_name = obj['project_name']
            project.isActive = obj['is_active']
            pu = Services.query_service(self,self.app, obj['project_id'],obj['user_id'])
            if pu == None:
                Services().save(self.app, project)
                logger.info("ProjectUser Added from Channel")
            else:
                Services.commit_project_user(self,self.app, pu ,obj['is_active'])
                logger.info("ProjectUser Updated from Channel")


class TaskListener(threading.Thread):
    def __init__(self,app, r, channels):
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
            task = Task()
            task.user_id = obj['user_id']
            task.project_id = obj['project_id']
            task.task_id = obj['task_id']
            task.task_name = obj['task_name']
            task.sub_task_name = obj['sub_task_name']
            task.sub_task_id = obj['sub_task_id']
            Services().save(self.app,task)
            logging.info("Task Added from Channel")

class MilestoneListener(threading.Thread):
    def __init__(self,app, r, channels):
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
            milestone = Milestone()
            milestone.milestone_id = obj['milestone_id']
            milestone.task_id = obj['task_id']
            Services().save(self.app,milestone)
            logging.info("Milestone Added from Channel")

