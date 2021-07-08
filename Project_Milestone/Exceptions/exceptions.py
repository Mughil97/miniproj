class InternalServerError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class EmailDoesnotExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass

class InvalidColumnError(Exception):
    pass

class ProjectExistError(Exception):
    pass

class ProjectNotFound(Exception):
    pass

class UserNotFound(Exception):
    pass

class RoleNotFound(Exception):
    pass

class UserNotInProject(Exception):
    pass

class TaskNotFound(Exception):
    pass

class  MilestoneExistError(Exception):
    pass

class InvalidInputKey(Exception):
    pass

class InvalidDueDate(Exception):
    pass

class MilestoneNotFound(Exception):
    pass

class TaskNotFoundInMilestone(Exception):
    pass

class Unauthorized(Exception):
    pass

class TaskExistInMilestone(Exception):
    pass

class UserAlreadyWorkingError(Exception):
    pass

class NullValueError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "EmailDoesnotExistsError": {
         "message": "Couldn't find the user with given email address",
         "status": 400
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 403
     },

     "InvalidColumnError": {
         "message": "Invalid Column",
         "status": 400
     },
     
     "ProjectExistError": {
         "message": "Project already exist",
         "status": 409
     },
      
     "ProjectNotFound": {
         "message": "Project Not Found",
         "status": 400
     },

     "UserNotFound": {
         "message": "User Not Found",
         "status": 400
     },

     "RoleNotFound": {
         "message": "Role Not Found",
         "status": 400
     },

     "UserNotInProject": {
         "message": "User not working in this project",
         "status": 400
     },

     "TaskNotFound": {
         "message": "Task Not Found in this project",
         "status": 400
     },

     "MilestoneExistError": {
         "message": "Given task is already in a milestone",
         "status": 409
     },

     "UserAlreadyWorkingError": {
         "message": "User already working in this project",
         "status": 409
     },

     "TaskExistInMilestone": {
         "message": "Given task is already in this milestone",
         "status": 409
     },

     "InvalidInputKey": {
         "message": "Invalid Input Key",
         "status": 400
     },

     "InvalidDueDate": {
         "message": "Invalid Due Date",
         "status": 400
     },

     "MilestoneNotFound": {
         "message": "Milestone Not Found in this project",
         "status": 400
     },

     "TaskNotFoundInMilestone": {
         "message": "Task Not Found in this Milestone",
         "status": 400
     },

     "Unauthorized": {
         "message": "No access permission",
         "status": 401
     },

     "NullValueError": {
         "message": "Null value identified",
         "status": 400
     }
}
