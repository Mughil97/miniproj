class InternalServerError(Exception):
    pass

class InvalidInputError(Exception):
    pass

class AlreadyExistsError(Exception):
    pass

class TaskExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class EmailDoesnotExistsError(Exception):
    pass

class TokenAuthenticationError(Exception):
    pass

class TokenMissingError(Exception):
    pass

class BadTokenError(Exception):
    pass

class InActiveError(Exception):
    pass

class WrongDateError(Exception):
    pass

class WrongTimeError(Exception):
    pass

class InvalidKeyError(Exception):
    pass

class NulldataError(Exception):
    pass

class UserNotFound(Exception):
    pass

class ProjectNotFound(Exception):
    pass

class TaskNotFound(Exception):
    pass

class SubTaskNotFound(Exception):
    pass

class TaskNotInProject(Exception):
    pass

class UnAssignedTask(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "UnAssignedTask" : {
        "message" : "Unassigned Task",
        "status" : 400
    },
    "TaskNotInProject": {
        "message": "Task not in project",
        "status": 400
    },
    "UserNotFound": {
        "message": "User Not Found",
        "status": 404
    },
    "ProjectNotFound": {
        "message": "Project Not Found",
        "status": 404
    },
    "TaskNotFound":{
        "message" : "Task Unavailable",
        "status": 404
    },
    "SubTaskNotFound":{
        "message" : "SubTask Unavailable",
        "status": 404
    },
     "InvalidInputError": {
         "message": "Invalid Input",
         "status": 400
     },
     "AlreadyExistsError": {
         "message": "Already Assigned task",
         "status": 409
     },
     "TaskExistsError": {
         "message": "Task Exists already",
         "status": 409
     },
     "UnauthorizedError": {
         "message": "Unauthorized",
         "status": 401
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 400
     },
     "InActiveError":{
         "message" : "InActive project",
         "status" : 400
     },
     "NulldataError":{
         "message" : "Value is Null",
         "status" : 400
     },

     "WrongDateError":{
        "message" : "InValid date",
         "status" : 400
     },
     "WrongTimeError":{
        "message" : "InValid time",
        "status" : 400
     },
     "InvalidKeyError" :{
         "message" : "Invalid Key",
         "status" : 400
     },
    "TokenAuthenticationError":{
        "message" : "InValid token signature",
        "status" : 400
    },
    "TokenMissingError":{
        "message" : "Token Missing",
        "status" : 400
    }
}
