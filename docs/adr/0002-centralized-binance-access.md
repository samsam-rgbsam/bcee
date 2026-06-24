# ADR-0002: Centralize all Binance access

- Status: Accepted for architecture
- Date: 2026-06-23

All Binance REST and WebSocket API commands pass through `BinanceRequestBroker`; all market subscription commands pass through `BinanceSubscriptionManager`. Scanners, models, UI, trader, research, and reconciliation may not call Binance directly.

This boundary owns credentials, signing, server-time uncertainty, compatibility checks, deterministic IDs, unknown-status recovery, multidimensional rate/order/connection budgets, strict priorities, state-derived emergency reserve, and telemetry. A lower-priority component cannot bypass or consume capacity reserved for risk reduction.
