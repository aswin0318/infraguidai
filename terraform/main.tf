# Terraform Configuration
terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "infraguidai-tfstate-901607650789"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "infraguidai-tfstate-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

# Provider
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}

# Local Values
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  # Containerized services that get an ECR repository.
  ecr_services = [
    "chat-service",
    "agent-service",
    "rag-service",
    "ingestion-service",
    "frontend",
  ]
}

# ─────────────────────────────── Networking ───────────────────────────────
module "vpc" {
  source = "./modules/vpc"

  project     = var.project
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
  azs         = var.azs
  aws_region  = var.aws_region
  tags        = local.common_tags
}

# ─────────────────────────────── Encryption ───────────────────────────────
module "kms" {
  source = "./modules/kms"

  project        = var.project
  environment    = var.environment
  aws_account_id = var.aws_account_id
  tags           = local.common_tags
}

# ─────────────────────────────── Storage (new buckets) ─────────────────────
module "s3" {
  source = "./modules/s3"

  project        = var.project
  environment    = var.environment
  aws_account_id = var.aws_account_id
  kms_key_arn    = module.kms.key_arn
  tags           = local.common_tags
}

# ─────────────────────────────── Auth ──────────────────────────────────────
module "cognito" {
  source = "./modules/cognito"

  project     = var.project
  environment = var.environment
  tags        = local.common_tags
}

# ─────────────────────────────── Database ─────────────────────────────────
module "rds" {
  source = "./modules/rds"

  project               = var.project
  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  isolated_subnet_ids   = module.vpc.isolated_subnet_ids
  rds_security_group_id = module.vpc.rds_security_group_id
  kms_key_arn           = module.kms.key_arn
  instance_class        = var.rds_instance_class
  allocated_storage     = var.rds_allocated_storage
  multi_az              = var.rds_multi_az
  db_name               = var.rds_db_name
  db_username           = var.rds_username
  tags                  = local.common_tags
}

# ─────────────────────────────── Secrets ─────────────────────────────────
module "secrets" {
  source = "./modules/secrets"

  project               = var.project
  environment           = var.environment
  kms_key_arn           = module.kms.key_arn
  rds_endpoint          = module.rds.endpoint
  rds_username          = module.rds.username
  rds_password          = module.rds.password
  rds_db_name           = module.rds.db_name
  cognito_user_pool_id  = module.cognito.user_pool_id
  cognito_app_client_id = module.cognito.app_client_id
  s3_document_bucket    = module.s3.documents_bucket_name
  aws_region            = var.aws_region
  tags                  = local.common_tags
}

# ─────────────────────────────── ECR ──────────────────────────────────────
module "ecr" {
  source = "./modules/ecr"

  namespace    = var.ecr_namespace
  repositories = local.ecr_services
  kms_key_arn  = module.kms.key_arn
  tags         = local.common_tags
}

# ─────────────────────────────── EKS ──────────────────────────────────────
module "eks" {
  source = "./modules/eks"

  project            = var.project
  environment        = var.environment
  private_subnet_ids = module.vpc.private_subnet_ids
  public_subnet_ids  = module.vpc.public_subnet_ids
  eks_version        = var.eks_version
  node_instance_type = var.node_instance_type
  node_desired_size  = var.node_desired_size
  node_min_size      = var.node_min_size
  node_max_size      = var.node_max_size
  tags               = local.common_tags
}

# Allow worker nodes to reach RDS.
resource "aws_vpc_security_group_ingress_rule" "rds_from_nodes" {
  security_group_id            = module.vpc.rds_security_group_id
  description                  = "PostgreSQL from EKS worker nodes"
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = module.eks.cluster_security_group_id
}

# ─────────────────────────────── IRSA ─────────────────────────────────────
module "irsa" {
  source = "./modules/irsa"

  project                   = var.project
  environment               = var.environment
  oidc_provider_arn         = module.eks.oidc_provider_arn
  oidc_provider_url         = module.eks.oidc_provider_url
  app_namespace             = var.app_namespace
  kms_key_arn               = module.kms.key_arn
  secret_arn                = module.secrets.secret_arn
  documents_bucket_arn      = module.s3.documents_bucket_arn
  knowledge_base_bucket_arn = module.s3.knowledge_base_bucket_arn
  tags                      = local.common_tags
}

# ─────────────────────────── DNS / Certificate ────────────────────────────
module "dns" {
  source = "./modules/dns"

  domain_name    = var.domain_name
  hosted_zone_id = var.hosted_zone_id
  tags           = local.common_tags
}

# ─────────────────────────────── SNS alerts ───────────────────────────────
module "sns" {
  source = "./modules/sns"

  project     = var.project
  environment = var.environment
  alert_email = var.alert_email
  tags        = local.common_tags
}

# ─────────────────── CS-02 Log Intelligence Agent (Lambda) ────────────────
module "log_intel_lambda" {
  source = "./modules/log-intel-lambda"

  project                   = var.project
  environment               = var.environment
  aws_region                = var.aws_region
  vpc_id                    = module.vpc.vpc_id
  private_subnet_ids        = module.vpc.private_subnet_ids
  sns_topic_arn             = module.sns.topic_arn
  secret_arn                = module.secrets.secret_arn
  kms_key_arn               = module.kms.key_arn
  eks_cluster_name          = module.eks.cluster_name
  bedrock_model_id          = var.bedrock_logintel_model_id
  lambda_source_dir         = "${path.root}/../services/log-intel-lambda"
  enable_argocd_correlation = var.enable_argocd_correlation
  tags                      = local.common_tags
}
