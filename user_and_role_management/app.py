from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from logging.config import fileConfig
from errors.errors import errors
from db import initialize_db
from routes import initialize_routes
from publish import initialize_publisher
from testjwt import initialize_jwt
from subscribe import Listener
import logging
import redis
from mail import initialize_mail
# from ..common_code import testfile

# initializing flask app
app = Flask(__name__)

# configuring app
app.config.from_object('config.Config')

# initializing logging
fileConfig(fname='logging.cfg', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info("Logger Initialized")

# configuring api with custom errors
api = Api(app, errors=errors)

# initializing BCrypt
bcrypt = Bcrypt(app)



# initialize_jwt(app)
initialize_jwt(app)


# initializing db
initialize_db(app)
logger.info("Logger DB")

#initialize routes
initialize_routes(api)


initialize_mail(app)

initialize_publisher(app)


r = redis.Redis(host='localhost', port=6379, db=0)
client = Listener(app, r, 'ProjectUser')
client.start()


