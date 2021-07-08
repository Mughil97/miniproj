from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from db.db import db
from models.user import User
from models.project import Project
from models.task import Task
from models.timelog import Timelog
from models.base import Base
from models.milestone import Milestone

db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()