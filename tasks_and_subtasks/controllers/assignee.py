import os
from flask import request, json
from flask_restful import Resource
from models.models import Assignee, Task, SubTask, ProjectUser
from db.db import db
from helpers.utils import send_response, check_exists, get_projects_from_jwt
from helpers.validations import *
from exceptions.exceptions import *
from config import Config
from ps.publish import redis
from flask_jwt_extended import jwt_required, get_jwt_claims

class AssigneeApi(Resource):
    
    @jwt_required
    def post(self):
        try:
            data = get_jwt_claims()
            pd = get_projects_from_jwt(self,data)
            body = request.get_json()
            assignee = Assignee(**body)
            proj_id = 0
            task_name = ""
            sub_task_name = None

            if User.query.get(assignee.user_id) == None:
                raise UserNotFound

            if Task.query.get(assignee.task_id) == None:
                raise TaskNotFound
            proj_id = Task.query.get(assignee.task_id).project_id
            
            if assignee.sub_task_id != None:
                if SubTask.query.get(assignee.sub_task_id) == None:
                    raise SubTaskNotFound
                else:
                    sub_task_name = SubTask.query.get(assignee.sub_task_id).sub_task_name
            
            task_name = Task.query.get(assignee.task_id).task_name
            
            if is_active_project(self,proj_id) ==  False:
                raise InActiveError

            if check_authorised(self,proj_id,pd) == False or assignee_in_project(self,assignee,proj_id) == False:
                raise UnauthorizedError
            
            if assignee_validation(self,assignee) ==  False:
                raise InvalidInputError

            if check_exists(self,assignee.user_id,assignee.task_id,assignee.sub_task_id) != None:
                raise AlreadyExistsError

            assignee.assigned_by = data['user_id']
            assignee.time_spent = "00:00:00"
            assignee.is_assigned = True
            db.session.add(assignee)
            db.session.commit()
            id = assignee.id
            logger.info("User assigned - {}".format(str(id)))
            redis.publish('assignee', json.dumps(assignee.serialize(proj_id, task_name, sub_task_name)))
            return send_response({"Message" : "Assigned" , "id" : str(id)}, status= 201)
            
        except AttributeError:
            raise InvalidInputError
        except AlreadyExistsError:
            raise AlreadyExistsError
        except InvalidInputError:
            raise InvalidInputError
        except UnauthorizedError:
            raise UnauthorizedError
            
    @jwt_required        
    def get(self):
        assignees = Assignee.query.all()
        results = [
            {
                "id" : assignee.id,
                "user_id" : assignee.user_id,
                "task_type" : assignee.task_type,
                "task_id" : assignee.task_id,
                "sub_task_id" : assignee.sub_task_id
            }for assignee in assignees
        ]

        return {"count" : len(results) , "tasks" : results , "message" : 200}


class AssigneeIdApi(Resource):
    @jwt_required
    def get(self, u_id):
        try:
            if User.query.get(u_id) == None:
                raise UserNotFound

            assignees = Assignee.query.filter_by(user_id = u_id)
            results = [
                {
                    "id" : assignee.id,
                    "user_id" : assignee.user_id,
                    "task_type" : assignee.task_type,
                    "task_id" : assignee.task_id,
                    "sub_task_id" : assignee.sub_task_id
                }for assignee in assignees
            ]
            return {"count" : len(results) , "tasks" : results , "message" : 200}

        except Exception:
            raise UserNotFound
            
class AssignedtoMeApi(Resource):
    @jwt_required
    def get(self):
        data = get_jwt_claims()
        u_id = data['user_id']
        assignees = Assignee.query.filter_by(user_id = u_id)
        results = [
            {
                "task_type" : assignee.task_type,
                "task_id" : assignee.task_id,
                "sub_task_id" : assignee.sub_task_id
            }for assignee in assignees
        ]
        return {"count" : len(results) , "tasks" : results , "message" : 200}

