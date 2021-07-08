from Exceptions.exceptions import NullValueError,InvalidInputKey,ProjectExistError,Unauthorized,InvalidDueDate
from datetime import date,datetime
from datetime import timedelta,date,datetime
from config import db
from Model.models import Project,User,Role,ProjectUser,Task,Milestone,MilestoneTask,MilestoneTime
from logger import Mylogger

logger=Mylogger.logger
class CommonService:
    def myresponse(self,message,status):
        return {"message":message,"statusCode":status}
    
    def my_create_response(self,result_id,message,status):
        return {"id":result_id,"message":message,"statusCode":status}

    def total_time(self,times):
        total_secs = 0
        for tm in times:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs = total_secs // 60
        hr, min = divmod(total_secs, 60)
        s = ("%d:%02d:%02d" % (hr, min, 00))
        return s
    
    def due_date_validation(self,today,due_date):
        try:
            due_date_obj = datetime.strptime(due_date, '%m-%d-%Y').date()
            if today > due_date_obj:
                raise InvalidDueDate
        except Exception:
            raise InvalidDueDate

    def get_project_id(self,projects):
        result=[]
        for project in projects:
            result.append(int(project['id']))
        return result

    def get_project_role(self,projects):
        result=[]
        for project in projects:
            result.append(project['role'].lower())
        return result

    def null_validation(self,input_list):
        try:
            if '' in input_list:
                raise NullValueError
        except NullValueError:
            raise NullValueError

    def milestone_authorization(self,default_role,project_id,allowed_projects,allowed_roles):
        if default_role.lower() != 'admin':
            if not project_id in allowed_projects:
                logger.debug("No permission for project")
                raise Unauthorized
            if not 'ba' in allowed_roles and not 'project manager' in allowed_roles:
                logger.debug("No permission for this role")
                raise Unauthorized

    def tasks_exist_in_any_milestone(self,milestones,tasks):
        for milestone in milestones:
            task_list=db.session.query(MilestoneTask).filter(MilestoneTask.milestoneId==milestone.id).all()
            result_tasks=[]
            for task in task_list:
                if {"taskId":task.taskId} in tasks:
                    result_tasks.append({"taskId":task.taskId})
            if len(result_tasks)>0:
                return result_tasks
        return []

    def get_milestone_details(self,today,project_id,milestones):
        milestone_list=[]
        #Iterate all milestone in a project
        for milestone in milestones:
                completed=0
                total=0
                percentage=0
                task_list=db.session.query(MilestoneTask).filter(MilestoneTask.milestoneId==milestone.id).all()
                result_tasks=[]
                task_times=[]
                task_logged_time=[]
                for task in task_list:
                    total=total+1
                    task_obj=db.session.query(Task).filter(Task.taskId==task.taskId,Task.projectId==project_id).first()
                    if task_obj.status=="complete":
                        completed=completed+1
                    task_estimated_time=task_obj.estimatedTime
                    task_time=task_obj.time
                    task_times.append(task_estimated_time)
                    task_logged_time.append(task_obj.time)
                    result_tasks.append({"taskId":task.taskId,"estimatedTime":task_estimated_time,"timeLogged":task_time,"status":task_obj.status})
                if total != 0:
                    percentage=(completed/total)*100
                #get milestone's logged time
                due_date_obj = datetime.strptime(str(milestone.dueDate), '%Y-%m-%d').date()
                due_status="Normal"
                if percentage != 100 and due_date_obj < today:
                    due_status="Overdue"
                milestone_estimate=CommonService.total_time(self,task_times)
                task_log_time=CommonService.total_time(self,task_logged_time)
                milestone.completion=percentage
                db.session.commit()
                milestone_list.append({"milestoneId":milestone.id,"tasks":result_tasks,"estimatedTime":str(milestone_estimate),"completion %":percentage,"due_date":str(milestone.dueDate),"timeTracked":task_log_time,"due_status":due_status})    
        return milestone_list
   
    def test(self):
        try:
            raise ProjectExistError
        except InvalidInputKey:
            raise InvalidInputKey
        except ProjectExistError:
            raise ProjectExistError
        