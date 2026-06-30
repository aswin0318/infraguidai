variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "kms_key_arn" {
  description = "ARN of the KMS key"
  type        = string
}

variable "s3_document_bucket_arn" {
  description = "ARN of the S3 documents bucket"
  type        = string
}

variable "secret_arn" {
  description = "ARN of the Secrets Manager secret"
  type        = string
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
