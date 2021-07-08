import unittest
from db.db import db
from app import app
from config import TestingConfig
from models.models import User, Project, ProjectUser, Task, SubTask, Assignee

class TestBase(unittest.TestCase):

    jso = "application/json" 
    access_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTEyNzYzNjIsIm5iZiI6MTU5MTI3NjM2MiwianRpIjoiMzI4YmZkNDItZjhhYy00MzFlLThiYTEtNjI3NzM4M2JlMTk1IiwiaWRlbnRpdHkiOjMsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsInVzZXJfY2xhaW1zIjp7InVzZXJfaWQiOjEsImZ1bGxfbmFtZSI6Ik1vaGFuIiwiZGVmYXVsdF9yb2xlIjoxLCJkZWZhdWx0X3JvbGVfbmFtZSI6ImFkbWluIiwicHJvamVjdHMiOlt7ImlkIjoxLCJyb2xlX2lkIjo1LCJyb2xlIjoiYmEiLCJoaWVyYWNoeV9rZXkiOjF9XX19.oht65iZD54zAHD12M81ykFnPvn1j4vmfy6srIci3Vo4"
    headers = {
            "Content-Type": jso,
            'Authorization': access_token
        }

    def setUp(self):
        with app.app_context():
            app.config.from_object(TestingConfig())
            self.app = app.test_client()
            db.drop_all()
            db.create_all()
            db.session.add(User(1,"Levi"))
            db.session.add(User(2,"Rahul"))
            db.session.add(User(3,"Eren"))
            db.session.add(Project(1,"VM", True))
            db.session.add(Project(2,"PS", False))
            db.session.add(Project(3,"Testlabs", True))
            db.session.add(ProjectUser(1,1,True))
            db.session.add(ProjectUser(2,1,True))
            db.session.add(ProjectUser(3,1,False))
            # db.session.add(ProjectUser(1,2,False))
            db.session.add(Task(1, "Task Testing", "07/10/2020", "30:00:00", "open"))
            db.session.add(Task(1, "Timelog task", "07/10/2020", "30:00:00", "open"))
            db.session.add(Task(3, "Test Project", "07/10/2020", "30:00:00", "open"))
            db.session.commit()
            task_id = Task.query.filter_by(task_name = "Task Testing").first().id
            task_id_2 = Task.query.filter_by(task_name = "Timelog task").first().id
            db.session.add(SubTask(1, task_id, "Subtask Testing", "08/10/2020", "10:00:00", "open"))
            db.session.add(SubTask(1, task_id_2, "Subtask timelog", "08/10/2020", "10:00:00", "open"))
            db.session.commit()
            ass = {'user_id': 1, 'task_type': 'sub_task', 'task_id': '2', 'sub_task_id': '2'}
            assignee = Assignee(**ass)
            db.session.add(assignee)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()