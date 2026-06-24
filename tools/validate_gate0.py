from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    ".python-version",
    "pyproject.toml",
    "release_readiness.json",
    "docs/binance/api-compatibility-matrix.md",
    "docs/requirements/product-requirements.md",
    "docs/quantitative/mathematical-specification.md",
    "docs/economics/economic-feasibility-specification.md",
    "docs/risk/customer-risk-policy.schema.json",
    "docs/data/data-requirements.md",
    "docs/operations/windows-python-compatibility-matrix.md",
    "docs/licensing/third-party-licensing-report.md",
    "docs/customer/unresolved-customer-inputs.md",
    "docs/reviews/gate-0-review.md",
)
REQUIRED_CHECKS = {
    "python_compatibility", "windows_compatibility", "dependency_lock",
    "dependency_security", "licensing", "binance_api_compatibility",
    "unit_tests", "property_tests", "contract_tests", "integration_tests",
    "fault_tests", "windows_tests", "request_budget_tests",
    "account_configuration", "customer_risk_policy", "reconciliation",
    "model_approval", "baseline_comparison", "paper_validation",
    "shadow_validation", "testnet_validation", "live_minimum_size_validation",
    "compliance_acknowledgement",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_key(node: Any, key: str) -> bool:
    if isinstance(node, dict):
        return key in node or any(find_key(value, key) for value in node.values())
    if isinstance(node, list):
        return any(find_key(value, key) for value in node)
    return False


def validate() -> list[str]:
    failures: list[str] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty required artifact: {relative}")

    readiness = load_json(ROOT / "release_readiness.json")
    live = readiness.get("live_trading", {})
    if live.get("state") != "LOCKED" or live.get("orders_permitted") is not False:
        failures.append("live trading must remain locked and orders forbidden")
    if readiness.get("gate_decisions", {}).get("gate_0", {}).get("status") != "REJECTED":
        failures.append("Gate 0 must remain rejected while blockers exist")
    checks = set(readiness.get("checks", {}))
    if checks != REQUIRED_CHECKS:
        failures.append(f"release check set mismatch; missing={sorted(REQUIRED_CHECKS-checks)} extra={sorted(checks-REQUIRED_CHECKS)}")
    if any(item.get("status") == "PASS" for item in readiness.get("checks", {}).values()):
        failures.append("unexecuted release checks may not be marked PASS")

    schema = load_json(ROOT / "docs/risk/customer-risk-policy.schema.json")
    if find_key(schema, "default"):
        failures.append("customer policy schema must not contain defaults")
    if schema.get("properties", {}).get("production_automation_authorization", {}).get("const") is not True:
        failures.append("production automation authorization must require explicit true")
    if (ROOT / ".python-version").read_text(encoding="utf-8").strip() != "3.14.6":
        failures.append("Python candidate must match the compatibility decision")
    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("Gate 0 validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Gate 0 validation: PASS (artifact/safety-lock checks only; not Windows, Binance, or trading validation)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
