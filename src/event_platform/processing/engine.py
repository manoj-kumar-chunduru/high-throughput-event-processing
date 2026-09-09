from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Full, Queue
from threading import Event as ThreadEvent
from threading import Lock

from ..observability.metrics import Metrics, Timer
from .partition import partition_for
from .retry import run_with_retry


class ProcessingEngine:
    def __init__(
        self,
        partitions=4,
        queue_capacity=1000,
        workers=4,
        max_retries=3,
        retry_base_seconds=0.01,
    ):
        self.partitions = partitions
        self.queues = [Queue(maxsize=queue_capacity) for _ in range(partitions)]
        self.max_retries = max_retries
        self.retry_base_seconds = retry_base_seconds
        self.metrics = Metrics()
        self.dead_letter = Queue()
        self._processed_ids = set()
        self._id_lock = Lock()
        self._stop = ThreadEvent()
        self._pool = ThreadPoolExecutor(max_workers=workers)
        self._futures = [self._pool.submit(self._worker, p) for p in range(partitions)]

    def publish(self, event):
        partition = partition_for(event.key, self.partitions)
        try:
            self.queues[partition].put_nowait(event)
        except Full as exc:
            raise RuntimeError("partition queue is full; backpressure applied") from exc
        self.metrics.increment("accepted")
        return partition

    def _process(self, event):
        with self._id_lock:
            if event.event_id in self._processed_ids:
                return
            self._processed_ids.add(event.event_id)

    def _process_with_retry(self, event):
        return run_with_retry(
            lambda event=event: self._process(event),
            self.max_retries,
            self.retry_base_seconds,
        )

    def _worker(self, partition):
        queue = self.queues[partition]

        while not self._stop.is_set() or not queue.empty():
            try:
                event = queue.get(timeout=0.05)
            except Empty:
                continue

            try:
                with Timer(self.metrics):
                    self._process_with_retry(event)
                self.metrics.increment("processed")
            except RuntimeError:
                self.metrics.increment("failed")
                self.dead_letter.put(event)
                self.metrics.increment("dead_lettered")
            finally:
                queue.task_done()

    def queue_depth(self):
        return sum(q.qsize() for q in self.queues)

    def shutdown(self):
        self._stop.set()

        for queue in self.queues:
            queue.join()

        self._pool.shutdown(wait=True)
