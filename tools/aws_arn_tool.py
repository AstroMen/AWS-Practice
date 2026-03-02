#!/usr/bin/env python3
"""Parse and compose AWS ARN strings.

Examples:
  python tools/aws_arn_tool.py parse arn:aws:s3:::my-bucket
  python tools/aws_arn_tool.py build --service lambda --region us-east-1 --account-id 123456789012 --resource function:my-func
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass

ARN_PATTERN = re.compile(
    r"^arn:(?P<partition>aws[a-zA-Z-]*)?:"
    r"(?P<service>[a-z0-9-]+):"
    r"(?P<region>[a-z0-9-]*):"
    r"(?P<account_id>[0-9]{12}|):"
    r"(?P<resource>.+)$"
)


@dataclass
class ArnParts:
    partition: str
    service: str
    region: str
    account_id: str
    resource: str

    @property
    def arn(self) -> str:
        return (
            f"arn:{self.partition}:{self.service}:"
            f"{self.region}:{self.account_id}:{self.resource}"
        )


def parse_arn(value: str) -> ArnParts:
    match = ARN_PATTERN.match(value)
    if not match:
        raise ValueError(f"Invalid ARN format: {value}")

    parts = ArnParts(**match.groupdict())
    if not parts.partition:
        parts.partition = "aws"
    return parts


def build_arn(
    partition: str,
    service: str,
    region: str,
    account_id: str,
    resource: str,
) -> ArnParts:
    candidate = ArnParts(
        partition=partition,
        service=service,
        region=region,
        account_id=account_id,
        resource=resource,
    )
    parse_arn(candidate.arn)
    return candidate


def cmd_parse(args: argparse.Namespace) -> int:
    parts = parse_arn(args.arn)
    if args.json:
        print(json.dumps(asdict(parts), indent=2, ensure_ascii=False))
    else:
        print(f"partition : {parts.partition}")
        print(f"service   : {parts.service}")
        print(f"region    : {parts.region or '(global)'}")
        print(f"account   : {parts.account_id or '(none)'}")
        print(f"resource  : {parts.resource}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    parts = build_arn(
        partition=args.partition,
        service=args.service,
        region=args.region,
        account_id=args.account_id,
        resource=args.resource,
    )
    print(parts.arn)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse or compose AWS ARN values.")
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_parse = sub.add_parser("parse", help="Parse an ARN")
    p_parse.add_argument("arn", help="ARN to parse")
    p_parse.add_argument("--json", action="store_true", help="Output as JSON")
    p_parse.set_defaults(func=cmd_parse)

    p_build = sub.add_parser("build", help="Build an ARN")
    p_build.add_argument("--partition", default="aws")
    p_build.add_argument("--service", required=True)
    p_build.add_argument("--region", default="")
    p_build.add_argument("--account-id", default="")
    p_build.add_argument("--resource", required=True)
    p_build.set_defaults(func=cmd_build)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
