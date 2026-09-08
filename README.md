# High-Throughput Event Processing Platform

A production-oriented event processing platform demonstrating high-throughput ingestion,
partitioning, concurrency, retries, backpressure, observability, and fault-tolerant
distributed-system design.

## Overview
The platform separates ingestion from processing and deterministically routes events by key.
Independent partitions process concurrently while preserving FIFO behavior within each partition.

This self-contained implementation is designed for local experimentation. It does not claim
production Kafka throughput without benchmark evidence.

## Architecture
```text
Producers
   |
   v
Ingestion API (FastAPI)
   |
   v
Partition Router (SHA-256 key)
   |
   v
Bounded Partition Queues
   |
   v
Concurrent Workers
   |------------|
   v            v
Retry/Backoff  Dead Letter Queue
   |
   v
Event Handler

Observability: health + readiness + metrics
```

## Tech Stack
- Python 3.11+
- FastAPI / Pydantic
- ThreadPoolExecutor
- Pytest / Ruff
- Docker / Docker Compose
- Kubernetes
- GitHub Actions

## Key Features
- REST event ingestion
- Deterministic key-based partitioning
- Concurrent workers
- Per-key ordering within a partition
- Idempotent event IDs
- Bounded queues and backpressure
- Exponential retry/backoff
- Dead-letter handling
- Graceful shutdown
- Health/readiness/metrics endpoints
- Unit, integration, concurrency and performance tests
- Throughput/latency benchmark
- Docker and Kubernetes artifacts
- CI pipeline

## API Examples
Publish:
```bash
curl -X POST http://localhost:8000/v1/events -H "Content-Type: application/json" -d "{"event_id":"evt-1001","key":"customer-42","event_type":"order.created","payload":{"order_id":"ord-9001"}}"
```

Health:
```bash
curl http://localhost:8000/health
```

Readiness:
```bash
curl http://localhost:8000/ready
```

Metrics:
```bash
curl http://localhost:8000/metrics
```

## Project Structure
```text
high-throughput-event-processing/
├── src/event_platform/
│   ├── api.py
│   ├── config.py
│   ├── domain/models.py
│   ├── processing/engine.py
│   ├── processing/partition.py
│   ├── processing/retry.py
│   ├── storage/event_log.py
│   └── observability/metrics.py
├── tests/unit/
├── tests/integration/
├── tests/concurrency/
├── tests/performance/
├── benchmarks/throughput_benchmark.py
├── docs/
├── k8s/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

## Running Locally
```bash
python -m venv .venv
```
Windows:
```bash
.venv\Scripts\activate
```
Linux/macOS:
```bash
source .venv/bin/activate
```
Install:
```bash
pip install -e ".[dev]"
```
Run:
```bash
uvicorn event_platform.api:app --reload
```

## Testing
```bash
pytest
ruff check .
```

## Benchmarking
```bash
python benchmarks/throughput_benchmark.py
```
The benchmark reports events/sec and average/p50/p95/p99 latency. Results depend on the host,
runtime, workload, partition count and worker count. They must not be represented as production
capacity.

## Observability
- `/health`
- `/ready`
- `/metrics`

## Reliability
The design demonstrates bounded queues, controlled retries, exponential backoff, dead-letter
handling, idempotency, graceful shutdown and isolated event failures.

## CI/CD
GitHub Actions installs dependencies, runs Ruff, and executes the test suite.

## Engineering Principles
- Preserve ordering where business keys require it.
- Apply backpressure instead of unbounded memory growth.
- Isolate failures to individual events.
- Make retries bounded and observable.
- Measure before claiming performance.
- Document operational behavior.

## Future Improvements
- Apache Kafka integration
- Durable consumer offsets
- Schema registry
- OpenTelemetry tracing
- Distributed partition rebalancing
- Persistent state stores
- Autoscaling based on consumer lag

## Author
**Manoj Kumar Chunduru**  
Software Engineer
