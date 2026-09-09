from threading import Lock
from time import perf_counter


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self.accepted = 0
        self.processed = 0
        self.failed = 0
        self.retries = 0
        self.dead_lettered = 0
        self.latencies = []

    def increment(self, name, amount=1):
        with self._lock:
            setattr(self, name, getattr(self, name) + amount)

    def observe_latency(self, seconds):
        with self._lock:
            self.latencies.append(seconds)

    def snapshot(self):
        with self._lock:
            return {
                "events_accepted": self.accepted,
                "events_processed": self.processed,
                "events_failed": self.failed,
                "retry_attempts": self.retries,
                "dead_lettered": self.dead_lettered,
                "latency_samples": len(self.latencies),
            }


class Timer:
    def __init__(self, metrics):
        self.metrics = metrics

    def __enter__(self):
        self.started = perf_counter()
        return self

    def __exit__(self, *_):
        self.metrics.observe_latency(perf_counter() - self.started)
