from event_platform.processing.partition import partition_for

def test_partition_is_deterministic():
    assert partition_for("customer-42", 8) == partition_for("customer-42", 8)

def test_partition_is_in_range():
    for i in range(100):
        assert 0 <= partition_for(str(i), 4) < 4
