variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
  default     = "943339979898"
}

variable "ecr_image_uri" {
  description = "ECR image URI"
  type        = string
  default     = "943339979898.dkr.ecr.ap-southeast-1.amazonaws.com/aws-security-scanner:latest"
}

variable "task_cpu" {
  description = "CPU units for ECS task"
  type        = string
  default     = "256"
}

variable "task_memory" {
  description = "Memory for ECS task in MB"
  type        = string
  default     = "512"
}