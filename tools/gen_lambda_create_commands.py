#!/usr/bin/env python3
"""Generate aws lambda create-function commands from discovered handlers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from list_lambda_handlers import extract_handlers


def to_kebab_case(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def normalize_function_name(name: str) -> str:
    """Drop leading demo index prefixes like demo1_ to avoid redundant names."""
    return re.sub(r"^demo\d+_", "", name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate create-function commands for handlers in a Python module."
    )
    parser.add_argument("--file", default="lambda_handler.py", type=Path)
    parser.add_argument("--runtime", default="python3.12")
    parser.add_argument("--role-arn", default="<YOUR_EXECUTION_ROLE_ARN>")
    parser.add_argument("--zip", default="function.zip")
    parser.add_argument("--prefix", default="")
    args = parser.parse_args()

    handlers = extract_handlers(args.file)
    if not handlers:
        print(f"No handlers found in {args.file}")
        return 0

    module = args.file.stem
    for item in handlers:
        normalized = normalize_function_name(item["name"])
        function_name = f"{args.prefix}{to_kebab_case(normalized)}"
        cmd = (
            "aws lambda create-function "
            f"--function-name {function_name} "
            f"--runtime {args.runtime} "
            f"--role {args.role_arn} "
            f"--handler {module}.{item['name']} "
            f"--zip-file fileb://{args.zip}"
        )
        print(cmd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
