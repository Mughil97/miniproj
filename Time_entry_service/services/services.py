from db.db import db
from models.user import User 
from models.project import Project

class Services:

    def save(self,app, object):
        with app.app_context():
            db.session.add(object)
            db.session.commit()
            return object.id

    def commit_project_user(self,app, pu, is_active):
        with app.app_context():
            pu.isActive = is_active
            db.session.merge(pu)
            db.session.commit()
    
    def query_service(self,app, pid, uid):
        with app.app_context():
            pu = Project.query.filter_by(user_id = uid, project_id = pid).first()
            return pu