# Binance USD-M Futures API compatibility matrix

**Application:** 0.0.0-gate0  
**Official-document verification date:** 2026-06-23  
**Runtime verification:** none  
**Status:** partial official-document verification; execution blocked

Only current official Binance developer documentation was used for exchange assertions.

## Roots and transport

| Surface | Current documented fact | Required handling |
|---|---|---|
| Production REST | `https://fapi.binance.com` | broker-owned, versioned configuration |
| Testnet REST | `https://demo-fapi.binance.com` | separate credentials/data/security boundary |
| Market WebSocket | `wss://fstream.binance.com` with `/public`, `/market`, `/private` route forms and raw/combined streams | route is part of the stream contract; unrouted connections receive public-route streams only |
| Testnet WebSocket | `wss://demo-fstream.binance.com` | routed parity requires contract testing |
| Connection lifetime | 24 hours | overlap replacement: connect, subscribe, confirm, synchronize, switch, close old |
| Ping/pong | ping every 3 minutes; disconnect if no pong within 10 minutes; copy ping payload | protocol health and monotonic deadlines |
| Market control/incoming limit | 10 messages/second including control/ping/pong | centrally budgeted batched/deduplicated subscription queue |
| Streams per connection | 1024 | shard by failure domain/workload, not merely maximum packing |
| User listen key | valid 60 minutes; start/keepalive weight 1 | broker renewal, recreate on invalid key, reconcile on replacement |

## Core REST registry

| Purpose | Method/path | Documented cost | Critical behavior |
|---|---|---|---|
| Server time | `GET /fapi/v1/time` | weight 1 | measure offset/RTT/uncertainty; no arbitrary timing constant |
| Exchange info | `GET /fapi/v1/exchangeInfo` | weight 1 | dynamic rates, symbols/status, trigger protection, order types/TIF, filters; precision fields are not tick/step |
| Depth snapshot | `GET /fapi/v1/depth` | weight depends on limit | last update ID, exchange times, absolute quantities; RPI orders excluded |
| New ordinary order | `POST /fapi/v1/order` | IP weight 0; order count 1 on documented 10-second and 1-minute windows | deterministic client ID; IOC; position/reduce/hedge restrictions |
| Test order | `POST /fapi/v1/order/test` | load current endpoint cost | validates without matching-engine submission |
| Cancel ordinary | `DELETE /fapi/v1/order` | weight 1 | by order or client order ID; cancellation requires confirmation |
| Query ordinary | `GET /fapi/v1/order` | weight 1 | old canceled/expired no-fill and old orders have retention limits |
| Open ordinary | `GET /fapi/v1/openOrders` | 1 scoped, 40 unscoped | emergency plan accounts for scoped/unscoped costs |
| New algo | `POST /fapi/v1/algoOrder` | documented IP weight 0; order-count effect unresolved | conditional STOP/TP/trailing; client algo ID; mode/reduce/close restrictions |
| Cancel/query algo | `DELETE/GET /fapi/v1/algoOrder` | weight 1 | track client/exchange algo ID, resulting order, retention, final confirmation |
| Open algos | `GET /fapi/v1/openAlgoOrders` | 1 scoped, 40 unscoped | reconciliation cost differs by scope |
| Balance V3 | `GET /fapi/v3/balance` | weight 5 | asset and available balances |
| Account V3 | `GET /fapi/v3/account` | weight 5 | single-/multi-assets semantics and mode-dependent positions |
| Commission | `GET /fapi/v1/commissionRate` | weight 20 | maker, taker, RPI commission per symbol |
| Account config | `GET /fapi/v1/accountConfig` | weight 5 | `canTrade`, position mode, multi-assets mode, fee tier |
| Symbol config | `GET /fapi/v1/symbolConfig` | weight 5 | margin type, leverage, maximum notional |
| Account order rates | `GET /fapi/v1/rateLimit/order` | weight 1 | separate order windows; never collapse scopes/windows |
| Leverage brackets | `GET /fapi/v1/leverageBracket` | weight 1 | account/symbol bracket floors/caps, max leverage, maintenance ratio |
| Quantitative rules | `GET /fapi/v1/apiTradingStatus` | 1 scoped, 10 unscoped | locked indicator blocks entry; planned recovery is observed state |

Position mode, margin mode, multi-assets mode, position information, account trades/fills, funding/income history, batch/amend/countdown endpoints, and all enabled stream schemas require endpoint-by-endpoint contract entries before implementation. Their omission is blocking, not permission to infer behavior.

## Current enums and filters

Official common definitions currently include contract states `PENDING_TRADING`, `TRADING`, `PRE_DELIVERING`, `DELIVERING`, `DELIVERED`, `PRE_SETTLE`, `SETTLING`, `CLOSE`; ordinary statuses `NEW`, `PARTIALLY_FILLED`, `FILLED`, `CANCELED`, `REJECTED`, `EXPIRED`, `EXPIRED_IN_MATCH`; order types LIMIT/MARKET/STOP/STOP_MARKET/TAKE_PROFIT/TAKE_PROFIT_MARKET/TRAILING_STOP_MARKET; TIF values GTC/IOC/FOK/GTX/GTD/RPI; STP modes; and price, lot, market-lot, minimum-notional, percent-price, ordinary-order-count, and algo-order-count filters.

Unknown enum/filter values must be retained raw, quarantined, and fail closed. Runtime uses filter tick/step, not display precision.

## Local order book

Required official algorithm: buffer depth updates before snapshot; obtain a broker-budgeted REST snapshot; discard obsolete events; require the first event to cover the snapshot update ID; require each subsequent `pu` to equal the prior `u`; treat quantities as absolute; remove zero levels; invalidate/reinitialize on any gap; block entries while invalid. Recovery priority is open positions, armed entries, hot set, scanner-only, without consuming emergency reserve.

## Ordinary and algo lifecycles

User order updates expose NEW/CANCELED/CALCULATED/EXPIRED/TRADE/AMENDMENT execution types, ordinary statuses, and expiry reasons including STP, IOC remainder, liquidation, delisting, trigger-related expiry, and incomplete market fill.

Algo events expose `NEW`, `CANCELED`, `TRIGGERING`, `TRIGGERED`, `FINISHED`, `REJECTED`, and `EXPIRED`, plus client/exchange algo IDs and resulting matching-engine order fields. A distinct `CONDITIONAL_ORDER_TRIGGER_REJECT` event proves that accepted conditional intent can fail at trigger. Algo acceptance is therefore not confirmed protection.

## Unknown execution result

HTTP 503 unknown status, `-1006`, `-1007`, timeout, disconnect, malformed/unexpected response, missing acknowledgement, or any possibly-executed command maps to `STATUS_UNKNOWN`. Do not retry blindly. Search deterministic client ID, inspect user events, query positions/orders when budget permits, reconcile, and retry only after proving non-execution with a new attempt ID under the original business command.

## Rate/error behavior

`exchangeInfo` provides public definitions; response headers expose used request weight and order counts by interval, but unsuccessful orders may omit order-count headers. HTTP 429 is rate limiting; repeated violations may produce 418 ban. During ban do not probe repeatedly. Missing counters retain pessimistic reservations. `-1008` overload may exempt documented reduce-only/close-position risk-reduction requests but never waives local validation/reconciliation.

## Blocking conflicts and unknowns

1. Ordinary test-order documentation gives trailing callback 0.1–5 while new algo-order documentation gives 0.1–10 for its surface. Exchange trailing remains disabled pending official clarification and contract tests.
2. New algo order documents zero IP weight, but complete account order-count effects/windows are not established. Reserve pessimistically.
3. Testnet route parity and authenticated schemas have not been executed.
4. Documentation examples are not runtime/account truth; limits and filters are dynamically loaded and reconciled.
5. Error messages may vary even where codes are universal; logic cannot parse English messages as the primary contract.

## Official pages

- https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info
- https://developers.binance.com/docs/derivatives/usds-margined-futures/common-definition
- https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams
- https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/How-to-manage-a-local-order-book-correctly
- https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information
- https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Order
- https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Algo-Order
- https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Order-Update
- https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Conditional-Order-Trigger-Reject
- https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Algo-Order-Update
- https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V3
- https://developers.binance.com/docs/derivatives/usds-margined-futures/error-code

## Decision

The matrix establishes fail-closed design constraints but does not approve testnet or production execution. Authenticated behavior, omitted surfaces, contract tests, and conflicts remain blocking.
