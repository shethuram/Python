import uuid
import pickle

class Task:
    def __init__(self, func, args=None, kwargs=None):
        self.id = str(uuid.uuid4())[:6]
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.retries = 0

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)