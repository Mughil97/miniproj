from flask import Flask
from flask_restful import Api
from db.db import initialize_db
from helpers.logger import initialize_logger
from exceptions.exceptions import errors
from flask_jwt_extended import JWTManager
from logging.config import fileConfig
from routes.routes import initialize_routes
from pubsub.subscriber import UserListener
from pubsub.subscriber import ProjectListener
from pubsub.subscriber import TaskListener
from pubsub.subscriber import MilestoneListener
import redis
from pubsub.publish import initialize_publisher

app = Flask(__name__)
app.config.from_object('config.Config')
fileConfig(fname='logging.cfg', disable_existing_loggers=False)

api = Api(app, errors = errors)
jwt = JWTManager(app)

# Initialize the logger
initialize_logger(app)

# Initialize the database
initialize_db(app)

# Initialize the routes 
initialize_routes(api)

# Initalize Subsciber
r = redis.Redis(host='10.8.0.10', port=6379, db=0)
userclient = UserListener(app, r,'user')
projectclient = ProjectListener(app, r,'ProjectUser')
taskclient = TaskListener(app, r, 'assignee')
milestoneclient = MilestoneListener(app, r, 'Milestone')
userclient.start()
projectclient.start()
taskclient.start()
milestoneclient.start()

# Initialize Publisher
initialize_publisher(app)