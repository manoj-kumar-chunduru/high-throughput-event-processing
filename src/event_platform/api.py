from fastapi import FastAPI, HTTPException
from .config import Settings
from .domain.models import Event, PublishResponse
from .processing.engine import ProcessingEngine

settings = Settings()
engine = ProcessingEngine(settings.partitions, settings.queue_capacity, settings.workers, settings.max_retries, settings.retry_base_seconds)
app = FastAPI(title="High-Throughput Event Processing Platform", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready", "queue_depth": engine.queue_depth()}

@app.get("/metrics")
def metrics():
    data = engine.metrics.snapshot()
    data["queue_depth"] = engine.queue_depth()
    data["partitions"] = engine.partitions
    return data

@app.post("/v1/events", response_model=PublishResponse, status_code=202)
def publish(event: Event):
    try:
        partition = engine.publish(event)
    except RuntimeError as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc
    return PublishResponse(event_id=event.event_id, partition=partition, accepted=True)
