from event_platform.domain.models import Event
from event_platform.processing.engine import ProcessingEngine


def test_small_processing_batch():
    engine = ProcessingEngine(partitions=4, queue_capacity=500, workers=4)
    for i in range(100):
        engine.publish(
            Event(
                event_id=f"perf-{i}",
                key=f"key-{i % 10}",
                event_type="benchmark",
                payload={"value": i},
            )
        )
    for queue in engine.queues:
        queue.join()
    assert engine.metrics.snapshot()["events_processed"] == 100
    engine.shutdown()
