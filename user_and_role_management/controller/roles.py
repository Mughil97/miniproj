from flask import Response, request
from flask_restful import Resource
from models.models import Role
from errors.errors import InternalServerError
from db import db
from helpers import sendResponse
from publish import redis
import json


class RolesApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            role = Role(**body)
            db.session.add(role)
            db.session.commit()
            redis.publish('role', json.dumps(
                {"role_id": role.role_id, "role_name": role.role}))
            id = role.role_id
            return sendResponse({"message":"Successflly added","_id":id}, 401)
        except Exception as e:
            raise e
