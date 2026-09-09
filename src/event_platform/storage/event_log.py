from collections import deque
from threading import Lock


class EventLog:
    def __init__(self, capacity: int = 10000):
        self._events = deque(maxlen=capacity)
        self._lock = Lock()

    def append(self, event):
        with self._lock:
            self._events.append(event)

    def size(self):
        with self._lock:
            return len(self._events)

    def snapshot(self):
        with self._lock:
            return list(self._events)
