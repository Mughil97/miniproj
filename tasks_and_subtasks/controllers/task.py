import os
from flask import Response, request, json
from flask_restful import Resource
from helpers.utils import send_response, check_active, check_exists, get_projects_from_jwt
from helpers.validations import *
from exceptions.exceptions import *
from models.models import Task, SubTask, Assignee
from flask_jwt_extended import jwt_required, get_jwt_claims
from db.db import db
from config import Config
from jwt_auth import jwt
from logger import MyLogger
from ps.publish import redis
from sqlalchemy import exc

logger = MyLogger.logger

class TaskApi(Resource):

    @jwt_required
    def post(self):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            body = request.get_json()
            task = Task(body['project_id'],body['task_name'],body['due_date'],body['estimated_time'], None)
            dd = task.due_date
            
            if is_active_project(self,task.project_id) == False:
                raise InActiveError
            
            if check_authorised(self, task.project_id, pd) == False:
                raise UnauthorizedError

            if task_validation(self,task) == False:
                raise NulldataError

            if date_validation(self,dd) == False:
                raise WrongDateError

            if time_validation(self,task.estimated_time) == False:
                raise WrongTimeError
                              
            logger.debug("Task is Valid")
            task.time_spent = "00:00:00"
            task.created_by = data['user_id']
            task.status = "open"
            task.is_active = True
            db.session.add(task)
            db.session.commit()
            id = task.id
            redis.publish('task', json.dumps(task.serialize()))
            logger.debug("Task Added {}".format(str(id)))
            return  send_response({'message': 'Task added','_id': str(id)}, status= 201)
            
        except KeyError:
            raise InvalidInputError        
        except exc.IntegrityError:
            raise AlreadyExistsError
        except TypeError:
            raise InvalidKeyError
        except UnauthorizedError:
            raise UnauthorizedError
        except InvalidInputError:
            raise InvalidInputError
        except WrongDateError:
            raise WrongDateError    
        except WrongTimeError:
            raise WrongTimeError

    @jwt_required
    def get(self):
        try:
            tasks = Task.query.all()
            results = []
            for task in tasks:
                subtasks = []
                subtasks_obj = SubTask.query.filter_by(task_id = task.id).all()
                for names in subtasks_obj:
                    subtasks.append({"sub_task_name" : names.sub_task_name})
                results.append({
                        "id" : task.id,
                        "project_id" : task.project_id,
                        "name" : task.task_name,
                        "subtasks" : subtasks,
                        "estimated_time" : str(task.estimated_time),
                        "due_date" : str(task.due_date),
                        "status" : task.status,
                        "created_by" : task.created_by,
                        "time_spent" : task.time_spent
                    })
            logger.debug("Tasks retrived")

            return {"count" : len(results) , "tasks" : results , "message" : 200}
                
        except Exception:
            InternalServerError

class TaskIdApi(Resource):
    @jwt_required
    def get(self,id):
        task = Task.query.get(id)
        subtasks = []
        subtasks_obj = SubTask.query.filter_by(task_id = id).all()
        for names in subtasks_obj:
            subtasks.append({"sub_task_name" : names.sub_task_name})
        result = {
                "id" : task.id,
                "project_id" : task.project_id,
                "name" : task.task_name,
                "subtasks" : subtasks,
                "estimated_time" : str(task.estimated_time),
                "due_date" : str(task.due_date),
                "status" : task.status,
                "created_by" : task.created_by,
                "time_spent" : task.time_spent
            }
        logger.debug("Task retrived")
        return result

    @jwt_required
    def delete(self,id):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            task = Task.query.filter_by(id = id).first()
            pid = task.project_id
            if pid in pd.keys():
                role = pd.get(pid)
                if role < 3:
                    task.is_active = False
                    subtasks = SubTask.query.filter_by(task_id = id).all()
                    if len(subtasks) > 0: 
                        for subtask in subtasks:
                            subtask.is_active = False
                    db.session.commit()
                    logger.debug("Task is changed to inactive")
                    return send_response({"message":"Task is changed to inactive", "_id" : str(id)}, status =202)
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError

        except Exception:
            raise UnauthorizedError

    @jwt_required
    def put(self,id):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            body = request.get_json()
            task = Task.query.get(id)
            pid = task.project_id
        
            ip_task = Task(task.project_id,body['task_name'],body['due_date'],body['estimated_time'], body['status'])
            
            if is_active_project(self,task.project_id) == False:
                raise InActiveError

            if check_authorised(self, pid, pd) == False:
                raise UnauthorizedError

            if task_validation(self,ip_task) == False and ip_task.status.lower() in ["open","progress","complete"] == False:
                raise InvalidInputError

            if date_validation(self,ip_task.due_date) == False:
                raise WrongDateError

            if time_validation(self,ip_task.estimated_time) == False:
                raise WrongTimeError
        
            task.estimated_time = ip_task.estimated_time
            task.due_date = ip_task.due_date
            task.status = ip_task.status
            task.task_name = ip_task.task_name
            db.session.commit()
            logger.debug("Task Updated {}".format(task.id))
            redis.publish('task', json.dumps(task.serialize()))
            
            logger.debug("Updated Task Published")
            return send_response({"message": "Task Update", "id" : str(task.id)},status=200)
        
        except KeyError:
            raise InvalidInputError        
        except exc.IntegrityError:
            raise AlreadyExistsError
        except TypeError:
            raise InvalidKeyError
        except UnauthorizedError:
            raise UnauthorizedError
        except InvalidInputError:
            raise InvalidInputError
        except WrongDateError:
            raise WrongDateError    
        except WrongTimeError:
            raise WrongTimeError


class TaskProjectApi(Resource):
    @jwt_required
    def get(self,p_id):
        tasks = Task.query.filter_by(project_id = p_id)
        
        results = [
            {
                "id" : task.id,
                "project_id" : task.project_id,
                "name" : task.task_name,
                "estimated_time" : str(task.estimated_time),
                "due_date" : str(task.due_date),
                "status" : task.status,
                "created_by" : task.created_by,
                "time_spent" : task.time_spent
            }for task in tasks
        ]
        logger.debug("Task retrived by Project")

        return {"count" : len(results) , "tasks" : results , "message" : 200}

class MyTasksApi(Resource):
    @jwt_required
    def get(self):
        data = get_jwt_claims()
        pd = get_projects_from_jwt(self, data)
        projects = pd.keys()
        project_obj = []
        for i in projects:
            project_obj.append(Project.query.get(i))
        results = []
        for p in project_obj:
            tasks = []
            tasks_obj = Task.query.filter_by(project_id = p.id).all()
            for names in tasks_obj:
                tasks.append(
                    {
                        "id" : names.id,
                        "task_name" : names.task_name,
                        "status" : names.status
                    })
            results.append({
                    "project_id" : p.project_id,
                    "name" : p.project_name,
                    "tasks" : tasks
                })
        logger.debug("Tasks retrived")
        return {"count" : len(results) , "tasks" : results , "message" : 200}
        
#inputs - user_id, is_assigned 
class RevokeUserFromTask(Resource):
    @jwt_required
    def put(self,id):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            body = request.get_json()
            task = Task.query.get(id)
            task_name = Task.query.get(id).task_name
            pid = task.project_id
            
            if check_authorised(self, task.project_id, pd) == False:
                raise UnauthorizedError
            if body['user_id'] == None:
                raise InvalidInputError

            if User.query.get(body['user_id']) == None:
                raise UserNotFound
            else:
                assi = check_exists(self,body['user_id'],id,None)
                if assi != None:
                        if body['is_assigned'] != None:
                            assi.is_assigned = body['is_assigned']
                            db.session.commit()
                            redis.publish('assignee', json.dumps(assi.serialize(pid,task_name, None)))
                            return send_response({"message": "Task Update", "id" : str(task.id)},status=200)
                        else:
                            raise InvalidInputError
                else:
                    raise UnAssignedTask
            
        except KeyError:
            raise InvalidInputError
        except UserNotFound:
            raise UserNotFound
        except UnAssignedTask:
            raise UnAssignedTask
        except UnauthorizedError:
            raise UnauthorizedError