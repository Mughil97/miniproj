from flask import make_response, jsonify
from db import db
from models.models import User, Password, Role, ProjectUser


class Services:

    def saveUser(self,object):
        db.session.add(object)
        db.session.commit()
        return object.user_id

    def savePassword(self,object):
        db.session.add(object)
        db.session.commit()
        return object.password_id

    def saveRole(self,object):
        db.session.add(object)
        db.session.commit()
        return object.role_id

    def saveProjectUser(self,app,object):
        with app.app_context():
            db.session.add(object)
            db.session.commit()
            return object.row_id
        

def sendResponse(result, status):
    response = make_response(jsonify(result), status)
    response.mimetype = 'application/json'
    return response
