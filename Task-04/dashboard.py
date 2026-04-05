import socket
from backend import get_all

def start_dashboard():
    server = socket.socket()
    server.bind(("localhost", 9999))
    server.listen(5)

    print("[DASHBOARD] Running on port 9999")

    while True:
        client, _ = server.accept()

        data = "Task ID | Status | Retries | Duration\n"
        for task_id, d in get_all():
            data += f"{task_id} | {d['status']} | {d['retries']} | {d['duration']}\n"

        client.send(data.encode())
        client.close()