import os
import redis
from flask import Flask,request,jsonify
from flask_restful import Api
from db.db import initialize_db
from db.db import db
from exceptions.exceptions import errors
from logging.config import fileConfig
from routes.routes import initialize_routes
from flask_bcrypt import Bcrypt
from config import *
from ps.subscriber import Listener
from ps.publish import initialize_publisher
from jwt_auth import initialize_jwt, jwt

app = Flask(__name__)

app.config.from_object(ProductionConfig())

fileConfig(fname='logger.cfg',disable_existing_loggers=False)

bcrypt = Bcrypt(app)

api = Api(app, errors = errors)

initialize_db(app)

initialize_jwt(app)

initialize_routes(api)

r = redis.Redis(host='localhost', port=6379, db=0)
project = Listener(app, r,'project')
project.start()
project_user = Listener(app,r ,'ProjectUser')
project_user.start()
user = Listener(app,r,'user')
user.start()
time_log = Listener(app,r,'timelog')
time_log.start()

initialize_publisher(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
