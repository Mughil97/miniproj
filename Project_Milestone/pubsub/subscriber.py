import redis
from Model.models import User,Task,Role
from Service.dbService import DbService
from logger import Mylogger
import threading
from flask import json
import time

logger=Mylogger.logger

class Listener(threading.Thread):
    channel=''
    def __init__(self,app, r, channels):
        self.channel=channels
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
            if self.channel=='task':
                task_obj=DbService.search_task(self,self.app,obj['project_id'],obj['id'])
                if task_obj==None:
                    task = Task(taskId=obj['id'],taskName=obj['task_name'].lower(),projectId=obj['project_id'],status=obj['status'].lower(),estimatedTime=obj['estimated_time'],time=obj['time_spent'])
                    DbService.save_from_channel(self,self.app,task)
                    logger.debug("Task added from channel")
                else:
                    DbService.commit_changes(self,self.app,task_obj,obj['status'],obj['task_name'],obj['estimated_time'],obj['time_spent'])
                    logger.debug("Task updated from channel")
            
            elif self.channel=='role':
                role_obj=DbService.search_role(self,self.app,obj['role_id'])
                if role_obj==None:
                    r_obj = Role(roleId=obj['role_id'],roleName=obj['role_name'].lower())
                    DbService.save_from_channel(self,self.app,r_obj)
                    logger.debug("Role added from channel")
                else:
                    DbService.commit_role_changes(self,self.app,role_obj,obj['role_name'].lower())
                    logger.debug("Role updated from channel")
            
            elif self.channel=='user':
                user = User(userId=obj['user_id'],userName=obj['full_name'].lower())
                DbService.save_from_channel(self,self.app,user)
                logger.debug("user added from channel")

        
