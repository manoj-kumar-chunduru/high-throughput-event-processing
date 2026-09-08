import time

def retry_delay(attempt: int, base_seconds: float) -> float:
    if attempt < 0:
        raise ValueError("attempt must be non-negative")
    return base_seconds * (2 ** attempt)

def run_with_retry(fn, max_retries: int, base_seconds: float):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if attempt == max_retries:
                raise
            time.sleep(retry_delay(attempt, base_seconds))
    raise last_error
