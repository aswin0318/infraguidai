# Application URL
output "app_url" {
  description = "Application URL"
  value       = "https://${var.domain_name}"
}

# EKS
output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS API server endpoint"
  value       = module.eks.cluster_endpoint
}

output "update_kubeconfig_command" {
  description = "Run this to configure kubectl for the cluster"
  value       = "aws eks update-kubeconfig --name ${module.eks.cluster_name} --region ${var.aws_region}"
}

output "oidc_provider_arn" {
  description = "EKS OIDC provider ARN"
  value       = module.eks.oidc_provider_arn
}

# ECR
output "ecr_registry_url" {
  description = "ECR registry base URL"
  value       = module.ecr.registry_url
}

output "ecr_repository_urls" {
  description = "Map of service => ECR repository URL"
  value       = module.ecr.repository_urls
}

# IRSA role ARNs (annotate the matching Kubernetes service accounts with these)
output "irsa_app_role_arn" {
  description = "IRSA role ARN for application pods"
  value       = module.irsa.app_role_arn
}

output "irsa_alb_controller_role_arn" {
  description = "IRSA role ARN for the AWS Load Balancer Controller"
  value       = module.irsa.alb_controller_role_arn
}

output "irsa_external_secrets_role_arn" {
  description = "IRSA role ARN for External Secrets"
  value       = module.irsa.external_secrets_role_arn
}

output "irsa_fluent_bit_role_arn" {
  description = "IRSA role ARN for Fluent Bit"
  value       = module.irsa.fluent_bit_role_arn
}

# RDS
output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.endpoint
}

# Cognito
output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = module.cognito.user_pool_id
}

output "cognito_app_client_id" {
  description = "Cognito App Client ID"
  value       = module.cognito.app_client_id
}

# Secrets Manager
output "secret_name" {
  description = "Secrets Manager secret name"
  value       = module.secrets.secret_name
}

# S3 buckets
output "documents_bucket_name" {
  description = "Documents S3 bucket name"
  value       = module.s3.documents_bucket_name
}

output "knowledge_base_bucket_name" {
  description = "Knowledge base S3 bucket name"
  value       = module.s3.knowledge_base_bucket_name
}

output "lambda_artifacts_bucket_name" {
  description = "Lambda artifacts S3 bucket name"
  value       = module.s3.lambda_artifacts_bucket_name
}

# ACM certificate (used by the ALB Ingress)
output "acm_certificate_arn" {
  description = "Validated ACM certificate ARN for the ALB Ingress"
  value       = module.dns.acm_certificate_validated_arn
}

# SNS
output "alerts_topic_arn" {
  description = "SNS alerts topic ARN"
  value       = module.sns.topic_arn
}

# Log Intelligence Lambda
output "log_intel_function_name" {
  description = "Log Intelligence Lambda function name"
  value       = module.log_intel_lambda.function_name
}

# VPC
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}
