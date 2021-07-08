class NotUnique(Exception):
    pass


class InternalServerError(Exception):
    pass


class UnauthorizedError(Exception):
    pass

class UserNotRegisteredError(Exception):
    pass

errors = {
    "NotUnique": {
        "message": "UserName or email already exists",
        "status": 409
    },
    "InternalServerError": {
        "message": "Internal error!!!",
        "status": 500
    },
    "UnauthorizedError": {
        "message": "Not authorized",
        "status": 403
    },
    "UserNotRegisteredError": {
        "message": "The user name is not registered",
        "status": 404
    }
}
