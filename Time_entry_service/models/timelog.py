from db.db import db
from models.base import Base
from sqlalchemy import Date, Time

class Timelog(Base):
    __tablename__ = 'timelog'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    sub_task_id = db.Column(db.Integer)
    hours_logged = db.Column(db.Time, nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String)
  