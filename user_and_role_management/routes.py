from controller.roles import RolesApi
from controller.users import RegisterApi ,LoginApi, TestApi

def initialize_routes(api):
    api.add_resource(RolesApi, '/api/roles')
    api.add_resource(RegisterApi,'/api/register')
    api.add_resource(LoginApi,'/api/login')
    api.add_resource(TestApi,'/api/test')
