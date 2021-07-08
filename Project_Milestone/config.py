import os
from flask import Flask,jsonify
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy import create_engine

db=SQLAlchemy()
def initialize_db_env(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AciesGlobal@1@localhost:5432/project'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)

def initialize_db_test(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AciesGlobal@1@localhost:5432/project_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)

class JwtConfig:
    JWT_SECRET_KEY = 'ourfirstprojet@acies'

