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
from datetime import datetime

class TimeForPeriod(Resource):
    @jwt_required
    def get(self,id):
        x = get_jwt_claims()
        u_id = x['user_id']
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            #if(start_date == None and end_date == None)
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()     
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            project_key = bool(Timelog.query.filter(Timelog.project_id == id).all()) 
            if(project_key == True):
                entries = Timelog.query.filter(Timelog.project_id == id).filter(Timelog.user_id == u_id).filter(Timelog.entry_date <= end_date).filter(Timelog.entry_date >= start_date)
                results = [      
                    {
                        "id" : timelog.id,
                        "user_id" : timelog.user_id,
                        "project_id" : timelog.project_id,
                        "task_id" : timelog.task_id,
                        "sub_task_id" : timelog.sub_task_id, 
                        "entry_date": timelog.entry_date.strftime("%Y-%m-%d"),
                        "hours_logged": timelog.hours_logged.strftime("%H:%M:%S"),                    
                        "notes": timelog.notes 
                    } for timelog in entries ]
                if (len(results)!=0):
                    return {"count": len(results), "entries": results}
                else:
                    return {"No entries available",u_id}
            else:
                return('No Project available for given Id',u_id) 
        except Exception:
            raise InternalServerError 
  
