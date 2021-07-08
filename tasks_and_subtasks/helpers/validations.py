import os
from flask import json
from models.models import *
from logger import MyLogger
from helpers.utils import *
from datetime import datetime
from exceptions.exceptions import *

logger = MyLogger.logger

def is_active_project(self,project_id):
    project = Project.query.filter_by(project_id = project_id).first()
    if project != None:
        result = False if project.is_active == False else True
        return result
    else:
        raise ProjectNotFound

def check_authorised(self,pid, pd):
    if pid != None:
        is_authorised = False
        if pid in pd.keys():
            role = pd.get(pid)
            is_authorised = False if role >= 3 else True
        else:
            is_authorised = False
        return is_authorised
    else:
        raise InvalidInputError

def task_validation(self,task):
    is_valid = True
    if task.task_name == "" or task.estimated_time == "" or task.due_date == "":
        is_valid = False
    return is_valid

def sub_task_validation(self,subtask):
    is_valid = True
    if subtask.task_id == "" or subtask.sub_task_name == "" or subtask.estimated_time == "" or subtask.due_date == "":
        is_valid = False
    return is_valid

def task_in_project(self,subtask):
    is_valid = False
    pid = subtask.project_id
    tid = subtask.task_id
    task = Task.query.filter_by(id = tid).first()
    if task != None:
        if task.project_id == pid:
            is_valid = True
        else:
            is_valid = False
    else:
        is_valid = False
    return is_valid


def date_validation(self,due_date):
    try:    
        ip_date = datetime.strptime(str(due_date), "%m/%d/%Y")
        present = datetime.now()
        is_valid = False
        if ip_date.date() > present.date():
            if ip_date.year not in [present.year , present.year +1]:
                is_valid = False
            else:
                is_valid = True
        else:
            is_valid = False
        return is_valid
    except ValueError:
        raise WrongDateError

def time_validation(self,time):    
    is_time = True
    if time_constraints(time):
        for i in time:
            if i.isnumeric() == False:
                if i == ":":
                    is_time = True
                else:
                    is_time = False
                    break
            else:
                is_time = True
    else:
        is_time = False
    return is_time

def time_constraints(time):
    is_time = False
    if len(time) >= 7 and len(time) < 11:
        if time_startswith(time):
            if time[-3] ==":" and time[-6] == ":":
                is_time = True
            else:
                is_time = False
        else:
            is_time = False
    else:
        is_time = False
    return is_time

def time_startswith(time):
    is_time = False
    if time.startswith("00:00") == False and time.startswith("0:00") == False:
        if time.count(":") == 2:
            is_time = True
        else:
            is_time = False
    else:
        is_time = False
    return is_time

def assignee_validation(self,assignee):
    
    is_valid = True
    if assignee.task_type.lower() == "sub_task" and assignee.sub_task_id == None or assignee.sub_task_id != None and SubTask.query.get(assignee.sub_task_id).task_id != assignee.task_id:
        is_valid = False
    return is_valid

def assignee_in_project(self,assignee,p_id):
    is_assigned = False
    project_users = ProjectUser.query.filter_by(user_id = assignee.user_id)
    for i in project_users:
        if i.project_id == p_id and i.is_active == True:
            is_assigned = True
            break
    return is_assigned

