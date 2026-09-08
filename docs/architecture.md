# Architecture

Events are deterministically routed by SHA-256(event key). Each partition has a bounded queue
and worker. This enables concurrency across partitions while preserving FIFO behavior within
a partition. The local implementation demonstrates application-level idempotency; production
systems would persist offsets and processed state.
