from event_platform.storage.event_log import EventLog


def test_event_log_append_size_and_snapshot():
    log = EventLog()

    log.append("event-1")
    log.append("event-2")

    assert log.size() == 2
    assert log.snapshot() == ["event-1", "event-2"]


def test_event_log_respects_capacity():
    log = EventLog(capacity=2)

    log.append("event-1")
    log.append("event-2")
    log.append("event-3")

    assert log.size() == 2
    assert log.snapshot() == ["event-2", "event-3"]
