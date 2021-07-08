import json
user = '{"user_id" : 4,"full_name" : "balu"}'
obj = json.loads(user)
print(obj['user_id'])