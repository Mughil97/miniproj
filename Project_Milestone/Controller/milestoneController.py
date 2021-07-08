from flask import Response, request,jsonify,json
from flask_restful import Resource
from logger import Mylogger
from Exceptions.exceptions import NullValueError,ProjectExistError,Unauthorized,InvalidInputKey,InternalServerError,ProjectNotFound,RoleNotFound,UserNotFound,UserAlreadyWorkingError,UserNotInProject,MilestoneExistError
from Exceptions.exceptions import InvalidDueDate,TaskNotFound,UnauthorizedError,MilestoneNotFound,TaskExistInMilestone,TaskNotFoundInMilestone
from Model.models import Project,User,Role,ProjectUser,Task,Milestone,MilestoneTask,MilestoneTime
from config import db
from Service.dbService import DbService
from Service.commonService import CommonService
from datetime import date,datetime
from datetime import timedelta,date,datetime
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt_claims
from Helpers.staticValues import internal_server_error,project_not_found

logger=Mylogger.logger

class MilestoneController(Resource):
    @jwt_required
    def post(self,project_id):
        try:
            logger.debug("Entered create Milestone method")
            today=datetime.now().date()
            tokendata=get_jwt_claims()
            allowed_projects=CommonService.get_project_id(self,tokendata['projects'])
            allowed_roles=CommonService.get_project_role(self,tokendata['projects'])
            #project and role authorization
            CommonService.milestone_authorization(self,tokendata['default_role_name'],project_id,allowed_projects,allowed_roles)
            data=request.get_json()
            #Check error in input key
            try:
                due_date=data['dueDate']
                tasks=data['tasks']
            except Exception:
                raise InvalidInputKey
            #null validation
            input_list=[]
            input_list.append(due_date)
            for task in tasks:
                input_list.append(task['taskId'])
            CommonService.null_validation(self,input_list)
            #Due_date validation
            CommonService.due_date_validation(self,today,due_date)
            #Check for project existance
            DbService.is_project_exist(self,project_id)
            #Check for task existance
            DbService.is_tasks_exist_in_project(self,project_id,tasks)
            #get all milestones for given project
            milestones=db.session.query(Milestone).filter(Milestone.projectId==project_id).all()
            #check whether given tasks is present in any existing milestone
            result_tasks=CommonService.tasks_exist_in_any_milestone(self,milestones,tasks)
            if len(result_tasks)>0:
                return CommonService.myresponse(self,result_tasks,200)
            #comment raise MilestoneExistError
            milestone_obj=Milestone(projectId=project_id,dueDate=due_date)
            DbService.save(self,milestone_obj)
            for task in tasks:
                milestone_task_obj=MilestoneTask(milestoneId=milestone_obj.id,taskId=task["taskId"])
                DbService.save(self,milestone_task_obj)
            return CommonService.my_create_response(self,milestone_obj.id,"Created Successfully",201)
        except Unauthorized:
            raise Unauthorized
        except  InvalidDueDate:
            raise InvalidDueDate
        except InvalidInputKey:
            raise InvalidInputKey
        except TaskNotFound:
            raise TaskNotFound
        except MilestoneExistError:
            raise MilestoneExistError
        except ProjectNotFound:
            raise ProjectNotFound
        except ProjectExistError:
            raise ProjectExistError
        except NullValueError:
            raise NullValueError
        except Exception:
            logger.debug(internal_server_error)
            raise InternalServerError

    @jwt_required
    def get(self,project_id):
        try:
            logger.debug("Entered List milestone method")
            tokendata=get_jwt_claims()
            allowed_projects=CommonService.get_project_id(self,tokendata['projects'])
            #checking user has permission for given project
            if not project_id in allowed_projects:
                raise Unauthorized
            today=datetime.now().date()
            DbService.is_project_exist(self,project_id)
            milestones=db.session.query(Milestone).filter(Milestone.projectId==project_id).all()
            #get all milestone details for given project
            milestone_list=CommonService.get_milestone_details(self,today,project_id,milestones)
            return {"projectId":project_id,"milestones":milestone_list}
        except Unauthorized:
            raise Unauthorized
        except TaskNotFound:
            raise TaskNotFound
        except MilestoneExistError:
            raise MilestoneExistError
        except ProjectNotFound:
            raise ProjectNotFound
        except ProjectExistError:
            raise ProjectExistError
        except Exception:
            logger.debug(internal_server_error)
            raise InternalServerError

class TaskMilestone(Resource):   
    def post(self,project_id,milestone_id,task_id):
        try:
            logger.debug("Entered add task in milestone method")
            #check for project existence
            DbService.is_project_exist(self,project_id)
            #check for milestone existence
            DbService.is_milestone_exist(self,milestone_id)
            #Check for task existence in project
            DbService.is_task_exist(self,task_id,project_id)
            #check for task existence in any milestone
            milestonetask_obj=db.session.query(MilestoneTask).filter(MilestoneTask.taskId==task_id).first()
            if milestonetask_obj != None:
                if milestonetask_obj.milestoneId==milestone_id:
                    logger.debug("Task already present in this milestone")
                    raise TaskExistInMilestone
                else:
                    logger.debug("Task already present in a milestone")
                    raise MilestoneExistError
            milestonetask_obj=MilestoneTask(milestoneId=milestone_id,taskId=task_id)
            DbService.save(self,milestonetask_obj)
            return CommonService.myresponse(self,"Task Added Successfully",200)
        except TaskExistInMilestone:
            raise TaskExistInMilestone
        except TaskNotFoundInMilestone:
            raise TaskNotFoundInMilestone
        except MilestoneNotFound:
            raise MilestoneNotFound
        except TaskNotFound:
            raise TaskNotFound
        except MilestoneExistError:
            raise MilestoneExistError
        except ProjectNotFound:
            raise ProjectNotFound
        except ProjectExistError:
            raise ProjectExistError
        except Exception:
            logger.debug(internal_server_error)
            raise InternalServerError

    def delete(self,project_id,milestone_id,task_id):
        try:
            logger.debug("Entered Remove milestone method")
            #check for project existence
            DbService.is_project_exist(self,project_id)
            #check for milestone existence
            m_obj=DbService.is_milestone_exist(self,milestone_id)
            #Check for task existence in project
            DbService.is_task_exist(self,task_id,project_id)
            #check for task existence in this milestone
            milestonetask_obj=db.session.query(MilestoneTask).filter(MilestoneTask.milestoneId==milestone_id,MilestoneTask.taskId==task_id).first()
            if milestonetask_obj == None:
                logger.debug("Task not found in this milestone")
                raise TaskNotFoundInMilestone
            db.session.delete(milestonetask_obj)
            db.session.commit()
            milestone_list=db.session.query(MilestoneTask).filter(MilestoneTask.milestoneId==milestone_id).all()
            if len(milestone_list) == 0:
                logger.debug("Deleted milestone instance,No tasks available")
                db.session.delete(m_obj)
                db.session.commit()
            return CommonService.myresponse(self,"Task Deleted Successfully",200)
        except TaskNotFoundInMilestone:
            raise TaskNotFoundInMilestone
        except MilestoneNotFound:
            raise MilestoneNotFound
        except TaskNotFound:
            raise TaskNotFound
        except MilestoneExistError:
            raise MilestoneExistError
        except ProjectNotFound:
            raise ProjectNotFound
        except ProjectExistError:
            raise ProjectExistError
        except Exception:
            logger.debug(internal_server_error)
            raise InternalServerError