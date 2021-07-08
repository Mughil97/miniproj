from db.db import db
from models.base import Base

class User(Base):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    fullname = db.Column(db.String, nullable=False)