import os
from flask import Response, request, json
from flask_restful import Resource
from helpers.utils import *
from helpers.validations import *
from models.models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from exceptions.exceptions import *
from db.db import db
from config import Config
import jwt
from sqlalchemy import exc

class SubTaskApi(Resource):
    @jwt_required
    def post(self):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            body = request.get_json()
            sub_task = SubTask(body['task_id'],body['project_id'],body['sub_task_name'],body['due_date'],body['estimated_time'], None)
            
            if is_active_project(self,sub_task.project_id) == False:
                raise InActiveError
            
            if Task.query.get(sub_task.task_id) == None:
                raise TaskNotFound
            
            if task_in_project(self,sub_task) == False:
                raise TaskNotInProject
            
            if check_authorised(self, sub_task.project_id, pd) == False:
                raise UnauthorizedError

            if sub_task_validation(self,sub_task) == False:
                raise NulldataError
            
            if date_validation(self,sub_task.due_date) == False:
                raise WrongDateError

            if time_validation(self,sub_task.estimated_time) == False:
                raise WrongTimeError

             
            sub_task.created_by = data['user_id']
            sub_task.status = "open"
            sub_task.time_spent = "00:00:00"
            sub_task.is_active = True
            db.session.add(sub_task)
            db.session.commit()
            id = sub_task.id
            logger.debug("SubTask Added")
            return  send_response({'message': 'SubTask added','_id': str(id)}, status= 201)

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
        except NulldataError:
            raise NulldataError

    @jwt_required
    def get(self):
        subtasks = SubTask.query.all()
        results = [
            {
                "id" : subtask.id,
                "project_id" : subtask.project_id,
                "task_id" : subtask.task_id,
                "name" : subtask.sub_task_name,
                "estimated_time" : str(subtask.estimated_time),
                "due_date" : str(subtask.due_date),
                "status" : subtask.status,
                "created_by" : subtask.created_by,
                "time_spent" : subtask.time_spent
            }for subtask in subtasks
        ]
        logger.debug("SubTasks retrived")
        return {"count" : len(results) , "subtasks" : results , "message" : 200}

class SubTaskIdTask(Resource):
    @jwt_required
    def get(self,t_id):
        subtasks = SubTask.query.filter_by(task_id = t_id)
        
        results = [
            {
                "id" : subtask.id,
                "project_id" : subtask.project_id,
                "task_id" : subtask.task_id,
                "name" : subtask.sub_task_name,
                "estimated_time" : str(subtask.estimated_time),
                "due_date" : str(subtask.due_date),
                "status" : subtask.status,
                "created_by" : subtask.created_by,
                "time_spent" : subtask.time_spent
            }for subtask in subtasks
        ]
        logger.debug("SubTask retrived by Task")

        return {"count" : len(results) , "tasks" : results , "message" : 200}

class SubTaskIdApi(Resource):
    @jwt_required
    def get(self,id):
        subtask = SubTask.query.filter_by(id = id).first()
        
        result = {
                "id" : subtask.id,
                "project_id" : subtask.project_id,
                "task_id" : subtask.task_id,
                "name" : subtask.sub_task_name,
                "estimated_time" : str(subtask.estimated_time),
                "due_date" : str(subtask.due_date),
                "status" : subtask.status,
                "created_by" : subtask.created_by,
                "time_spent" : subtask.time_spent
            }
        logger.debug("SubTask retrived")

        return {"subtask" : result , "message" : 200}

    @jwt_required
    def put(self,id):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            body = request.get_json()
            subtask = SubTask.query.get(id)
            ip_sub = SubTask(subtask.task_id,subtask.project_id,body['sub_task_name'],body['due_date'],body['estimated_time'], None)
            status = body['status']
            
            if check_authorised(self, subtask.project_id, pd) == False:
                raise UnauthorizedError

            if sub_task_validation(self,ip_sub) == False and status.lower() in ["open","progress","complete"] == False:
                raise InvalidInputError

            if date_validation(self,ip_sub.due_date) == False:
                raise WrongDateError

            if time_validation(self,ip_sub.estimated_time) == False:
                raise WrongTimeError

            if is_active_project(self,subtask.project_id) == False:
                raise InActiveError 
            
            subtask.estimated_time = ip_sub.estimated_time
            subtask.due_date = ip_sub.due_date
            subtask.status = status
            subtask.sub_task_name = ip_sub.sub_task_name
            db.session.commit()
            logger.debug("SubTask Updated")
            return send_response({"message": "Task Update", "id" : str(subtask.id)},status=200)
            
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
