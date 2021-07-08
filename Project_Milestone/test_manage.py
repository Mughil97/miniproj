from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from config import db
from Model.models import Project

db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()