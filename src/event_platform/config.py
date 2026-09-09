import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    partitions: int = int(os.getenv("EVENT_PARTITIONS", "4"))
    queue_capacity: int = int(os.getenv("EVENT_QUEUE_CAPACITY", "1000"))
    workers: int = int(os.getenv("EVENT_WORKERS", "4"))
    max_retries: int = int(os.getenv("EVENT_MAX_RETRIES", "3"))
    retry_base_seconds: float = float(os.getenv("EVENT_RETRY_BASE_SECONDS", "0.01"))
