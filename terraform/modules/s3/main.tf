# Fresh S3 buckets created by Terraform.
#   documents       — application document storage (upload + ingestion source)
#   knowledge-base  — RAG knowledge base source documents
#   lambda-artifacts — deployment zips for the log-intel Lambda
locals {
  buckets = {
    documents        = "${var.project}-${var.environment}-documents-${var.aws_account_id}"
    knowledge_base   = "${var.project}-${var.environment}-knowledge-base-${var.aws_account_id}"
    lambda_artifacts = "${var.project}-${var.environment}-lambda-artifacts-${var.aws_account_id}"
  }
}

resource "aws_s3_bucket" "this" {
  for_each = local.buckets

  bucket = each.value

  tags = merge(var.tags, {
    Name = each.value
  })
}

resource "aws_s3_bucket_versioning" "this" {
  for_each = aws_s3_bucket.this
  bucket   = each.value.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  for_each = aws_s3_bucket.this
  bucket   = each.value.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  for_each = aws_s3_bucket.this
  bucket   = each.value.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
