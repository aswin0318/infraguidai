# IRSA — IAM Roles for Service Accounts, federated through the cluster OIDC provider.
# Each role trusts a specific Kubernetes service account (namespace + name).

locals {
  # Service accounts that assume each role.
  app_sa              = "system:serviceaccount:${var.app_namespace}:${var.app_service_account}"
  alb_controller_sa   = "system:serviceaccount:kube-system:aws-load-balancer-controller"
  external_secrets_sa = "system:serviceaccount:external-secrets:external-secrets"
  fluent_bit_sa       = "system:serviceaccount:amazon-cloudwatch:fluent-bit"
}

# Reusable assume-role policy generator for IRSA.
data "aws_iam_policy_document" "assume" {
  for_each = {
    app              = local.app_sa
    alb_controller   = local.alb_controller_sa
    external_secrets = local.external_secrets_sa
    fluent_bit       = local.fluent_bit_sa
  }

  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:sub"
      values   = [each.value]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

# ─────────────────────────── App role ───────────────────────────
resource "aws_iam_role" "app" {
  name               = "${var.project}-${var.environment}-app-irsa"
  assume_role_policy = data.aws_iam_policy_document.assume["app"].json
  tags               = var.tags
}

resource "aws_iam_role_policy" "app" {
  name = "app-permissions"
  role = aws_iam_role.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Bedrock"
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = ["arn:aws:bedrock:*::foundation-model/*"]
      },
      {
        Sid      = "SecretsManager"
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
        Resource = var.secret_arn
      },
      {
        Sid      = "KmsDecrypt"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = var.kms_key_arn
      },
      {
        Sid      = "S3Objects"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
        Resource = ["${var.documents_bucket_arn}/*", "${var.knowledge_base_bucket_arn}/*"]
      },
      {
        Sid      = "S3List"
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = [var.documents_bucket_arn, var.knowledge_base_bucket_arn]
      }
    ]
  })
}

# ───────────────────── AWS Load Balancer Controller role ─────────────────────
resource "aws_iam_role" "alb_controller" {
  name               = "${var.project}-${var.environment}-alb-controller-irsa"
  assume_role_policy = data.aws_iam_policy_document.assume["alb_controller"].json
  tags               = var.tags
}

resource "aws_iam_policy" "alb_controller" {
  name        = "${var.project}-${var.environment}-alb-controller"
  description = "AWS Load Balancer Controller policy"
  policy      = file("${path.module}/policies/alb-controller.json")

  lifecycle {
    ignore_changes = [policy]
  }
}

resource "aws_iam_role_policy_attachment" "alb_controller" {
  role       = aws_iam_role.alb_controller.name
  policy_arn = aws_iam_policy.alb_controller.arn
}

# ───────────────────────── External Secrets role ─────────────────────────
resource "aws_iam_role" "external_secrets" {
  name               = "${var.project}-${var.environment}-external-secrets-irsa"
  assume_role_policy = data.aws_iam_policy_document.assume["external_secrets"].json
  tags               = var.tags
}

resource "aws_iam_role_policy" "external_secrets" {
  name = "read-app-secret"
  role = aws_iam_role.external_secrets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
        Resource = var.secret_arn
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = var.kms_key_arn
      }
    ]
  })
}

# ───────────────────────────── Fluent Bit role ─────────────────────────────
resource "aws_iam_role" "fluent_bit" {
  name               = "${var.project}-${var.environment}-fluent-bit-irsa"
  assume_role_policy = data.aws_iam_policy_document.assume["fluent_bit"].json
  tags               = var.tags
}

resource "aws_iam_role_policy" "fluent_bit" {
  name = "cloudwatch-logs-write"
  role = aws_iam_role.fluent_bit.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutRetentionPolicy"
      ]
      Resource = "arn:aws:logs:*:*:*"
    }]
  })
}
