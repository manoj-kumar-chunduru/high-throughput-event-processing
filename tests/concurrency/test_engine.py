from concurrent.futures import ThreadPoolExecutor

from event_platform.domain.models import Event
from event_platform.processing.engine import ProcessingEngine


def test_concurrent_publish():
    engine = ProcessingEngine(partitions=4, queue_capacity=1000, workers=4)

    def publish(i):
        return engine.publish(
            Event(
                event_id=f"evt-{i}", key=f"customer-{i % 20}", event_type="test", payload={"i": i}
            )
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(publish, range(200)))

    for queue in engine.queues:
        queue.join()
    assert engine.metrics.snapshot()["events_processed"] == 200
    engine.shutdown()
