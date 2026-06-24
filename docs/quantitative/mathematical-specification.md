# Mathematical specification

**Version:** 0.1.0  
**Status:** no calibrated production values

## Numeric domains

Exchange price is integer ticks `p` with symbol tick size `τ`; quantity is integer steps `q` with step size `σ`. Physical values are `P=pτ` and `Q=qσ`. Fees, notional, PnL, and risk use exact decimal fixed-point values with explicit asset/currency units. Binary float is prohibited at exchange/accounting boundaries and may appear only inside isolated numerical arrays with validated conversion and rounding.

## Model outputs

For decision state `X_t`, direction `d`, and validity horizon `H`, separate models estimate:

- upward continuation, downward continuation, and no-action probabilities;
- target-before-invalidation probability;
- reachable-price distribution and quantiles;
- invalidation distribution;
- maximum favorable/adverse excursion distributions;
- time-to-target and time-to-invalidation distributions;
- exhaustion probability;
- entry/exit VWAP, slippage, fill-ratio, and capacity distributions;
- ordinary-noise, meaningful-reversal, continuation-resumption, and waiting-cost probabilities/values.

A point target is only a summary of a conditional distribution. Censored paths are not relabeled as wins.

## Cost

```text
direct_cost =
    entry_commission
  + expected_exit_commission
  + spread_cost
  + upper_bound(entry_slippage)
  + upper_bound(exit_slippage)
  + expected_market_impact
  + funding_allowance
  + latency_allowance
  + model_error_allowance
```

Commission and current funding inputs are exchange/account-derived. Slippage, impact, latency, fill ratio, noise, and model error are empirically calibrated and versioned.

For an app-managed reversal exit:

```text
required_profitable_distance =
    direct_cost
  + noise_reversal_distance
  + customer_required_net_profit
  + risk_safety_reserve
```

## Expected value

For net reward `G>=0`, net loss `L>=0`, and success probability `p`:

```text
EV = p*G - (1-p)*L
break_even_probability = L/(G+L)
```

The denominator must be positive. Approval requires:

```text
LCB(predicted_success_probability)
  > break_even_probability + validated_probability_safety_margin
```

The confidence method, coverage, and safety margin are selected inside nested chronological validation and predeclared before final testing.

```text
cost_coverage_ratio = conservative_remaining_movement / conservative_total_cost
```

Its acceptance threshold is calibrated and customer-approved; it is not hard-coded.

## Marginal rung

```text
marginal_EV_k =
    p_continue_k * conditional_net_gain_k
  - p_reverse_k * conditional_net_loss_k
  - entry_cost_k
  - eventual_exit_cost_k
  - incremental_tail_risk_k
```

Each rung independently passes a conservative lower-confidence-bound gate. Earlier profit cannot subsidize a negative marginal rung.

## Exit comparison

```text
EV_wait_i = P(noise|X_t)*continuation_value
          - P(reversal|X_t)*delayed_exit_loss
          - expected_cost_of_waiting
EV_exit_i = immediate_realizable_value - immediate_exit_cost
```

Mandatory risk/protection/invalidation/time exits override model preference.

## Position sizing and rounding

```text
q_approved = floor_to_step(min(
  q_risk, q_liquidity, q_campaign, q_portfolio,
  q_exchange_filter, q_leverage_bracket
))
```

Rounding may never increase any risk/exposure limit. Current minimum/maximum quantity and notional filters must pass after rounding.

## Conservation

```text
sum(signed_remaining_virtual_lot_quantity) = reconciled_exchange_position
sum(reserved_exit_quantity + active_exit_quantity) <= reducible_position
```

Any tolerance is derived only from current exchange quantity-step/account representation. Duplicate/reordered events are idempotent and may not silently alter final state.

## Request budget

For each scope/window `j`, entry is admissible only when:

```text
remaining_j - pessimistic_entry_workflow_reservation_j
  >= derived_emergency_plan_j(current_account_state)
```

The emergency plan covers cancel, unknown-order query, protection repair, close, final confirmation, and reconciliation. No percentage reserve is allowed.

## Validation

Required: nested chronological validation, purging/embargo, probability calibration, dependence-aware bootstrap intervals, multiple-testing tracking, deflated statistics, overfitting diagnostics, regime separation, cost/latency/capacity stress, and an untouched final test set. No production threshold is supplied by this document.
