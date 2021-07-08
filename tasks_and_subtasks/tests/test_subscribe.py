from tests.test import TestBase
from ps.subscriber import subscribe_method
from app import app
from services.services import Services
import json

class SubscribeTest(TestBase):
    def test_user_subscribe(self):
        user = '{"user_id" : 4, "full_name" : "balu"}'          
        user = json.loads(user)
        self.assertEqual(subscribe_method(self, user, "user", app),4)
    
    def test_project_subscribe(self):
        project = '{"id" : 4, "projectName" : "enclara", "isActive": true}'          
        project = json.loads(project)
        self.assertEqual(subscribe_method(self, project, "project", app),4)
    
    def test_project_user_subscribe(self):
        project_user = '{"user_id" : 2, "project_id" : "3", "is_active": true}'          
        project_user = json.loads(project_user)
        self.assertEqual(subscribe_method(self, project_user, "ProjectUser", app),4)
    
    def test_project_subscribe_update(self):
        project = '{"id" : 2, "projectName" : "PS", "isActive": true}'          
        project = json.loads(project)
        self.assertEqual(subscribe_method(self, project, "project", app),2)

    def test_project_user_subscribe_update(self):
        project_user = '{"user_id" : 3, "project_id" : "1", "is_active": true}'          
        project_user = json.loads(project_user)
        self.assertEqual(subscribe_method(self, project_user, "ProjectUser", app),3)
    
    def test_timelog_subscribe(self):
        time_log = '{"user_id" : 1, "task_id" : 2,  "sub_task_id" : 2, "user_time": "10:00:00", "task_time": "10:00:00", "sub_task_time": "10:00:00"}'          
        time_log = json.loads(time_log)
        self.assertEqual(subscribe_method(self, time_log, "timelog", app),"Time Logged")