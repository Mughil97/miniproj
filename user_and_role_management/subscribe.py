import redis
from models.models import ProjectUser
from helpers import Services
import logging
import threading
from flask import json
import time

logger = logging.getLogger(__name__)


class Listener(threading.Thread):
    def __init__(self, app, r, channels):
        threading.Thread.__init__(self)
        self.daemon = True
        self.app = app
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)

    def work(self, item):
        if item['data'] == "KILL":
            self.pubsub.unsubscribe()
        if item['type'] == 'message':
            obj = json.loads(item['data'])
            projectuser = ProjectUser()
            projectuser.project_id = obj['project_id']
            projectuser.user_id = obj['user_id']
            projectuser.user_role = obj['user_role']
            id = Services().saveProjectUser(self.app, projectuser)
            logger.info(id)
