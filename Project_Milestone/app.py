import os,json
from flask import Flask,jsonify,request
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy import create_engine
from config import initialize_db_env
from flask_restful import Api
from logging.config import fileConfig
from flask_jwt_extended import JWTManager
from logger import Mylogger
from Exceptions.exceptions import errors
from Route.routes import initialize_routes
import redis
from pubsub.subscriber import Listener
from flask_jwt_extended import JWTManager

logger=Mylogger.logger
app=Flask(__name__)
api = Api(app,errors=errors)
app.config.from_object('config.JwtConfig')
jwt = JWTManager(app)
fileConfig(fname='logging.cfg',disable_existing_loggers=False)
initialize_db_env(app)
initialize_routes(api)
logger.debug("Application starts")
#Initialize Subscriber
r = redis.Redis(host='localhost', port=6379, db=0)
pub = r.pubsub()
userclient = Listener(app, r,'user')
userclient.start()
taskclient = Listener(app, r,'task')
taskclient.start()
roleclient = Listener(app, r,'role')
roleclient.start()
