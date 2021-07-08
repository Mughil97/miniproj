from Controller.projectController import ProjectController,ProjectUserController,RevokeUserController,DeleteProject,TestController
from Controller.milestoneController import MilestoneController,TaskMilestone

def initialize_routes(api):
    api.add_resource(ProjectController, '/api/project')
    api.add_resource(DeleteProject, '/api/project/<input_value>')
    api.add_resource(ProjectUserController,'/api/assignuser')
    api.add_resource(RevokeUserController,'/api/revokeuser')
    api.add_resource(MilestoneController, '/api/project/<int:project_id>/milestone')
    api.add_resource(TaskMilestone, '/api/project/<int:project_id>/milestone/<int:milestone_id>/task/<int:task_id>')
    api.add_resource(TestController,'/api/test')