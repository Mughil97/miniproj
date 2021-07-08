from models.user import User
from models.project import Project
from models.task import Task
from models.timelog import Timelog
from sqlalchemy import and_
from validation.timevalidation import total_time

time_user = []
time_task = []
time_subtask = []
time_milestone = []

def user_query(query_user):
    for z in query_user:
        time_user.append(str(z.hours_logged))
    x = total_time(time_user)
    return x

def task_query(query_task):
    for z in query_task:
        time_task.append(str(z.hours_logged))
    x = total_time(time_task)
    return x

def subtask_query(query_subtask):
    for z in query_subtask:
        time_subtask.append(str(z.hours_logged))
    x = total_time(time_subtask)
    return x
