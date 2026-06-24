# Engineering operating rules

1. Work gate by gate. Do not implement a later gate while an earlier gate has a blocking safety, accounting, execution, or data-integrity defect.
2. Every phase begins with repository inspection, official-source identification, assumption review, module scope, acceptance tests, and risks.
3. Every numerical value must be classified as exchange-derived, empirically calibrated, customer policy, or logical invariant.
4. Never introduce live-risk defaults. Missing required customer policy keeps live trading disabled.
5. Never represent a timeout or ambiguous exchange response as a failed order. Mark it `STATUS_UNKNOWN` and reconcile by deterministic client identifier before any retry.
6. No component may bypass the future Binance request broker or subscription manager.
7. Prices, quantities, fees, PnL, risk, and exchange rounding use `Decimal`, integer ticks, or integer quantity steps at system boundaries.
8. Make changes in reviewable units; run and record affected tests; update ADRs, risk register, review report, and release readiness.
9. Never claim a test passed unless its command was run and its actual result was captured.
10. Never claim profitability, model approval, testnet validation, Windows compatibility, or live readiness without evidence.
11. Any material configuration change disarms live entries.
12. The safe default is `NO TRADE`; the safe production state is `LIVE_LOCKED`.
