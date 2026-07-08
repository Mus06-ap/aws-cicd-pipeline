# AWS CI/CD Pipeline — Containerised Security Scanner on ECS Fargate

Automated deployment pipeline that containerises an AWS security scanner and runs it daily on ECS Fargate using Docker, ECR, Terraform, and EventBridge. Zero manual intervention required.

## Architecture

Code Push to GitHub
|
Docker Build (local)
|
Amazon ECR (image registry)
|
EventBridge Rule (daily 8am UTC)
|
ECS Fargate Task (pulls image, runs scanner)
|
CloudWatch Logs (stores results)


## What This Does

The AWS Security Posture Scanner runs automatically every day at 8am UTC without any manual steps. When triggered it scans the AWS account for misconfigurations across IAM, S3, and EC2, then logs all findings to CloudWatch.

## Infrastructure Deployed

| Resource | Purpose |
|----------|---------|
| Amazon ECR | Stores the Docker image |
| ECS Fargate Cluster | Runs the container serverlessly |
| ECS Task Definition | Defines CPU, memory, and IAM permissions |
| IAM Execution Role | Allows ECS to pull from ECR |
| IAM Task Role | Least-privilege permissions for the scanner |
| CloudWatch Log Group | Stores scan results and logs |
| EventBridge Rule | Triggers the scan daily at 8am UTC |
| Security Group | Outbound only for AWS API calls |

## Tech Stack

Docker, Amazon ECR, Amazon ECS Fargate, Terraform, AWS EventBridge, CloudWatch, IAM, Python, Boto3

## How To Deploy

### Prerequisites
```bash
terraform --version
aws configure
docker --version
```

### Build and Push Docker Image
```bash
docker build -t aws-security-scanner .

aws ecr create-repository --repository-name aws-security-scanner --region ap-southeast-1

aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com

docker tag aws-security-scanner:latest <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/aws-security-scanner:latest

docker push <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/aws-security-scanner:latest
```

### Deploy Infrastructure
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Destroy
```bash
terraform destroy
```

## Security Controls

IAM task role scoped to scanner permissions only. No hardcoded credentials anywhere. Security group allows outbound traffic only. CloudWatch logs retained for 7 days.

## Author

Musab Elfurgi | Cloud Engineering Student
Asia Pacific University (APU) Malaysia
GitHub: github.com/Mus06-ap