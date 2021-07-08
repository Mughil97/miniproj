from controllers import sub_task,assignee, task

def initialize_routes(api):
    api.add_resource(task.TaskApi,'/api/task')
    api.add_resource(task.TaskIdApi,'/api/task/<id>')
    api.add_resource(task.MyTasksApi,'/api/mytasks')
    api.add_resource(task.TaskProjectApi,'/api/task/project/<p_id>')
    api.add_resource(task.RevokeUserFromTask,'/api/task/user/<id>')
    api.add_resource(sub_task.SubTaskApi,'/api/subtask')
    api.add_resource(sub_task.SubTaskIdApi,'/api/subtask/<id>')
    api.add_resource(sub_task.SubTaskIdTask,'/api/subtask/task/<t_id>')
    api.add_resource(assignee.AssigneeApi,'/api/assignee/task')
    api.add_resource(assignee.AssignedtoMeApi,'/api/assignee/mytasks')
    api.add_resource(assignee.AssigneeIdApi,'/api/assignee/<u_id>')
    