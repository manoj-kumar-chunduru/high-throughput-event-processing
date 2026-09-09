from time import perf_counter

from event_platform.domain.models import Event
from event_platform.processing.engine import ProcessingEngine

EVENTS = 10000


def main():
    engine = ProcessingEngine(partitions=8, queue_capacity=EVENTS, workers=8)
    start = perf_counter()
    for i in range(EVENTS):
        engine.publish(
            Event(
                event_id=f"bench-{i}",
                key=f"customer-{i % 1000}",
                event_type="benchmark",
                payload={"sequence": i},
            )
        )
    for queue in engine.queues:
        queue.join()
    elapsed = perf_counter() - start
    latencies = sorted(engine.metrics.latencies)
    processed = engine.metrics.snapshot()["events_processed"]

    def percentile(p):
        if not latencies:
            return 0.0
        return latencies[min(len(latencies) - 1, int(len(latencies) * p))] * 1000

    print(f"events={processed}")
    print(f"elapsed_seconds={elapsed:.4f}")
    print(f"events_per_second={processed / elapsed:.2f}")
    print(f"avg_latency_ms={(sum(latencies) / len(latencies)) * 1000:.4f}")
    print(f"p50_latency_ms={percentile(0.50):.4f}")
    print(f"p95_latency_ms={percentile(0.95):.4f}")
    print(f"p99_latency_ms={percentile(0.99):.4f}")
    engine.shutdown()


if __name__ == "__main__":
    main()
