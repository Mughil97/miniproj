import json
import pytest
from tests.test import TestBase

class TestCreateTask(TestBase):
    task_api = '/api/task'
    headers = TestBase.headers

    def test_task_successful_creation(self):
        project_id = 1
        task_name = "success_test_task"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        task_payload = json.dumps({
            "project_id" : project_id,
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.task_api, headers= self.headers, data=task_payload)
        self.assertEqual(201, response.status_code)

    def test_wrong_project(self):
        project_id = 10
        task_name = "success_test_task3"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        task_payload = json.dumps({
            "project_id" : project_id,
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.task_api, headers= self.headers, data=task_payload)
        self.assertEqual("Project Not Found", response.json['message'])
        self.assertEqual(404, response.status_code)

    def test_inactive_project(self):
        project_id = 2
        task_name = "inactive project"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        task_payload = json.dumps({
            "project_id" : project_id,
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.task_api, headers= self.headers, data=task_payload)
        self.assertEqual("InActive project", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_wrng_date(self):
        project_id = 1
        task_name = "date task"
        due_date =  "07/15/2022"
        estimated_time = "20:00:00"
        task_payload = json.dumps({
            "project_id" : project_id,
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.task_api, headers= self.headers, data=task_payload)
        self.assertEqual("InValid date", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_wrng_time(self):
        project_id = 1
        task_name = "time_task"
        due_date =  "07/15/2020"
        estimated_time = "2000:00"
        task_payload = json.dumps({
            "project_id" : project_id,
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.task_api, headers= self.headers, data=task_payload)
        self.assertEqual("InValid time", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_null_data(self):
        project_id = 1
        task_name = ""
        due_date =  "07/15/2020"
        estimated_time = "2000:00"
        task_payload = json.dumps({
            "project_id" : project_id,
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time
        })
        response = self.app.post(self.task_api, headers= self.headers, data=task_payload)
        self.assertEqual("Value is Null", response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_gettasks(self):
        response = self.app.get(self.task_api, headers= self.headers)
        self.assertEqual(200,response.status_code)

    def test_get_task_id(self):
        response = self.app.get(self.task_api+"/1", headers= self.headers)
        self.assertEqual(200,response.status_code)

    def test_dlt_task_id(self):
        response = self.app.delete(self.task_api+"/1", headers= self.headers)
        self.assertEqual(202,response.status_code)

    def test_mytasks(self):
        response = self.app.get("/api/mytasks", headers= self.headers)
        self.assertEqual(200,response.status_code)
    
    def test_project_tasks(self):
        response = self.app.get(self.task_api+"/project/1", headers= self.headers)
        self.assertEqual(200,response.status_code)
    
    def test_update_task(self):
        task_name = "task updated"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        status = "progress"
        task_payload = json.dumps({
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time,
            "status" : status
        })
        response = self.app.put(self.task_api+"/1", headers= self.headers, data = task_payload)
        self.assertEqual(200,response.status_code)

    def test_update_task_wrng_time(self):
        task_name = "tast update wrong time"
        due_date =  "07/15/2020"
        estimated_time = "20-00:00"
        status = "progress"
        task_payload = json.dumps({
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time,
            "status" : status
        })
        response = self.app.put(self.task_api+"/1", headers= self.headers, data = task_payload)
        self.assertEqual(400,response.status_code)

    def test_update_task_wrng_date(self):
        task_name = "task update wrong date"
        due_date =  "07/15/020"
        estimated_time = "20:00:00"
        status = "progress"
        task_payload = json.dumps({
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time,
            "status" : status
        })
        response = self.app.put(self.task_api+"/1", headers= self.headers, data = task_payload)
        self.assertEqual(400,response.status_code)

    def test_update_task_wrng_status(self):
        task_name = "task update wrong status"
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        status = "complted"
        task_payload = json.dumps({
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time,
            "status" : status
        })
        response = self.app.put(self.task_api+"/1", headers= self.headers, data = task_payload)
        self.assertEqual(200,response.status_code)

    def test_update_task_null_data(self):
        task_name = ""
        due_date =  "07/15/2020"
        estimated_time = "20:00:00"
        status = "open"
        task_payload = json.dumps({
            "task_name" : task_name,
            "due_date" : due_date,
            "estimated_time": estimated_time,
            "status" : status
        })
        response = self.app.put(self.task_api+"/1", headers= self.headers, data = task_payload)
        self.assertEqual(200,response.status_code)
