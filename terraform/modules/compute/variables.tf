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

variable "public_subnet_ids" {
  description = "Public subnet IDs for ALB"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for ASG"
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "Security group ID for ALB"
  type        = string
}

variable "ec2_security_group_id" {
  description = "Security group ID for EC2"
  type        = string
}

variable "instance_profile_name" {
  description = "IAM instance profile name for EC2"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the backend application"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "secret_name" {
  description = "Secrets Manager secret name"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for HTTPS"
  type        = string
}

variable "min_size" {
  description = "ASG minimum size"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "ASG maximum size"
  type        = number
  default     = 2
}

variable "desired_capacity" {
  description = "ASG desired capacity"
  type        = number
  default     = 1
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
