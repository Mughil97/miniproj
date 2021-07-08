import pytest
import json
from tests.test import TestBase
from exceptions.exceptions import *

class TestCreateSubTask(TestBase):

    headers = TestBase.headers

    sub_task_api = '/api/subtask'

    def test_subtask_successful_creation(self):
        task_id = 1
        project_id = 1
        task_name = "success_sub_test"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        sub_task_payload = json.dumps({
            "task_id" : task_id,
            "project_id" : project_id,
            "sub_task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.sub_task_api, headers= self.headers, data=sub_task_payload)
        self.assertEqual(201, response.status_code)

    
    def test_wrng_task(self):
        
        task_id = 10
        project_id = 1
        task_name = "no task"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        sub_task_payload = json.dumps({
            "task_id" : task_id,
            "project_id" : project_id,
            "sub_task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.sub_task_api, headers= self.headers, data=sub_task_payload)
        self.assertEqual("Task Unavailable", response.json['message'])
        self.assertEqual(404, response.status_code)

    def test_wrng_date(self):
        
        task_id = 1
        project_id = 1
        task_name = "succes_sub"
        due_date =  "07/15/020"
        estimated_time = "20:00:00"
        sub_task_payload = json.dumps({
            "task_id" : task_id,
            "project_id" : project_id,
            "sub_task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        
        response = self.app.post(self.sub_task_api, headers= self.headers, data=sub_task_payload)
        self.assertEqual("InValid date", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_wrng_time(self):
        task_id = 1
        project_id = 1
        task_name = "success_subtask"
        due_date =  "07/15/2020"
        estimated_time = "200:00"
        sub_task_payload = json.dumps({
            "task_id" : task_id,
            "project_id" : project_id,
            "sub_task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.sub_task_api, headers= self.headers, data=sub_task_payload)
        self.assertEqual("InValid time", response.json['message'])
        self.assertEqual(400, response.status_code)
    
    def test_null_data(self):
        project_id = 1
        task_id = 1
        sub_task_name = ""
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        subtask_payload = json.dumps({
            "project_id" : project_id,
            "task_id" : task_id,
            "sub_task_name" : sub_task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.sub_task_api, headers= self.headers, data=subtask_payload)
        self.assertEqual("Value is Null", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_subtasks(self):
        response = self.app.get(self.sub_task_api, headers= self.headers)
        self.assertEqual(200,response.status_code)

    def test_update_subtask(self):
        sub_task_name = "subtask updated"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        status = "progress"
        task_payload = json.dumps({
            "sub_task_name" : sub_task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time,
            "status" : status
        })
        response = self.app.put(self.sub_task_api+"/1", headers= self.headers, data = task_payload)
        self.assertEqual(200,response.status_code)

    def test_subtask_by_task(self):
        response = self.app.get("/api/subtask/task/1", headers= self.headers)
        self.assertEqual(200,response.status_code)

    def test_subtask_by_subtask(self):
        response = self.app.get("/api/subtask/1", headers= self.headers)
        self.assertEqual(200,response.status_code)
