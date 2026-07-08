# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "security-scanner-cluster"
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "scanner" {
  name              = "/ecs/security-scanner"
  retention_in_days = 7
}

# ECS Task Definition
resource "aws_ecs_task_definition" "scanner" {
  family                   = "security-scanner"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "security-scanner"
      image     = var.ecr_image_uri
      essential = true

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/security-scanner"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

#  get default VPC
data "aws_vpc" "default" {
  default = true
}

#  get default subnets
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Security Group for ECS task
resource "aws_security_group" "ecs_task" {
  name        = "security-scanner-sg"
  description = "Security group for security scanner ECS task"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound for AWS API calls"
  }
}

#  run scanner daily
resource "aws_cloudwatch_event_rule" "daily_scan" {
  name                = "daily-security-scan"
  description         = "Runs the security scanner every day at 8am UTC"
  schedule_expression = "cron(0 8 * * ? *)"
}

# EventBridge target 
resource "aws_cloudwatch_event_target" "scanner" {
  rule      = aws_cloudwatch_event_rule.daily_scan.name
  target_id = "SecurityScannerTask"
  arn       = aws_ecs_cluster.main.arn
  role_arn  = aws_iam_role.ecs_task_execution_role.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.scanner.arn
    task_count          = 1
    launch_type         = "FARGATE"

    network_configuration {
      subnets          = data.aws_subnets.default.ids
      security_groups  = [aws_security_group.ecs_task.id]
      assign_public_ip = true
    }
  }
}