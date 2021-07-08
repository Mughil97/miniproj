from flask import Response, request
from flask_restful import Resource
from helpers.util import send_response
from helpers.logger import logging
from models.timelog import Timelog
from models.user import User
from models.project import Project
from models.task import Task
from exceptions.exceptions import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from db.db import db
from sqlalchemy import Date, and_ ,or_
import datetime, time
from validation.timevalidation import total_time, time_function, time_function_filter
from flask import json


logger = logging.getLogger(__name__)
user_str = 'User does not exist'
total_str = 'Total duration'
hour_str = 'Total hours is obtained'

class ProjectLogTime(Resource):
    @jwt_required
    def get(self,id):    
        user_id = request.args.get('user_id')
        dt = request.args.get('day')
        mnth = request.args.get('month')
        yr = request.args.get('year')
        #Total hours of project if no user_id is present
        if(bool(user_id)==False):
            project_key = Timelog.query.filter(Timelog.project_id == id)
            data = time_function(project_key)
            if data == True:
                logger.debug(hour_str, data)
                return send_response({'message':'Total hours for task',total_str : data},202)
            else:
                logger.error('Invalid Project id',id)
                return send_response({'message':'Invalid Project id','id':id},404)
        #Total hours of project with user_id and filters
        else:
            project_key_filter = Timelog.query.filter(and_(Timelog.project_id == id, Timelog.user_id == user_id)).all()
            data = time_function_filter(user_id, project_key_filter, dt, mnth, yr)
            if(data == True):
                logger.debug(hour_str, data)
                return send_response({'message':'Total hours for a user in project',total_str : data},202)
            else:
                logger.error('Invalid Project for user',user_id)
                return send_response({'message':'Invalid Project for user','user_id':user_id},404)

             

class TaskLogTime(Resource):
    @jwt_required
    def get(self,id):
        user_id = request.args.get('user_id')
        dt = request.args.get('day')
        mnth = request.args.get('month')
        yr = request.args.get('year')
        #Total hours of task if no user_id is present
        if(bool(user_id) == False):
            task_key = Timelog.query.filter(Timelog.task_id == id).all()
            data = time_function(task_key)
            if(data==True):
                logger.debug(hour_str, data)
                return send_response({'message':'Total hours for task',total_str : data},202)
            else:
                logger.error('Invalid Task id',id)
                return send_response({'message':'Invalid Task id','id':id},404)
        #Total hours of task with user_id and filters
        else:
            task_key_filter = Timelog.query.filter(and_(Timelog.task_id == id, Timelog.user_id == user_id)).all()
            data = time_function_filter(user_id, task_key_filter, dt, mnth, yr)
            if(data == True):
                logger.debug(hour_str, data)
                return send_response({'message':'Total hours for a user in task',total_str : data},202)
            else:
                logger.error('Invalid Task for user',user_id)
                return send_response({'message':'Invalid Task for user','user_id':user_id},404)
                
        
                  

             


class SubTaskLogTime(Resource):
    @jwt_required
    def get(self,id):
        user_id = request.args.get('user_id')
        dt = request.args.get('day')
        mnth = request.args.get('month')
        yr = request.args.get('year')
        #Total hours of subtask with no user_id
        if(bool(user_id)==False):
            sub_task_key = Timelog.query.filter(Timelog.sub_task_id == id).all()
            data = time_function(sub_task_key)
            if(data==True):
                logger.debug(hour_str, data)
                return send_response({'message':'Total hours for subtask',total_str : data},202)
            else:
                logger.error('Invalid Subtask id',id)
                return send_response({'message':'Invalid SubTask id','id':id},404)
        #Total hours of subtask with user_id and filters
        else:
            sub_task_filter_key = Timelog.query.filter(and_(Timelog.sub_task_id == id, Timelog.user_id == user_id)).all()
            data = time_function_filter(user_id, sub_task_filter_key, dt, mnth, yr)
            if(data==True):
                logger.debug(hour_str, data)
                return send_response({'message':'Total hours for a user in subtask',total_str : data},202)
            else:
                logger.error('Invalid SubTask for user',user_id)
                return send_response({'message':'Invalid SubTask for user','user_id':user_id},404)


           


