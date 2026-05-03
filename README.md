# AWS Security Posture Scanner

Automated security scanner that detects 
misconfigurations in AWS environments and 
generates a professional HTML report.

## What It Detects

| Check | Severity | Service |
|-------|----------|---------|
| Public S3 buckets | CRITICAL | Amazon S3 |
| IAM users without MFA | HIGH | AWS IAM |
| Root account access keys | CRITICAL | AWS IAM |
| Dangerous ports open to internet | CRITICAL | AWS EC2 |

## Tech Stack

Python · Boto3 · AWS IAM · Amazon S3 · AWS EC2

## Setup

```bash
pip install boto3
aws configure
python scanner.py
```

## How It Works

The scanner connects to your AWS account 
via Boto3, runs security checks across 
IAM, S3, and EC2, then generates an HTML 
report with severity scoring.

## Real Finding Detected

During testing, the scanner identified a 
HIGH severity finding in a live AWS 
environment — an IAM admin user with no 
MFA device assigned. Finding was documented 
in FINDINGS.md, remediated, and verified 
by re-running the scanner which returned 
0 findings after the fix.

## Project Structure