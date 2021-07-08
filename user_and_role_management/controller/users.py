from flask import Response, request
from flask_restful import Resource
from models.models import User, Password, Role, ProjectUser
from errors.errors import InternalServerError, UnauthorizedError, UserNotRegisteredError
from db import db
from helpers import sendResponse, Services
import json
import logging
from publish import redis
from flask_mail import Message
from mail import mail
import datetime
from testjwt import jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_claims

logger = logging.getLogger(__name__)


@jwt.user_claims_loader
def create_token(identity):
    user = User()
    role = Role()
    project_user = ProjectUser()
    user_id = identity
    full_name = user.query.filter_by(user_id=user_id).first().full_name
    default_role = user.query.filter_by(user_id=user_id).first().role_id
    projects = project_user.query.filter_by(user_id=user_id).all()
    logger.debug(projects)
    projects_array = []
    for i in projects:
        projects_array.append(dict([
            ('id', i.project_id),
            ('role_id', i.user_role),
            ('hierachy_key', role.query.filter_by(role_id=i.user_role).first().hierachy_key)]
        ))
        logger.debug(dict([
                    ('id', i.project_id),
                    ('role_id', i.user_role),
                    ('hierachy_key', role.query.filter_by(role_id=i.user_role).first().hierachy_key)]
        ))
    token = {
        "user_id": identity,
        "full_name": full_name,
        "default_role": default_role,
        "projects": projects_array
    }
    return token


class RegisterApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            role = Role()
            user = User()
            password = Password()
            user.user_name = body["user_name"]
            user.email = body["email"]
            user.full_name = body["full_name"]
            role_body = None
            try:
                role_body = body["role"]
            except KeyError:
                role_body = 2
            else:
                role_body = role.query.filter_by(
                    role=body["role"]).first().role_id
            user.role_id = role_body
            logger.info(role_body)
            user_id = Services().saveUser(user)
            password.user_id = user_id
            password.password = body["password"]
            password.hash_password()
            password_id = Services().savePassword(password)
            redis.publish('user', json.dumps(
                {"full_name": user.full_name, "user_id": user.user_id}))
            return sendResponse({"user_id": user_id, "password_id": password_id}, 401)
        except Exception as e:
            raise e


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User()
            password = Password()
            body_password = body["password"]
            # user id
            db_user = user.query.filter_by(
                user_name=body["user_name"]).first().user_id
            if db_user:
                auth = password.check_password(db_user, body_password)
                if not auth:
                    raise UnauthorizedError
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(db_user, expires)
            return sendResponse({'token': access_token}, 200)
        except Exception as e:
            raise e


class TestApi(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        logger.debug(type(claims))
        return sendResponse(claims,200)


class ResetPassword(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User()
            password = Password()
            user_id = user.query.filter_by(user_name = body["user_name"]).first().user_id
            if user_id is None:
                raise UserNotRegisteredError
            return 
        except Exception as e:
            raise e
