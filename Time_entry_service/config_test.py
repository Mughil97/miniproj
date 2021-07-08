import os

class Config:
    JWT_SECRET_KEY = 'thismysecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:AciesGlobal@1@localhost:5432/pyflaskpoc_test'