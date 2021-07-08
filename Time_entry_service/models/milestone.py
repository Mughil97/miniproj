from db.db import db
from models.base import Base

class Milestone(Base):
    __tablename__ = 'milestone'

    id = db.Column(db.Integer, primary_key = True)
    milestone_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)