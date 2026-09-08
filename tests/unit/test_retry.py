from event_platform.processing.retry import retry_delay

def test_retry_delay_exponential():
    assert retry_delay(0, 0.1) == 0.1
    assert retry_delay(1, 0.1) == 0.2
    assert retry_delay(2, 0.1) == 0.4
