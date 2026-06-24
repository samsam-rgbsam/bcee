# Data requirements

Data must be reproducible, versioned, time-aware, immutable for source events, and traceable from every decision back to raw evidence. Missing, stale, reordered, duplicated, gapped, or schema-incompatible data is explicit state and must never be silently treated as healthy.

## Source domains

- Binance public market streams: lightweight market-wide streams, bid/ask, depth deltas, aggressive trades, mark/funding/contract context.
- Broker-budgeted REST snapshots, exchange metadata, server time, and delist information.
- Authenticated user stream: orders/trades, account/margin/configuration, conditional trigger rejection, algo lifecycle, and expiry events.
- Authenticated reconciliation: balances, account, positions, open ordinary/algo orders, fills, commissions, account/symbol configuration, order-rate limits, leverage brackets, and quantitative-rule indicators.
- Internal events: candidates, features, proposals, risk decisions, requests/reservations, orders, fills, lots, protection, reconciliation, incidents, configuration/model releases, and operator actions.

## Versioned event envelope

Every internal event includes event/schema IDs and versions, producer/instance, correlation/causation IDs, business command/attempt/idempotency IDs where applicable, exchange event/transaction time, local monotonic and wall receive/processing time, request/stream/connection IDs, symbol/account scope, raw payload reference, normalized payload, and quality state.

Delivery is at least once. Consumers commit processed-event identity transactionally with state mutation.

## Storage

High-volume events use immutable partitioned Parquet with raw and normalized payloads, symbol, data type, UTC partition date, exchange/receive timestamps, sequence ID, connection ID, schema/recorder versions, and checksum. Partition/row-group/flush values are empirical operational calibrations, not guessed constants.

SQLite WAL stores configuration versions, customer policies, candidates, campaigns, rungs, virtual lots, ordinary/algo orders, fills, commissions, risk snapshots, request-budget observations, reconciliation records, model registry, audits, incidents, and release status. Foreign keys, explicit transactions, migrations, integrity checks, checksummed backups, restore tests, and append-only security audit behavior are required. Do not synchronously write every market event to SQLite and do not use SQLite polling for IPC.

DuckDB queries immutable Parquet and exported operational snapshots. Research jobs identify source partition checksums, extraction time, code/schema versions, universe/exclusions, and known defects. Research/replay cannot access production trading credentials.

## Deterministic replay

Each replay manifest fixes dataset, event-ordering rule, simulator, feature/model/config versions, seed, latency/cost/failure scenarios, and source commit. Duplicate, reordered, missing, delayed, disconnect, sequence-gap, stale-candidate, and unknown-status injections never mutate source data.

## Quality states

At minimum: `UNKNOWN`, `WARMING`, `HEALTHY`, `STALE`, `SEQUENCE_GAP`, `RECOVERING`, `SCHEMA_MISMATCH`, `CLOCK_UNCERTAIN`, `SOURCE_DISCONNECTED`, `DISK_DEGRADED`, and `INVALID`. Execution readiness requires every dependency to be healthy under source-specific freshness/synchronization rules.

## Feature/label lineage

Every feature records definition/version, input cutoff, computation time, units/type, and missing-data treatment. Labels record horizon, executable-price basis, competing-risk/censoring treatment, costs, and embargo group. Look-ahead leakage tests are mandatory.

## Retention and disk failure

Retention periods are customer policy. Free-space headroom is derived from measured event/database growth, flush/checkpoint behavior, emergency logging, backup/restore, and retention needs. Insufficient storage blocks new campaigns, preserves risk/protection/reconciliation/critical audit writes, reduces noncritical recording, alerts, and never automatically deletes fills, orders, incidents, or audit records.

Secrets, signatures, listen keys, credential handles, and sensitive headers never enter datasets, databases, logs, telemetry, or crash reports.
