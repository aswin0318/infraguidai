variable "project" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "aws_account_id" {
  description = "AWS account ID (used to keep bucket names globally unique)"
  type        = string
}

variable "kms_key_arn" {
  description = "KMS key ARN for bucket encryption"
  type        = string
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
