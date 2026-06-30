# General
variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name used for resource naming"
  type        = string
  default     = "infraguidai"
}

variable "environment" {
  description = "Environment name (prod, staging, dev)"
  type        = string
  default     = "prod"
}

# Networking
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# EKS
variable "eks_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
  default     = "1.30"
}

variable "node_instance_type" {
  description = "EC2 instance type for EKS worker nodes"
  type        = string
  default     = "t3.large"
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

variable "app_namespace" {
  description = "Kubernetes namespace the application pods run in"
  type        = string
  default     = "infraguid"
}

# ECR
variable "ecr_namespace" {
  description = "ECR repository namespace prefix"
  type        = string
  default     = "infragui"
}

# Database
variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 20
}

variable "rds_multi_az" {
  description = "Enable Multi-AZ for RDS"
  type        = bool
  default     = false
}

variable "rds_db_name" {
  description = "RDS database name"
  type        = string
  default     = "infraguidai"
}

variable "rds_username" {
  description = "RDS master username"
  type        = string
  default     = "infraguidai_admin"
}

# Domain & DNS
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
}

variable "hosted_zone_id" {
  description = "Route 53 hosted zone ID"
  type        = string
}

# AWS Account
variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

# Log Intelligence Agent
variable "alert_email" {
  description = "Admin email subscribed to the SNS alerts topic"
  type        = string
  default     = ""
}

variable "bedrock_logintel_model_id" {
  description = "Bedrock Claude model id used by the log-intel Lambda for summarization"
  type        = string
  default     = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
}

variable "enable_argocd_correlation" {
  description = "Enable best-effort ArgoCD deployment correlation in the log-intel Lambda"
  type        = bool
  default     = false
}
