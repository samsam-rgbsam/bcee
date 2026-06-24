# Product Requirements Document

**Version:** 0.1.0  
**Reviewed:** 2026-06-23  
**Phase:** Gate 0  
**Decision:** not approved beyond Gate 0

## Objective

BCEE shall discover, validate, simulate, and—only after all gates pass—execute conservative directional campaigns on customer-permitted Binance USD-M Futures instruments. It shall optimize conservative risk-adjusted net geometric growth after costs and uncertainty, subject to customer policy, exchange constraints, liquidity, drawdown controls, data quality, execution reliability, and operational safety.

BCEE shall never promise profitability. `NO_TRADE` is required whenever economics, data, risk, protection, reconciliation, request capacity, model approval, or operational state is stale, unsupported, marginal, or uncertain.

## Operating modes

`REPLAY`, `PAPER`, `SHADOW`, `TESTNET`, `LIVE_LOCKED`, and `LIVE_ARMED` are distinct modes. Every UI surface and structured log shall display the mode. `run_live.bat` may start only `LIVE_LOCKED`; it shall never arm trading.

## Required architecture

- All Binance REST/WebSocket API requests pass through `BinanceRequestBroker`.
- All stream subscription commands pass through `BinanceSubscriptionManager`.
- Scanner 1 performs market-wide discovery and never approves or submits an order.
- Scanner 2 validates a warmed hot set and emits typed, expiring execution proposals; it never submits an order.
- One serialized execution actor per symbol owns position assumptions, virtual lots, exit reservations, protection, exposure, and campaign state.
- Risk and protection processes are independent from the UI.
- Internal delivery is at least once and consumers are idempotent.
- SQLite WAL stores operational state; immutable Parquet stores high-volume events; DuckDB serves research; SQLite polling is not real-time IPC.

## Exchange and market-data requirements

Exchange metadata, account configuration, filters, commissions, rate limits, leverage brackets, available balance, trading status, and server time shall be retrieved dynamically and persisted with source, retrieval timestamp, raw/parsed values, scope, validity, symbol, account-profile hash, and schema version. No exchange-derived value is a production business constant.

Market events shall preserve exchange event/transaction time, local receive/processing time, sequence IDs, stream/connection IDs, raw payload reference, schema version, and quality state. The official snapshot-plus-delta order-book algorithm is mandatory. Any sequence gap makes the book execution-ineligible until complete recovery.

## Campaign, rung, and execution requirements

A campaign records direction, distributions, time horizon, model/feature/configuration versions, remaining movement, risk, exposure, current rung, proposed rung, and state. At most one future rung may be armed. Price crossing does not authorize entry: current model, economics, risk, data, protection, budget, and reconciliation approvals are separately required. Skipped rungs are not chased.

Default entry intent is aggressive limit IOC with a bounded execution price derived from current depth, quantity, conservative slippage, remaining economic edge, and current exchange filters. Market entry and server-hosted conditional entry remain behind separately disabled feature flags until evidence supports them.

No-fill, partial-fill, full-fill, rejection, unknown status, STP expiry, delisting cancellation, and incomplete market fill have explicit state transitions. Every confirmed fill becomes a virtual lot; unconfirmed quantity never does. Aggregate exit fills use one documented deterministic allocation policy.

Timeout, connection loss, malformed/unexpected response, missing acknowledgement, HTTP/error states documented as execution-unknown, or any ambiguous outcome produce `STATUS_UNKNOWN`. Blind retry is prohibited. Reconciliation by deterministic client identifier, user events, positions, and orders must prove non-execution before a new attempt.

## Protection and reconciliation

After any position increase, required exchange-resident catastrophic protection must be submitted/resized and independently confirmed. Algo acceptance alone is not protection. Rejected, expired, unexpectedly canceled, or uncertain protection forces `RISK_ONLY`, blocks entries, attempts approved fallback, and closes exposure when protection cannot be confirmed.

Startup and every uncertainty trigger shall reconcile persisted state with account configuration, balances, positions, open ordinary orders, open algo orders, fills, commissions, and user events. Manual Binance activity disarms the application and requires operator-reviewed reconciliation; it is never silently adopted.

## Request-budget requirements

Every applicable IP, account order, WebSocket API, control-message, connection-attempt, stream-count, symbol-order, symbol-algo, and quantitative-rule budget is tracked separately by scope and window. Requests reserve pessimistic capacity before transmission. Missing counters retain pessimistic debits.

Entry is forbidden unless capacity remaining after the complete entry workflow still covers the dynamically derived emergency plan to cancel armed entries, query unknown orders, repair protection, close positions, confirm final positions/orders, and reconcile. No fixed reserve percentage is permitted.

## Security and operations

Production credentials use Windows DPAPI or Credential Manager and never appear in source, `.env`, batch files, command arguments, SQLite plaintext, logs, telemetry, or crash reports. REPLAY/PAPER/SHADOW/TESTNET/LIVE use separate credential and data boundaries. Non-live components cannot access production trading credentials.

A Python supervisor enforces single instance, child health, safe restart, orphan detection, crash reporting, and shutdown. It never reactivates trading after a trader crash; reconciliation is required. Closing the UI must not terminate protected trading components.

Disk thresholds are derived from observed rates and recovery requirements. Insufficient storage blocks new campaigns while preserving risk, protection, reconciliation, and critical audit writes. Fills, orders, incidents, and audit records are never automatically deleted.

## Non-configurable invariants

```text
sum(open_virtual_lot_quantity) == reconciled_exchange_position_quantity
sum(reserved_and_active_exit_quantity) <= reconciled_reducible_position_quantity
campaign_risk <= customer_campaign_risk_limit
portfolio_risk <= customer_portfolio_risk_limit
at_most_one_future_rung_armed_per_campaign
no_new_entry_when_market_data_is_stale
no_new_entry_when_order_book_is_unsynchronized
no_new_entry_when_account_state_is_unreconciled
no_new_entry_when_user_stream_is_unhealthy
no_new_entry_when_request_budget_is_insufficient
no_new_entry_when_emergency_request_reserve_is_insufficient
no_new_entry_when_protection_cannot_be_installed
no_live_order_without_explicit_production_arming
```

Any violation is a critical incident.

## Production arming predicate

`LIVE_ARMED` requires all of: supported environment, valid credentials, account can trade, complete customer policy, compliance acknowledgement, release integrity, reconciliation, healthy market data and request budget, approved model release, healthy risk engine, and explicit operator arming. No single UI switch or operator role may bypass this predicate.

## Current restriction

Production order transmission, strategy thresholds, customer risk numbers, and profitability claims are absent by design. Gate 0 remains rejected.
