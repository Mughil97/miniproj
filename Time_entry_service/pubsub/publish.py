import redis

r = redis.Redis(host='10.8.0.10', port=6379, db=0)
def initialize_publisher(app):
    r.pubsub()