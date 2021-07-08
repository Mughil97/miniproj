from db import db
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_bcrypt import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)

today = date.today() + relativedelta(months=+1)


class User(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role_table.role_id'), nullable=False)
    password = db.relationship('Password', backref='person', lazy=True)


class Password(db.Model):
    __tablename__ = 'password_table'
    password_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user_table.user_id'), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.String(100), default=today.strftime("%Y%m%d"))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self,user_id, password):
        db_password = self.query.filter_by(user_id = user_id).order_by(Password.expiry_date.desc()).first().password
        return check_password_hash(db_password, password)


class Role(db.Model):
    __tablename__ = 'role_table'
    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False, unique=True)
    hierachy_key = db.Column(db.Integer, nullable=False)
    role_relation = db.relationship('User', backref='role_table', lazy=True)


class ProjectUser(db.Model):
    __tablename__ = 'project_user'
    row_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_role = db.Column(db.Integer, nullable=False)
