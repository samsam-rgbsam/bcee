# Economic feasibility specification

**Status:** UNVERIFIED; no executable edge demonstrated

The objective is conservative net geometric growth after commission, spread, slippage, market impact, funding, latency, model error, protection cost, operational failures, and tail risk. Trade count, gross profit, maximum leverage, and time in market are not objectives.

## Required baseline comparison

Under identical signals, data, risk budget, costs, latency assumptions, and validation periods compare:

1. one entry with fixed exit;
2. one entry with app-managed reversal exit;
3. one entry with exchange trailing exit;
4. one entry with partial profit-taking;
5. rolling ladder with aggregate exit;
6. rolling ladder with virtual-lot exits.

Measure net expectancy, net geometric growth, profit factor, drawdown, expected shortfall, turnover, fees/gross profit, slippage/gross profit, holding time, capacity, profit/loss by rung, frequency the final rung erases earlier profit, symbol/regime stability, and cost/latency sensitivity. Report sample sizes and uncertainty intervals.

## Simulation standard

Candle-only backtesting is invalid. Deterministic event replay must model bid/ask, depth, aggressive trades, IOC partial fill and canceled remainder, fees, spread, slippage, impact, signal/submission/ack/fill latency, stop triggering, trigger rejection, reversal exits, funding, tick/step rounding, disconnects, sequence gaps, stale candidates, missed trades, and unknown order status.

Where queue position or event ordering is unknowable, assumptions must be documented and conservative, then stress-tested.

## Cost and capacity

Commission is exchange/account-derived. Spread and executable VWAP are event-derived. Slippage, impact, fill ratio, latency, and capacity are empirically calibrated by symbol, side, quantity, depth, volatility, flow, movement speed, signal age, time context, and order type. Missing or stale cost components force rejection.

Capacity is the greatest size for which the conservative economic and stressed-exit gates pass; it is not the exchange maximum.

## Selection and approval

Thresholds, rung spacing, progress/holding limits, reversal levels, hot-set size, and economic gates are selected inside nested chronological validation. A value performing best in one backtest is not approved. Every calibrated value records data range, dataset/feature/model versions, calibration/validation method, confidence interval, selection objective, stress results, and approval status.

## Stop rule

The project must stop at Gate 3 if no executable edge survives conservative costs and stress. The ladder enters production only if it adds defensible value over the best simpler baseline. Otherwise the simpler strategy is selected or the system remains non-trading.

No market dataset, simulator result, paper/shadow/testnet record, or controlled live observation has been supplied. Live trading is therefore blocked.
