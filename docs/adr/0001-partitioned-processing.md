# ADR 0001: Partitioned Event Processing

## Status
Accepted

## Decision
Partition events deterministically by business key and process each partition through a bounded queue.

## Trade-offs
Hot keys can create uneven load, partition-count changes alter routing, and production deployments
require durable partition ownership and rebalancing.
