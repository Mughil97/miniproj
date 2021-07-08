import os

class Config(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'ourfirstprojet@acies'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:AciesGlobal@1@localhost:5432/mini_clickup"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPOGATE_EXCEPTIONS = True

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:AciesGlobal@1@localhost:5432/test_task"