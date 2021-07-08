from flask import Response, request
from flask_restful import Resource
from helpers.util import send_response
from helpers.logger import logging
from models.timelog import Timelog
from models.user import User
from models.project import Project
from models.task import Task
from models.milestone import Milestone
from exceptions.exceptions import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from db.db import db
from sqlalchemy import and_ 
import datetime, time
from validation.timevalidation import time_validation, total_time
from validation.queryfunction import user_query, task_query, subtask_query
from pubsub.publish import r
from flask import json
logger = logging.getLogger(__name__)

class TimeLogApi(Resource): 
    @jwt_required
    def post(self):
        x = get_jwt_claims()
        u_id = x['user_id']
        date_str = 'Invalid date, cannot log for future dates'
        date_res_str = 'Cannot log time for future date'
        timelog_str = 'Timelog entry is sucessfuly added'
        time_err_str = 'Cannot log more than 24 hours'
        try:
            body = request.get_json()
            timelog =  Timelog(**body)
            timelog.user_id = u_id
            time_logged = []
            time_user = []
            time_task = []
            time_subtask = []
            x = timelog.sub_task_id
            date_key = datetime.datetime.strptime(timelog.entry_date,"%Y-%m-%d").date()
            if(bool(x) == True):
                if(timelog.project_id == None or timelog.task_id == None or timelog.sub_task_id == None or timelog.hours_logged == None or timelog.entry_date == None or timelog.notes == None):
                    project_key = bool(Project.query.filter(and_(Project.project_id == timelog.project_id, Project.user_id == u_id, Project.isActive == True)).first())
                    task_key = bool(Task.query.filter(and_(Task.task_id == timelog.task_id, Task.project_id == timelog.project_id, Task.sub_task_id == timelog.sub_task_id, Task.user_id == u_id)).first())
                    if(project_key == True and task_key == True):
                        timelog_key = bool(Timelog.query.filter(and_(Timelog.user_id == timelog.user_id, Timelog.entry_date == timelog.entry_date)).all())
                        #Time validation for 24hour if data already exists in db
                        if(timelog_key == True):
                            y = Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.entry_date == timelog.entry_date)).all()
                            for z in y:
                                time_logged.append(str(z.hours_logged))
                            time_logged.append(str(timelog.hours_logged))
                            temp = time_validation(time_logged)
                            if(temp == True):
                                #Future date validation
                                if(date_key > datetime.date.today()):
                                    logger.error(date_str)
                                    return send_response({'message': date_res_str},400)
                                else:
                                    db.session.add(timelog)
                                    db.session.commit()
                                    #Total time for a user
                                    query_user = Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.task_id == timelog.task_id, Timelog.sub_task_id == timelog.sub_task_id)).all()
                                    time_user = user_query(query_user)
                                    #Total time for a task
                                    query_task = Timelog.query.filter( Timelog.task_id == timelog.task_id).all()
                                    time_task = task_query(query_task)
                                    #Total time for a subtask
                                    query_subtask = Timelog.query.filter(Timelog.sub_task_id == timelog.sub_task_id).all()
                                    time_subtask = subtask_query(query_subtask)                        
                                    mydict = {"user_id":u_id, "task_id":timelog.task_id, "sub_task_id":timelog.sub_task_id, "user_time":time_user, "task_time":time_task, "sub_task_time":time_subtask}
                                    logger.info("SubTask data is published")
                                    r.publish('timelog',json.dumps(mydict))
                                    logger.debug(timelog_str)
                                    return send_response({'message': timelog_str},201)
                            else:
                                logger.error(time_err_str)
                                return send_response({'message': time_err_str},400)
                        else:
                            #Time validation for new data
                            time_logged.append(str(timelog.hours_logged))
                            temp = time_validation(time_logged)
                            if(temp == True):
                                #Future date validation
                                if(date_key > datetime.date.today()):
                                    logger.error(date_str)
                                    return send_response({'message':  date_res_str},400)
                                else:
                                    db.session.add(timelog)
                                    db.session.commit()
                                    #Total time for a user
                                    query_user = Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.task_id == timelog.task_id, Timelog.sub_task_id == timelog.sub_task_id)).all()
                                    time_user = user_query(query_user)
                                    #Total time for a task
                                    query_task = Timelog.query.filter( Timelog.task_id == timelog.task_id).all()
                                    time_task = task_query(query_task)
                                    #Total time for a subtask
                                    query_subtask = Timelog.query.filter(Timelog.sub_task_id == timelog.sub_task_id).all()
                                    time_subtask = subtask_query(query_subtask)
                                    mydict = {"user_id":u_id, "task_id":timelog.task_id, "sub_task_id":timelog.sub_task_id, "user_time":time_user, "task_time":time_task, "sub_task_time":time_subtask}
                                    logger.info("SubTask data is published")
                                    r.publish('timelog',json.dumps(mydict))
                                    logger.debug(timelog_str)
                                    return send_response({'message': timelog_str},201)
                            else:
                                logger.error(time_err_str)
                                return send_response({'message': time_err_str},400)
                    else:
                        logger.error("Invalid Project/Task Id")
                        return send_response({'message':'Invalid Project/Task'},404)
                else:
                    logger.error("Null value exists")
                    return send_response({'message':'Null value exists'},400)
            else:
                if(timelog.project_id != None or timelog.task_id != None or timelog.hours_logged != None or timelog.entry_date != None or timelog.notes != None):
                    project_key = bool(Project.query.filter(and_(Project.project_id == timelog.project_id, Project.user_id == u_id)).first())
                    task_key = bool(Task.query.filter(and_(Task.task_id == timelog.task_id, Task.project_id == timelog.project_id, Task.user_id == u_id)).first())
                    if(project_key == True and task_key == True):
                        timelog_key = bool(Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.entry_date == timelog.entry_date)).all())
                        #Time validation for 24hour if data already exists in db
                        if(timelog_key == True):
                            y = Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.entry_date == timelog.entry_date)).all()
                            for z in y:
                                time_logged.append(str(z.hours_logged))
                            time_logged.append(str(timelog.hours_logged))
                            temp = time_validation(time_logged)
                            if(temp == True):
                                #Future date validation
                                if(date_key > datetime.date.today()):
                                    logger.error(date_str)
                                    return send_response({'message':date_res_str},400)
                                else:
                                    db.session.add(timelog)
                                    db.session.commit()
                                    #Total time for a user
                                    query_user = Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.task_id == timelog.task_id)).all()
                                    time_user = user_query(query_user)
                                    #Total time for a task
                                    query_task = Timelog.query.filter( Timelog.task_id == timelog.task_id).all()
                                    time_task = task_query(query_task)                              
                                    mydict = {"user_id":u_id, "task_id":timelog.task_id, "sub_task_id":timelog.sub_task_id, "user_time":time_user, "task_time":time_task, "sub_task_time": None}
                                    logger.info("Task data is published")
                                    r.publish('timelog',json.dumps(mydict))
                                    logger.debug(timelog_str)
                                    return send_response({timelog_str},201)
                            else:
                                logger.error(time_err_str)
                                return send_response({'message': time_err_str},400)
                        else:
                            #Time validation for new data
                            time_logged.append(str(timelog.hours_logged))
                            temp = time_validation(time_logged)
                            if(temp == True):
                                #Future date validation
                                if(date_key > datetime.date.today()):
                                    logger.error(date_str)
                                    return send_response({'message': date_res_str},400)
                                else:
                                    db.session.add(timelog)
                                    db.session.commit()
                                    #Total time for a user
                                    query_user = Timelog.query.filter(and_(Timelog.user_id == u_id, Timelog.task_id == timelog.task_id)).all()
                                    time_user = user_query(query_user)
                                    logger.info("User data is published")
                                    #Total time for a task
                                    query_task = Timelog.query.filter( Timelog.task_id == timelog.task_id).all()
                                    time_task = task_query(query_task)
                                    mydict = {"user_id":u_id, "task_id":timelog.task_id, "sub_task_id":timelog.sub_task_id, "user_time":time_user, "task_time":time_task, "sub_task_time": None}
                                    logger.info("Task data is published")
                                    r.publish('timelog',json.dumps(mydict))
                                    logger.debug(timelog_str)
                                    return send_response({'message': timelog_str},201)
                            else:
                                logger.error(time_err_str)
                                return send_response({'message': time_err_str},400)
                    else:
                        logger.error("Invalid Project/Task Id")
                        return send_response({'message':'Invalid Project/Task'},404)
                else:
                    logger.error("Null value exists")
                    return send_response({'message':'Null value exists'},400)
        except Exception:
            raise SchemaValidationError

    @jwt_required
    def get(self):
        x = get_jwt_claims()
        u_id = x["user_id"]
        temp = json.dumps(x)
        data = json.loads(temp)
        for z in data["projects"]:
            h_id = z["hierachy_key"]
        if(h_id == 1):
            log = Timelog.query.all()
        else:
            log = Timelog.query.filter(Timelog.user_id == u_id)
        results = [    
            {
                "id": timelog.id,
                "user_id": timelog.user_id,        
                "project_id": timelog.project_id,
                "task_id": timelog.task_id,
                "sub_task_id": timelog.sub_task_id,
                "hours_logged": timelog.hours_logged.strftime("%H:%M:%S"),
                "entry_date": timelog.entry_date.strftime("%Y-%m-%d"),
                "notes": timelog.notes 
            } for timelog in log]
        return {"count": len(results), "entries": results} 

    @jwt_required
    def delete(self,id):
        x = get_jwt_claims()
        u_id = x['user_id']
        try:
            timelog = Timelog.query.filter(and_(Timelog.id == id, Timelog.user_id == u_id)).first()
            if(bool(timelog) == True):
                db.session.delete(timelog)
                db.session.commit()
                return send_response({'message':'Timesheet entry deleted successfully','_id':str(id)},200) 
            else:
                return send_response({'message':'Invalid id','_id':str(id)},404)
        except Exception:
            raise InternalServerError
        
    @jwt_required
    def put(self,id):
        x = get_jwt_claims()
        u_id = x['user_id']
        try:
            body = request.get_json()
            timelog = Timelog.query.filter(and_(Timelog.id == id, Timelog.user_id == u_id)).first()
            if(bool(timelog)== True):
                timelog.hours_logged = body.get('hours_logged')
                timelog.notes = body.get('notes')
                db.session.commit()
                return send_response({'message':'Timesheet entry updated successfully','_id':str(id)},202)
            else:
                return send_response({'message':'Invalid id','_id':str(id)},404)
        except Exception:
            raise InternalServerError