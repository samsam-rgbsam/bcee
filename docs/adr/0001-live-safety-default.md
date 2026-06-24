# ADR-0001: Default to LIVE_LOCKED and NO_TRADE

- Status: Accepted for architecture
- Date: 2026-06-23

All startup paths default to non-live operation. `run_live.bat` may establish production observation only in `LIVE_LOCKED`; it may not arm trading. Missing, stale, unsupported, unreconciled, unprotected, economically marginal, or operationally uncertain state means `NO_TRADE`.

No convenience override is allowed. Material configuration change disarms live entries. This increases operational friction to prevent accidental exposure and invalid assumptions.
