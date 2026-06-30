variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for the Lambda ENIs"
  type        = list(string)
}

variable "sns_topic_arn" {
  description = "SNS alerts topic ARN"
  type        = string
}

variable "secret_arn" {
  description = "Secrets Manager secret ARN (holds ArgoCD token when correlation enabled)"
  type        = string
}

variable "kms_key_arn" {
  description = "KMS key ARN"
  type        = string
}

variable "eks_cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "log_group_name" {
  description = "CloudWatch log group Fluent Bit ships pod logs to"
  type        = string
  default     = "/infraguid/prod/pod-logs"
}

variable "log_retention_days" {
  description = "Retention for the pod-logs log group"
  type        = number
  default     = 14
}

variable "anomaly_filter_pattern" {
  description = "CloudWatch Logs filter pattern that triggers the Lambda"
  type        = string
  default     = "?OOMKilled ?CrashLoopBackOff ?ImagePullBackOff ?\"Liveness probe failed\" ?\"Readiness probe failed\""
}

variable "bedrock_model_id" {
  description = "Bedrock Claude model id used for summarization"
  type        = string
}

variable "lambda_source_dir" {
  description = "Path to the Lambda source directory"
  type        = string
}

variable "lambda_runtime" {
  description = "Lambda Python runtime"
  type        = string
  default     = "python3.12"
}

variable "enable_argocd_correlation" {
  description = "Enable best-effort ArgoCD deployment correlation"
  type        = bool
  default     = false
}

variable "eks_access_entry" {
  description = "Create an EKS access entry mapping the Lambda role to a read-only group"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
