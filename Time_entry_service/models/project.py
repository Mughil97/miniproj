from db.db import db
from models.base import Base

class Project(Base):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key = True)
    project_id = db.Column(db.Integer, nullable=False)
    project_name = db.Column(db.String,  nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
