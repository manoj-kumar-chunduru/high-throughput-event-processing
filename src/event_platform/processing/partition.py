import hashlib


def partition_for(key: str, partition_count: int) -> int:
    if partition_count <= 0:
        raise ValueError("partition_count must be positive")
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % partition_count
