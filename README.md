# BCEE — Binance Campaign Execution Engine

BCEE is a gated Windows/Python engineering project for a conservative Binance USD-M Futures directional-campaign platform.

## Current status

- Development phase: **Gate 0 — current facts and requirements**
- Gate 0 decision: **REJECTED / not passed**
- Trading mode: **LIVE_LOCKED**
- Exchange-order implementation: **not present**
- Profitability claim: **none**

Gate 0 is rejected because customer policy, authenticated account behavior, clean-Windows compatibility, testnet contract tests, model evidence, and operational validation are not yet available. No document in this repository authorizes live trading.

## Gate 0 deliverables

- `docs/binance/api-compatibility-matrix.md`
- `docs/requirements/product-requirements.md`
- `docs/quantitative/mathematical-specification.md`
- `docs/economics/economic-feasibility-specification.md`
- `docs/risk/customer-risk-policy.schema.json`
- `docs/data/data-requirements.md`
- `docs/operations/windows-python-compatibility-matrix.md`
- `docs/licensing/third-party-licensing-report.md`
- `docs/adr/`
- `docs/customer/unresolved-customer-inputs.md`
- `docs/reviews/gate-0-review.md`
- `release_readiness.json`

## Local Gate 0 validation

On Windows with the selected Python candidate installed:

```bat
doctor.bat
run_tests.bat
```

These commands validate documentation and safety-lock metadata only. They do not connect to Binance and cannot place orders.

## Safety boundary

Production execution must not be implemented or enabled until the compatibility matrix is current, customer policy is complete, all preceding gates pass, and the independent live interlocks described in the PRD are implemented and verified.
