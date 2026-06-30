variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "domain_name" {
  description = "Domain name for CloudFront"
  type        = string
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN (must be in us-east-1)"
  type        = string
}

variable "alb_dns_name" {
  description = "ALB DNS name for API origin"
  type        = string
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
}

variable "cognito_user_pool_id" {
  description = "Cognito User Pool ID for config.js"
  type        = string
}

variable "cognito_app_client_id" {
  description = "Cognito App Client ID for config.js"
  type        = string
}

variable "cognito_region" {
  description = "Cognito region for config.js"
  type        = string
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
