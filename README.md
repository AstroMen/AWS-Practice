# AWS-Practice

## AWS Common Services Command
AWS_Common_Services_Cheatsheet.md

## AWS Lambda demo
Code: lambda_handler.py  
Scenario description: lambda_demo.md


## Small helper tools

This repo now includes a few local helper scripts under `tools/` to make Lambda practice easier:

1. `tools/list_lambda_handlers.py`  
   Parse `lambda_handler.py` and list Lambda-style handlers (`event, context`) with line number + docstring.

   ```bash
   python tools/list_lambda_handlers.py
   python tools/list_lambda_handlers.py --json
   ```

2. `tools/gen_lambda_create_commands.py`  
   Auto-generate `aws lambda create-function` commands for all discovered handlers, with cleaner function names (drops `demo1_` style prefixes), so you can copy/paste and tweak quickly.

   ```bash
   python tools/gen_lambda_create_commands.py --role-arn arn:aws:iam::123456789012:role/lambda-role
   python tools/gen_lambda_create_commands.py --prefix demo- --runtime python3.11 --zip build/function.zip
   ```


3. `tools/audit_lambda_demos.py`  
   Run static checks on the demo file and quickly find:
   - placeholder config values (e.g., `YOUR_*`, `Your*`)
   - undefined helper calls (e.g., `process_data`, `store_data`)
   - deprecated import pattern (`from sklearn.externals import joblib`)

   ```bash
   python tools/audit_lambda_demos.py
   python tools/audit_lambda_demos.py --json
   ```

## AWS lightweight utils (multi-service)

Besides Lambda-specific helpers, there are now lightweight utilities for common AWS services:

1. `tools/aws_cli_playbooks.py`  
   Print ready-to-edit AWS CLI playbooks for S3 / EC2 / DynamoDB / CloudWatch / SQS / IAM / Lambda.

   ```bash
   python tools/aws_cli_playbooks.py --service all --region ap-southeast-1
   python tools/aws_cli_playbooks.py --service s3 --region us-west-2 --profile dev
   ```

2. `tools/aws_arn_tool.py`  
   Parse and build AWS ARN values quickly (useful across all services).

   ```bash
   python tools/aws_arn_tool.py parse arn:aws:lambda:us-east-1:123456789012:function:my-func
   python tools/aws_arn_tool.py build --service s3 --resource my-bucket
   ```


3. `tools/s3_inventory_summary.py`  
   Summarize `aws s3api list-objects-v2` JSON output: object count, total size, common extensions, and largest objects.

   ```bash
   aws s3api list-objects-v2 --bucket <bucket> --output json > s3-list.json
   python tools/s3_inventory_summary.py --input s3-list.json --top 10
   ```

4. `tools/elb_target_health_report.py`  
   Summarize `aws elbv2 describe-target-health` JSON output: state distribution, reasons, and per-target details.

   ```bash
   aws elbv2 describe-target-health --target-group-arn <tg-arn> --output json > elb-health.json
   python tools/elb_target_health_report.py --input elb-health.json
   ```

