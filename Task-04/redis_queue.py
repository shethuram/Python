import redis

r = redis.Redis(host="localhost", port=6379)

QUEUE = "queue:default"
RETRY = "queue:retry"
DEAD = "queue:dead"
CHANNEL = "events"

def push(task):
    r.lpush(QUEUE, task)

def pop():
    return r.brpop(QUEUE)[1]

def push_retry(task, time_score):
    r.zadd(RETRY, {task: time_score})

def get_due_retries(now):
    return r.zrangebyscore(RETRY, 0, now)

def remove_retry(task):
    r.zrem(RETRY, task)

def push_dead(task):
    r.lpush(DEAD, task)

def publish(msg):
    r.publish(CHANNEL, msg)

def get_redis():
    return r