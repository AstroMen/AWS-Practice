#!/usr/bin/env python3
"""Generate lightweight AWS CLI playbooks for common services."""

from __future__ import annotations

import argparse

PLAYBOOKS = {
    "s3": [
        "aws s3 ls",
        "aws s3 mb s3://<bucket-name> --region <region>",
        "aws s3 cp <local-file> s3://<bucket-name>/<key>",
        "aws s3 sync <local-dir> s3://<bucket-name>/<prefix>/",
    ],
    "ec2": [
        "aws ec2 describe-instances --region <region>",
        "aws ec2 start-instances --instance-ids <i-xxxx> --region <region>",
        "aws ec2 stop-instances --instance-ids <i-xxxx> --region <region>",
        "aws ec2 describe-security-groups --region <region>",
    ],
    "dynamodb": [
        "aws dynamodb list-tables --region <region>",
        "aws dynamodb describe-table --table-name <table> --region <region>",
        "aws dynamodb scan --table-name <table> --limit 10 --region <region>",
    ],
    "elbv2": [
        "aws elbv2 describe-load-balancers --region <region>",
        "aws elbv2 describe-target-groups --region <region>",
        "aws elbv2 describe-target-health --target-group-arn <tg-arn> --region <region>",
    ],
    "cloudwatch": [
        "aws cloudwatch list-metrics --namespace AWS/EC2 --region <region>",
        "aws logs describe-log-groups --region <region>",
        "aws logs tail <log-group-name> --since 1h --follow --region <region>",
    ],
    "sqs": [
        "aws sqs list-queues --region <region>",
        "aws sqs send-message --queue-url <queue-url> --message-body '{\"ok\":true}' --region <region>",
        "aws sqs receive-message --queue-url <queue-url> --max-number-of-messages 5 --region <region>",
    ],
    "iam": [
        "aws iam get-user",
        "aws iam list-roles",
        "aws iam list-attached-role-policies --role-name <role-name>",
    ],
    "lambda": [
        "aws lambda list-functions --region <region>",
        "aws lambda invoke --function-name <function-name> --payload '{}' response.json --region <region>",
        "aws lambda get-function-configuration --function-name <function-name> --region <region>",
    ],
}


def apply_context(command: str, region: str, profile: str) -> str:
    rendered = command.replace("<region>", region)
    if profile:
        rendered += f" --profile {profile}"
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AWS CLI command playbooks.")
    parser.add_argument(
        "--service",
        choices=["all", *PLAYBOOKS.keys()],
        default="all",
        help="Service to print commands for",
    )
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--profile", default="")
    args = parser.parse_args()

    services = PLAYBOOKS.keys() if args.service == "all" else [args.service]

    for svc in services:
        print(f"## {svc}")
        for raw in PLAYBOOKS[svc]:
            print(f"- {apply_context(raw, args.region, args.profile)}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
