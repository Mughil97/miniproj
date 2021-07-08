import redis

redis = redis.Redis(host='localhost', port=6379, db=0)


def initialize_publisher(app):
    pub = redis.pubsub()


