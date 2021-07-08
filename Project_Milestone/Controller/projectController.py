from flask import Response, request,jsonify,json
from flask_restful import Resource
from logger import Mylogger
from Exceptions.exceptions import NullValueError,ProjectExistError,Unauthorized,InvalidInputKey,InternalServerError,ProjectNotFound,RoleNotFound,UserNotFound,UserAlreadyWorkingError,UserNotInProject
from Model.models import Project,User,Role,ProjectUser,Task,Milestone,MilestoneTask
from config import db
from Service.dbService import DbService
from Service.commonService import CommonService
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt_claims

logger=Mylogger.logger
class ProjectController(Resource):
    @jwt_required
    def post(self):
        try:
            logger.debug("Entered create project method")
            tokendata=get_jwt_claims()
            if tokendata['default_role_name'].lower() != 'admin':
                raise Unauthorized
            data=request.get_json()
            try:
                project_name=data['projectName'].lower()
            except Exception:
                raise InvalidInputKey
            input_list=[]
            input_list.append(project_name)
            CommonService.null_validation(self,input_list)
            p_obj=db.session.query(Project).filter(Project.projectName==project_name,Project.isActive==True).first()
            if p_obj==None:
                p_obj=Project(projectName=project_name)
                DbService.save(self,p_obj)
                from app import r
                project_data={"id":p_obj.id,"projectName":p_obj.projectName,"isActive":p_obj.isActive}
                r.publish('project', json.dumps(project_data))
                logger.debug('project published successfully')
                logger.debug("project created Successfully")
            else:
                logger.debug("Error : project already exist")
                raise ProjectExistError
            return CommonService.my_create_response(self,p_obj.id,"Created Successfully",201)
        except NullValueError:
            raise NullValueError
        except Unauthorized:
            raise Unauthorized
        except InvalidInputKey:
            raise InvalidInputKey
        except ProjectExistError:
            raise ProjectExistError
        except Exception:
            logger.debug("Error : Internal Server Error")
            raise InternalServerError
    
    @jwt_required
    def get(self):
        try:
            tokendata=get_jwt_claims()
            allowed_projects=CommonService.get_project_id(self,tokendata['projects'])
            result=[]
            #Iterate all allowed project of authenticated user from jwt
            for project in allowed_projects:
                proj_obj=db.session.query(Project).filter(Project.id==project,Project.isActive==True).first()
                result_project={"projectId":proj_obj.id,"projectName":proj_obj.projectName}
                #Get all users of a project
                user_obj=db.session.query(ProjectUser).filter(ProjectUser.projectId==project,ProjectUser.isActive==True).all()
                #Iterate each user in project
                users=[]
                for user in user_obj:
                    users.append({"userId":user.userId,"roleId":user.roleId})
                #Get all tasks of a project
                task_obj=db.session.query(Task).filter(Task.projectId==project).all()
                #Iterate each task in a project
                tasks=[]
                for task in task_obj:
                    tasks.append({"taskId":task.taskId,"taskName":task.taskName,"status":task.status,"estimatedTime":task.estimatedTime,"timeLogged":task.time})
                result_project['users']=users
                result_project['tasks']=tasks
                result.append(result_project)
            return result
        except Unauthorized:
            raise Unauthorized
        except InvalidInputKey:
            raise InvalidInputKey
        except ProjectExistError:
            raise ProjectExistError
        except Exception:
            logger.debug("Error : Internal Server Error")
            raise InternalServerError

class DeleteProject(Resource):
    @jwt_required
    def delete(self,input_value):
        try:
            tokendata=get_jwt_claims()
            if tokendata['default_role_name'].lower() != 'admin':
                raise Unauthorized
            p_obj=db.session.query(Project).filter(Project.id==input_value,Project.isActive==True).first()
            if p_obj==None:
                raise ProjectNotFound
            tasks=db.session.query(Task).filter(Task.projectId==input_value,Task.status!='complete').first()
            if tasks!=None:
               return CommonService.myresponse(self,"pending Tasks available",400)
            p_obj.isActive=False
            db.session.commit()
            from app import r
            project_data={"id":p_obj.id,"projectName":p_obj.projectName,"isActive":p_obj.isActive}
            r.publish('project', json.dumps(project_data))
            logger.debug('project delete published successfully')
            logger.debug("project deleted Successfully")
            return CommonService.myresponse(self,"Deleted Successfully",200)
        except InvalidInputKey:
            raise InvalidInputKey
        except ProjectNotFound:
            raise ProjectNotFound
        except UserNotFound:
            raise UserNotFound
        except RoleNotFound:
            raise RoleNotFound
        except Unauthorized:
            raise Unauthorized
        except  Exception:
            raise InternalServerError

class ProjectUserController(Resource):
    @jwt_required
    def post(self):
        try:
            tokendata=get_jwt_claims()
            if tokendata['default_role_name'].lower() != 'admin':
                raise Unauthorized
            logger.debug("Entered assign user to project method")
            data=request.get_json()
            try:
                project_id=data['projectId']
                user_id=data['userId']
                role=data['role'].lower()
            except Exception:
                raise InvalidInputKey
            input_list=[]
            input_list.append(project_id)
            input_list.append(user_id)
            input_list.append(role)
            CommonService.null_validation(self,input_list)
            #Checking whether project available or not
            p_obj=db.session.query(Project).filter(Project.id==project_id,Project.isActive==True).first()
            if p_obj==None:
                logger.debug("Error : project Not Found")
                raise ProjectNotFound
            #Checking whether user available or not
            u_obj=db.session.query(User).filter(User.userId==user_id).first()
            if u_obj==None:
                logger.debug("Error : user Not Found")
                raise UserNotFound
            #Checking whether Role available or not
            r_obj=db.session.query(Role).filter(Role.roleName==role).first()
            if r_obj==None:
                logger.debug("Error : role Not Found")
                raise RoleNotFound
            #Checking user with project
            proj_user_obj=db.session.query(ProjectUser).filter(ProjectUser.projectId==p_obj.id,ProjectUser.userId==u_obj.userId,ProjectUser.isActive==True).first()
            if proj_user_obj == None:
                proj_user=ProjectUser(projectId=p_obj.id,userId=u_obj.userId,roleId=r_obj.id)
                DbService.save(self,proj_user)
                from app import r
                data={"project_id":proj_user.projectId,"user_id":proj_user.userId,"is_active":proj_user.isActive,"role_id":proj_user.roleId,"project_name":p_obj.projectName}
                r.publish('ProjectUser', json.dumps(data))
                return CommonService.myresponse(self,"User assigned Successfully",200)
            else:
                raise UserAlreadyWorkingError
        except NullValueError:
            raise NullValueError
        except UserAlreadyWorkingError:
            raise UserAlreadyWorkingError
        except InvalidInputKey:
            raise InvalidInputKey
        except ProjectNotFound:
            raise ProjectNotFound
        except UserNotFound:
            raise UserNotFound
        except RoleNotFound:
            raise RoleNotFound
        except Unauthorized:
            raise Unauthorized
        except  Exception:
            raise InternalServerError

class RevokeUserController(Resource):
    @jwt_required
    def put(self):
        try:
            tokendata=get_jwt_claims()
            if tokendata['default_role_name'].lower() != 'admin':
                raise Unauthorized
            logger.debug("Entered revoke user from project method")
            data=request.get_json()
            try:
                project_id=data['projectId']
                user_id=data['userId']
            except Exception:
                raise InvalidInputKey
            input_list=[]
            input_list.append(project_id)
            input_list.append(user_id)
            CommonService.null_validation(self,input_list)
            #Checking whether project available or not
            p_obj=db.session.query(Project).filter(Project.id==project_id,Project.isActive==True).first()
            if p_obj==None:
                logger.debug("Error : project Not Found")
                raise ProjectNotFound
            #Checking whether user available or not
            u_obj=db.session.query(User).filter(User.userId==user_id).first()
            if u_obj==None:
                logger.debug("Error : user Not Found")
                raise UserNotFound
            #Checking user with project
            proj_user_obj=db.session.query(ProjectUser).filter(ProjectUser.projectId==p_obj.id,ProjectUser.userId==u_obj.userId,ProjectUser.isActive==True).first()
            if proj_user_obj == None:
                raise UserNotInProject
            else:
                proj_user_obj.isActive=False #Soft Delete
                proj_user_obj.dateEnd=db.func.now() #DateEnd for history purpose
                db.session.commit()
                from app import r
                data={"project_id":proj_user_obj.projectId,"user_id":proj_user_obj.userId,"is_active":proj_user_obj.isActive,"role_id":proj_user_obj.roleId,"project_name":p_obj.projectName}
                r.publish('ProjectUser', json.dumps(data))
                return CommonService.myresponse(self,"User Successfully Revoked from project",200)
        except InvalidInputKey:
            raise InvalidInputKey
        except UserNotInProject:
            raise UserNotInProject
        except ProjectNotFound:
            raise ProjectNotFound
        except UserNotFound:
            raise UserNotFound
        except RoleNotFound:
            raise RoleNotFound
        except Unauthorized:
            raise Unauthorized
        except NullValueError:
            raise NullValueError
        except  Exception:
            raise InternalServerError

class TestController(Resource):
    def get(self):
        CommonService.test(self)
        return "Success"
    
    def post(self):
        data=request.get_json()
        input_list=[]
        input_list.append(data['test1'])
        input_list.append(data['test2'])
        CommonService.null_validation(self,input_list)
        return "Success"