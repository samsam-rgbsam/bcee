# ADR-0003: Exact numeric and storage boundaries

- Status: Accepted for architecture
- Date: 2026-06-23

Exchange prices, quantities, commissions, PnL, risk, and tick/step rounding use `Decimal` and integer tick/quantity-step representations. Binary float is allowed only inside isolated numerical/model arrays and must not cross exchange/accounting boundaries without validated conversion.

Operational transactional state uses SQLite WAL with foreign keys, explicit transactions, migrations, integrity checks, backups, and append-only audit controls. High-volume immutable events use partitioned Parquet. DuckDB performs research queries. SQLite polling is not real-time IPC and every market event is not synchronously written to SQLite.
