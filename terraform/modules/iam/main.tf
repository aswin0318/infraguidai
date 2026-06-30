# EC2 IAM Role — Backend Application
resource "aws_iam_role" "ec2" {
  name = "${var.project}-${var.environment}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

# SSM Managed Policy — Session Manager access (replaces bastion host)
resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Secrets Manager Access
resource "aws_iam_role_policy" "ec2_secrets" {
  name = "secrets-manager-access"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = var.secret_arn
    }]
  })
}

# KMS Decrypt — for Secrets Manager and S3
resource "aws_iam_role_policy" "ec2_kms" {
  name = "kms-decrypt"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "kms:Decrypt",
        "kms:GenerateDataKey",
        "kms:DescribeKey"
      ]
      Resource = var.kms_key_arn
    }]
  })
}

# Bedrock Access — Titan Embeddings + Llama 3.1
resource "aws_iam_role_policy" "ec2_bedrock" {
  name = "bedrock-invoke"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ]
      Resource = [
        "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v2:0",
        "arn:aws:bedrock:*::foundation-model/us.meta.llama3-1-70b-instruct-v1:0",
        "arn:aws:bedrock:*::foundation-model/*"
      ]
    }]
  })
}

# S3 Access — Document bucket (read/write for upload + ingestion)
resource "aws_iam_role_policy" "ec2_s3" {
  name = "s3-document-access"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${var.s3_document_bucket_arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = "s3:ListBucket"
        Resource = var.s3_document_bucket_arn
      }
    ]
  })
}

# CloudWatch Logs — Application logging
resource "aws_iam_role_policy" "ec2_cloudwatch" {
  name = "cloudwatch-logs"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogStreams"
      ]
      Resource = "arn:aws:logs:*:*:*"
    }]
  })
}

# Instance Profile
resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project}-${var.environment}-ec2-profile"
  role = aws_iam_role.ec2.name

  tags = var.tags
}
