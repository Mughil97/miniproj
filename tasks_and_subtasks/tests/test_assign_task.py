import json
import pytest
from tests.test import TestBase
from exceptions.exceptions import *

class TestAssignTask(TestBase):

    assign_api = '/api/assignee/task'
    headers = TestBase.headers

    def test_task_successful_assign(self):
        user_id = 1
        task_type = "sub_task"
        task_id = 1
        sub_task_id = 1
        assign_payload = json.dumps({
            "user_id" : user_id,
            "task_type" : task_type,
            "task_id" : task_id,
            "sub_task_id": sub_task_id
        })
        response = self.app.post(self.assign_api, headers= self.headers, data=assign_payload)
        self.assertEqual(201, response.status_code)

    
    def test_assign_unauthorised(self):
        user_id = 1
        task_type = "task"
        task_id = 3
        assign_payload = json.dumps({
            "user_id" : user_id,
            "task_type" : task_type,
            "task_id" : task_id
        })
        response = self.app.post(self.assign_api, headers= self.headers, data=assign_payload)
        self.assertEqual("Unauthorized", response.json['message'])
        self.assertEqual(401, response.status_code)


    def test_assign_wrng_user(self):
        user_id = 10
        task_type = "sub_task"
        task_id = 1
        sub_task_id = 1
        assign_payload = json.dumps({
            "user_id" : user_id,
            "task_type" : task_type,
            "task_id" : task_id,
            "sub_task_id": sub_task_id
        })
        response = self.app.post(self.assign_api, headers= self.headers, data=assign_payload)
        self.assertEqual("User Not Found", response.json['message'])
        self.assertEqual(404, response.status_code)

    def test_assign_wrng_task(self):
        user_id = 1
        task_type = "sub_task"
        task_id = 20
        sub_task_id = 1
        assign_payload = json.dumps({
            "user_id" : user_id,
            "task_type" : task_type,
            "task_id" : task_id,
            "sub_task_id": sub_task_id
        })
        response = self.app.post(self.assign_api, headers= self.headers, data=assign_payload)
        self.assertEqual("Task Unavailable", response.json['message'])
        self.assertEqual(404, response.status_code)

    def test_assign_wrng_subtask(self):
        user_id = 1
        task_type = "sub_task"
        task_id = 1
        sub_task_id = 10
        assign_payload = json.dumps({
            "user_id" : user_id,
            "task_type" : task_type,
            "task_id" : task_id,
            "sub_task_id": sub_task_id
        })
        response = self.app.post(self.assign_api, headers= self.headers, data=assign_payload)
        self.assertEqual("SubTask Unavailable", response.json['message'])
        self.assertEqual(404, response.status_code)


    def test_assign_invalid_input(self):
        user_id = 1
        task_type = "sub_task"
        task_id = 1
        assign_payload = json.dumps({
            "user_id" : user_id,
            "task_type" : task_type,
            "task_id" : task_id,
        })
        response = self.app.post(self.assign_api, headers= self.headers, data=assign_payload)
        self.assertEqual("Invalid Input", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_mytasks(self):
        response = self.app.get("/api/assignee/mytasks", headers= self.headers)
        self.assertEqual(200,response.status_code)

    def test_assignee_tasks(self):
        response = self.app.get("/api/assignee/task", headers= self.headers)
        self.assertEqual(200,response.status_code)
    
    def test_assignee_tasks(self):
        response = self.app.get("/api/assignee/1", headers= self.headers)
        self.assertEqual(200,response.status_code)

    def test_assignee_tasks(self):
        response = self.app.get("/api/assignee/10", headers= self.headers)
        self.assertEqual("User Not Found", response.json['message'])
        self.assertEqual(404,response.status_code)