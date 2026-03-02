#!/usr/bin/env python3
"""List Lambda handlers defined in a Python module."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any


def extract_handlers(file_path: Path) -> list[dict[str, Any]]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    handlers: list[dict[str, Any]] = []

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue

        args = [arg.arg for arg in node.args.args]
        if args[:2] != ["event", "context"]:
            continue

        handlers.append(
            {
                "name": node.name,
                "doc": ast.get_docstring(node) or "",
                "lineno": node.lineno,
            }
        )

    return handlers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract and list Lambda-style handlers (event, context) from a Python file."
    )
    parser.add_argument(
        "--file",
        default="lambda_handler.py",
        type=Path,
        help="Path to module containing Lambda handlers (default: lambda_handler.py)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of a table.",
    )
    args = parser.parse_args()

    handlers = extract_handlers(args.file)

    if args.json:
        print(json.dumps(handlers, indent=2, ensure_ascii=False))
        return 0

    if not handlers:
        print(f"No Lambda-style handlers found in {args.file}.")
        return 0

    print(f"Found {len(handlers)} Lambda-style handlers in {args.file}:\n")
    name_width = max(len(item["name"]) for item in handlers)
    for item in handlers:
        doc = item["doc"].splitlines()[0] if item["doc"] else "-"
        print(f"- {item['name']:<{name_width}}  line {item['lineno']:>3}  {doc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
