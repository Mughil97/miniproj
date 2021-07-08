from flask import make_response, jsonify
import jwt
from models.models import Task,SubTask,Assignee

def send_response(result, status):
    response = make_response(jsonify(result), status)
    response.mimetype = 'application/json'
    return response

def check_exists(self,ud,td,sd):
    ext = Assignee.query.filter_by(user_id = ud, task_id = td, sub_task_id = sd).first()
    return None if ext == None else ext

def get_projects_from_jwt(self,data):
    projects = data['projects']
    pd = {}
    for project in projects:
        key = project['id'] 
        value = project['hierachy_key']
        pd.update({key:value})
    return pd

def check_active(self, task_is_active, subtask_is_active, tid, stid):
    is_active = False
    if subtask_is_active != None:
        is_active = SubTask.query.get(stid).is_active
    else:
        is_active = Task.query.get(tid).is_active
    return is_active
