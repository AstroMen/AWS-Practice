#!/usr/bin/env python3
"""Summarize ELB target health JSON (from aws elbv2 describe-target-health)."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def summarize(payload: dict[str, Any]) -> dict[str, Any]:
    descriptions = payload.get("TargetHealthDescriptions", [])
    state_counter: Counter[str] = Counter()
    reason_counter: Counter[str] = Counter()
    rows: list[dict[str, Any]] = []

    for item in descriptions:
        target = item.get("Target", {})
        health = item.get("TargetHealth", {})
        state = str(health.get("State", "unknown"))
        reason = str(health.get("Reason", "-"))
        state_counter[state] += 1
        reason_counter[reason] += 1
        rows.append(
            {
                "id": target.get("Id", ""),
                "port": target.get("Port", ""),
                "state": state,
                "reason": reason,
                "description": health.get("Description", ""),
            }
        )

    return {
        "total_targets": len(descriptions),
        "states": dict(state_counter),
        "reasons": dict(reason_counter),
        "targets": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize ELB target health JSON from aws elbv2 describe-target-health."
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to target health JSON")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = summarize(payload)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print(f"Total targets: {report['total_targets']}")
    print("States:")
    for state, count in sorted(report["states"].items()):
        print(f"- {state}: {count}")

    print("\nReasons:")
    for reason, count in sorted(report["reasons"].items()):
        print(f"- {reason}: {count}")

    print("\nTargets:")
    for target in report["targets"]:
        print(
            f"- {target['id']}:{target['port']} state={target['state']} "
            f"reason={target['reason']} desc={target['description']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
