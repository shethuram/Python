import time
import multiprocessing
import threading

from task import Task
from redis_queue import pop, push_retry, push_dead, get_due_retries, remove_retry, publish, push
from backend import store

MAX_RETRIES = 3

def backoff(r):
    return 2 ** r

def worker(name):
    while True:
        data = pop()
        task = Task.deserialize(data)

        start = time.time()
        try:
            res = task.func(*task.args, **task.kwargs)
            duration = round(time.time() - start, 2)

            store(task.id, "SUCCESS", res, task.retries, duration)
            publish(f"SUCCESS:{task.id}")

            print(f"[{name}] Task {task.id} done in {duration}s")

        except Exception as e:
            task.retries += 1

            if task.retries > MAX_RETRIES:
                push_dead(task.serialize())
                store(task.id, "DEAD", None, task.retries)
                publish(f"DEAD:{task.id}")
                print(f"[{name}] Task {task.id} DEAD")

            else:
                delay = backoff(task.retries)
                push_retry(task.serialize(), time.time() + delay)
                publish(f"RETRY:{task.id}:{task.retries}")
                print(f"[{name}] Task {task.id} retry {task.retries} in {delay}s")

def retry_scheduler():
    while True:
        now = time.time()
        tasks = get_due_retries(now)

        for t in tasks:
            push(t)
            remove_retry(t)

        time.sleep(1)

def start_workers(n=2):
    for i in range(n):
        multiprocessing.Process(target=worker, args=(f"WORKER-{i+1}",)).start()

    threading.Thread(target=retry_scheduler, daemon=True).start()