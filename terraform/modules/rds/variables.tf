variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "isolated_subnet_ids" {
  description = "Isolated subnet IDs for DB subnet group"
  type        = list(string)
}

variable "rds_security_group_id" {
  description = "Security group ID for RDS"
  type        = string
}

variable "kms_key_arn" {
  description = "KMS key ARN for storage encryption"
  type        = string
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "multi_az" {
  description = "Enable Multi-AZ deployment"
  type        = bool
  default     = false
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "infraguidai"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "infraguidai_admin"
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
