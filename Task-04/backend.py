import json
from redis_queue import get_redis

r = get_redis()

def store(task_id, status, result=None, retries=0, duration=None):
    data = {
        "status": status,
        "result": str(result),
        "retries": retries,
        "duration": duration
    }
    r.set(f"result:{task_id}", json.dumps(data))

def get_all():
    keys = r.keys("result:*")
    results = []
    for k in keys:
        task_id = k.decode().split(":")[1]
        data = json.loads(r.get(k))
        results.append((task_id, data))
    return results