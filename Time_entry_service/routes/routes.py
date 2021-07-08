from controllers.timelog import TimeLogApi
from controllers.totallogtime import ProjectLogTime
from controllers.totallogtime import TaskLogTime
from controllers.totallogtime import SubTaskLogTime
from controllers.timeforperiod import TimeForPeriod


def initialize_routes(api):        
    api.add_resource(TimeLogApi, '/api/timelog','/api/timelog/<int:id>')
    api.add_resource(ProjectLogTime, '/api/projecthours/<int:id>')
    api.add_resource(TaskLogTime, '/api/taskhours/<int:id>')
    api.add_resource(SubTaskLogTime, '/api/subtaskhours/<int:id>')
    api.add_resource(TimeForPeriod, '/api/timeforperiod/<int:id>')


