import time
import threading
import socket

from task import Task
from redis_queue import push, publish
from worker import start_workers
from dashboard import start_dashboard

# ===== SIMPLE TASKS =====
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def fail_task(x):
    raise Exception("intentional failure")

# ===== PRODUCER =====
def enqueue(func, *args, **kwargs):
    t = Task(func, args, kwargs)
    push(t.serialize())
    publish(f"QUEUED:{t.id}:{func.__name__}")
    print(f"Task queued: <Task id={t.id} func={func.__name__}>")

# ===== MAIN =====
if __name__ == "__main__":
    print("=== Broker ===")
    print("[BROKER] Redis running")

    # Start dashboard (socket server)
    threading.Thread(target=start_dashboard, daemon=True).start()

    # Start workers
    start_workers(2)

    time.sleep(1)

    print("\n=== Producer ===")
    enqueue(add, 2, 3)
    enqueue(multiply, 4, 5)
    enqueue(fail_task, 10)

    # Wait for processing
    time.sleep(18)

    print("\n=== Dashboard ===")
    s = socket.socket()
    s.connect(("localhost", 9999))
    print(s.recv(4096).decode())
    s.close()