#!/usr/bin/env python3
"""Summarize S3 object listing JSON (from aws s3api list-objects-v2)."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def human_size(num: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f}{unit}" if unit != "B" else f"{int(value)}B"
        value /= 1024
    return f"{value:.2f}TB"


def extension_of(key: str) -> str:
    name = key.rsplit("/", maxsplit=1)[-1]
    if "." not in name or name.startswith("."):
        return "(no-ext)"
    return name.rsplit(".", maxsplit=1)[-1].lower()


def summarize(payload: dict[str, Any], top_n: int) -> dict[str, Any]:
    objects = payload.get("Contents", [])
    total_size = sum(int(obj.get("Size", 0)) for obj in objects)
    ext_counter: Counter[str] = Counter()
    largest: list[dict[str, Any]] = []

    for obj in objects:
        key = str(obj.get("Key", ""))
        ext_counter[extension_of(key)] += 1

    largest = sorted(objects, key=lambda x: int(x.get("Size", 0)), reverse=True)[:top_n]

    return {
        "name": payload.get("Name", ""),
        "key_count": int(payload.get("KeyCount", len(objects))),
        "object_count": len(objects),
        "total_size_bytes": total_size,
        "total_size_human": human_size(total_size),
        "top_extensions": ext_counter.most_common(top_n),
        "largest_objects": [
            {"key": item.get("Key", ""), "size": int(item.get("Size", 0))}
            for item in largest
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize an S3 object listing JSON file (aws s3api list-objects-v2 output)."
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to listing JSON")
    parser.add_argument("--top", type=int, default=5, help="Top N for extensions/largest objects")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    report = summarize(payload, top_n=args.top)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print(f"Bucket          : {report['name']}")
    print(f"Objects listed  : {report['object_count']}")
    print(f"KeyCount field  : {report['key_count']}")
    print(f"Total size      : {report['total_size_human']} ({report['total_size_bytes']} bytes)")

    print("\nTop extensions:")
    for ext, count in report["top_extensions"]:
        print(f"- {ext}: {count}")

    print("\nLargest objects:")
    for item in report["largest_objects"]:
        print(f"- {item['key']} ({human_size(item['size'])})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
