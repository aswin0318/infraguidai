# ───────────────────────────────────────────────────────────────────────────
# CS-02 Kubernetes Log Intelligence Agent — event-triggered Lambda.
# Fluent Bit ships pod logs to the CloudWatch log group below; a subscription
# filter invokes this Lambda ONLY on lines matching the anomaly pattern.
# ───────────────────────────────────────────────────────────────────────────

# Log group Fluent Bit writes pod logs into.
resource "aws_cloudwatch_log_group" "pod_logs" {
  name              = var.log_group_name
  retention_in_days = var.log_retention_days

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-pod-logs"
  })
}

# Security group for the VPC-attached Lambda (egress only).
resource "aws_security_group" "lambda" {
  name_prefix = "${var.project}-${var.environment}-logintel-"
  description = "Log Intelligence Lambda - egress only"
  vpc_id      = var.vpc_id

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.project}-${var.environment}-logintel-sg" })

  lifecycle {
    create_before_destroy = true
  }
}

# Execution role
resource "aws_iam_role" "lambda" {
  name = "${var.project}-${var.environment}-logintel-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

# VPC ENI management + base logging for the function's own logs.
resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "lambda" {
  name = "logintel-permissions"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "Bedrock"
        Effect   = "Allow"
        Action   = ["bedrock:InvokeModel"]
        Resource = ["arn:aws:bedrock:*::foundation-model/*"]
      },
      {
        Sid      = "PublishAlerts"
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = var.sns_topic_arn
      },
      {
        Sid      = "ReadLogs"
        Effect   = "Allow"
        Action   = ["logs:FilterLogEvents", "logs:GetLogEvents", "logs:DescribeLogStreams"]
        Resource = "${aws_cloudwatch_log_group.pod_logs.arn}:*"
      },
      {
        Sid      = "DescribeCluster"
        Effect   = "Allow"
        Action   = ["eks:DescribeCluster"]
        Resource = "*"
      },
      {
        Sid      = "ReadSecret"
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = var.secret_arn
      },
      {
        Sid      = "KmsDecrypt"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey"]
        Resource = var.kms_key_arn
      }
    ]
  })
}

# Package the Lambda source at apply time. The handler relies only on the
# Lambda runtime's bundled boto3 + stdlib (urllib), so no pip install is needed.
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = var.lambda_source_dir
  output_path = "${path.module}/build/log-intel-lambda.zip"
}

resource "aws_lambda_function" "this" {
  function_name    = "${var.project}-${var.environment}-log-intel"
  role             = aws_iam_role.lambda.arn
  runtime          = var.lambda_runtime
  handler          = "handler.lambda_handler"
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  timeout          = 60
  memory_size      = 256

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      SNS_TOPIC_ARN     = var.sns_topic_arn
      BEDROCK_MODEL_ID  = var.bedrock_model_id
      LOG_GROUP_NAME    = var.log_group_name
      EKS_CLUSTER_NAME  = var.eks_cluster_name
      ARGOCD_SECRET_ARN = var.secret_arn
      ENABLE_ARGOCD     = var.enable_argocd_correlation ? "true" : "false"
    }
  }

  tags = var.tags
}

# Allow CloudWatch Logs to invoke the function.
resource "aws_lambda_permission" "logs" {
  statement_id  = "AllowCloudWatchLogsInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "logs.${var.aws_region}.amazonaws.com"
  source_arn    = "${aws_cloudwatch_log_group.pod_logs.arn}:*"
}

# Subscription filter — invokes the Lambda only on anomaly lines.
resource "aws_cloudwatch_log_subscription_filter" "anomalies" {
  name            = "${var.project}-${var.environment}-anomaly-filter"
  log_group_name  = aws_cloudwatch_log_group.pod_logs.name
  filter_pattern  = var.anomaly_filter_pattern
  destination_arn = aws_lambda_function.this.arn

  depends_on = [aws_lambda_permission.logs]
}

# EKS access entry — read-only group the Lambda role maps to (for optional
# live pod/event lookups). RBAC binding for this group is shipped via ArgoCD.
resource "aws_eks_access_entry" "lambda" {
  count             = var.eks_access_entry ? 1 : 0
  cluster_name      = var.eks_cluster_name
  principal_arn     = aws_iam_role.lambda.arn
  kubernetes_groups = ["log-intel-readers"]
  type              = "STANDARD"
}
