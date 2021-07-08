import redis

redis = redis.Redis('localhost', port=6379, db=0)

def initialize_publisher(app): 
    redis.pubsub()
