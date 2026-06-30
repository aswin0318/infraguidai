# Terraform Module Catalog

Document ID: IG-TF-MODULE-001

Version: 1.0

Owner: Rahul Menon

Owner Role: Platform Engineering Lead

Department: Platform Engineering

Classification: Internal Use Only

Status: Approved

Review Cycle: 6 Months

Last Updated: June 2026

---

# 1. Purpose

This document defines the approved Terraform modules maintained and supported by InfraGuid Technologies Pvt. Ltd.

The objectives of this catalog are:

```text
Module Standardization

Infrastructure Consistency

Reusable Deployments

Reduced Terraform Duplication

AI-Assisted Code Generation
```

This document serves as the authoritative reference for:

```text
Terraform Developers

Platform Engineers

Solutions Architects

AI Assistants
```

---

# 2. Module Usage Philosophy

Infrastructure should be provisioned using:

```text
Approved Modules
```

instead of directly creating AWS resources.

---

Preferred:

```hcl
module "vpc" {

  source = "../../modules/vpc"
}
```

---

Avoid:

```hcl
resource "aws_vpc" "main" {}
resource "aws_subnet" "public" {}
resource "aws_route_table" "public" {}
```

throughout application repositories.

---

# 3. Approved Module Catalog

Current approved modules:

```text
modules/
│
├── vpc
├── security-group
├── alb
├── route53
├── acm
├── eks
├── irsa
├── ecr
├── rds
├── elasticache
├── efs
├── iam-role
├── cloudfront
├── waf
├── bedrock-endpoints
├── secrets-manager
├── monitoring
└── logging
```

---

# 4. Module Standards

Every module must contain:

```text
main.tf

variables.tf

outputs.tf

versions.tf

README.md
```

---

Every module must expose:

```text
Inputs

Outputs

Examples

Documentation
```

---

# 5. VPC Module

Module Name:

```text
vpc
```

---

## Purpose

Creates:

```text
VPC

Subnets

Route Tables

Internet Gateway

NAT Gateway

VPC Endpoints
```

---

## Inputs

```hcl
environment

vpc_cidr

availability_zones

enable_nat_gateway

enable_vpc_endpoints

tags
```

---

## Outputs

```hcl
vpc_id

public_subnet_ids

private_subnet_ids

nat_gateway_ids

route_table_ids
```

---

## Example

```hcl
module "vpc" {

  source = "../../modules/vpc"

  environment = "prod"

  vpc_cidr = "10.0.0.0/16"

  availability_zones = [
    "ap-south-1a",
    "ap-south-1b"
  ]
}
```

---

## Defaults

```text
DNS Enabled

Multi-AZ

Private Route Tables

Encryption Enabled
```

---

# 6. Security Group Module

Module Name:

```text
security-group
```

---

## Purpose

Creates:

```text
Application Security Groups

Database Security Groups

ALB Security Groups
```

---

## Inputs

```hcl
name

description

vpc_id

ingress_rules

egress_rules
```

---

## Outputs

```hcl
security_group_id
```

---

## Standards

Preferred:

```text
Security Group References
```

instead of:

```text
CIDR Based Access
```

---

# 7. ALB Module

Module Name:

```text
alb
```

---

## Purpose

Creates:

```text
Application Load Balancer

Target Groups

Listeners

Listener Rules
```

---

## Inputs

```hcl
name

vpc_id

subnet_ids

certificate_arn

internal

enable_logs
```

---

## Outputs

```hcl
alb_arn

alb_dns_name

target_group_arn
```

---

## Standards

Mandatory:

```text
HTTPS

Health Checks

Multi-AZ
```

---

# 8. Route53 Module

Module Name:

```text
route53
```

---

## Purpose

Creates:

```text
Hosted Zones

DNS Records

Alias Records
```

---

## Inputs

```hcl
zone_name

records

tags
```

---

## Outputs

```hcl
zone_id

record_fqdns
```

---

# 9. ACM Module

Module Name:

```text
acm
```

---

## Purpose

Creates:

```text
TLS Certificates

DNS Validation Records
```

---

## Outputs

```hcl
certificate_arn
```

---

## Standards

Preferred:

```text
DNS Validation
```

---

# 10. EKS Module

Module Name:

```text
eks
```

---

## Purpose

Creates:

```text
EKS Cluster

Managed Node Groups

Cluster IAM

Logging
```

---

## Inputs

```hcl
cluster_name

cluster_version

private_subnet_ids

node_groups

tags
```

---

## Outputs

```hcl
cluster_name

cluster_endpoint

cluster_security_group

oidc_provider_arn
```

---

## Defaults

```text
Managed Node Groups

IRSA Enabled

Control Plane Logs Enabled
```

---

## Mandatory Standards

```text
Multi-AZ

Private Subnets

OIDC Enabled
```

# 11. IRSA Module

Module Name:

```text
irsa
```

---

## Purpose

Creates:

```text
IAM Role

OIDC Trust Policy

Kubernetes Service Account Integration
```

for EKS workloads.

---

## Why IRSA Exists

Without IRSA:

```text
Pods

↓

Node IAM Role

↓

Excessive Permissions
```

---

With IRSA:

```text
Pod

↓

Dedicated IAM Role

↓

Least Privilege Access
```

---

## Inputs

```hcl
role_name

namespace

service_account_name

policy_arns

oidc_provider_arn

tags
```

---

## Outputs

```hcl
role_arn

role_name

service_account_name
```

---

## Example

```hcl
module "external_dns_irsa" {

  source = "../../modules/irsa"

  role_name = "external-dns"

  namespace = "external-dns"

  service_account_name = "external-dns"

  oidc_provider_arn =
    module.eks.oidc_provider_arn
}
```

---

## Standards

Preferred for:

```text
External DNS

ALB Controller

EBS CSI Driver

Application Pods
```

---

# 12. ECR Module

Module Name:

```text
ecr
```

---

## Purpose

Creates:

```text
ECR Repository

Lifecycle Policies

Repository Policies

Image Scanning Configuration
```

---

## Inputs

```hcl
repository_name

image_tag_mutability

scan_on_push

lifecycle_policy

tags
```

---

## Outputs

```hcl
repository_arn

repository_url

repository_name
```

---

## Example

```hcl
module "app_ecr" {

  source = "../../modules/ecr"

  repository_name = "payment-service"
}
```

---

## Defaults

```text
Image Scanning Enabled

Encryption Enabled
```

---

## Standards

Mandatory:

```text
Image Scanning

Lifecycle Policies
```

---

# 13. RDS Module

Module Name:

```text
rds
```

---

## Purpose

Creates:

```text
RDS Instance

Subnet Group

Parameter Group

Monitoring Configuration

Security Group
```

---

## Inputs

```hcl
db_name

engine

engine_version

instance_class

storage_size

multi_az

backup_retention_days

private_subnet_ids

kms_key_arn

tags
```

---

## Outputs

```hcl
db_endpoint

db_port

db_identifier

security_group_id

db_arn
```

---

## Example

```hcl
module "postgres" {

  source = "../../modules/rds"

  db_name = "platform"

  engine = "postgres"

  instance_class = "db.t3.medium"

  multi_az = true
}
```

---

## Defaults

```text
Encryption Enabled

Enhanced Monitoring Enabled

Performance Insights Enabled
```

---

## Production Standards

Mandatory:

```text
Multi-AZ

Private Subnets

Backups Enabled

KMS Encryption
```

---

# 14. ElastiCache Module

Module Name:

```text
elasticache
```

---

## Purpose

Creates:

```text
Redis Cluster

Subnet Group

Parameter Group

Security Group
```

---

## Inputs

```hcl
cluster_name

node_type

engine_version

private_subnet_ids

replicas

tags
```

---

## Outputs

```hcl
primary_endpoint

reader_endpoint

security_group_id
```

---

## Standards

Production:

```text
Replication Enabled

Automatic Failover Enabled

Private Networking Only
```

---

# 15. EFS Module

Module Name:

```text
efs
```

---

## Purpose

Creates:

```text
EFS File System

Mount Targets

Security Groups

Backup Policies
```

---

## Inputs

```hcl
name

subnet_ids

kms_key_arn

performance_mode

throughput_mode

tags
```

---

## Outputs

```hcl
efs_id

efs_dns_name

security_group_id
```

---

## Defaults

```text
Encryption Enabled

Backup Enabled
```

---

## Common Use Cases

```text
Shared Storage

Kubernetes Persistent Volumes

Application Uploads
```

---

# 16. IAM Role Module

Module Name:

```text
iam-role
```

---

## Purpose

Creates:

```text
IAM Roles

Trust Policies

Policy Attachments
```

---

## Inputs

```hcl
role_name

trusted_entities

policy_arns

inline_policies

tags
```

---

## Outputs

```hcl
role_arn

role_name
```

---

## Example

```hcl
module "app_role" {

  source = "../../modules/iam-role"

  role_name = "payment-service-role"
}
```

---

## Standards

Preferred:

```text
Least Privilege

Managed Policies

OIDC Trust Relationships
```

---

Avoid:

```text
AdministratorAccess
```

---

# 17. Secrets Manager Module

Module Name:

```text
secrets-manager
```

---

## Purpose

Creates:

```text
Secrets

Rotation Configuration

KMS Integration

Resource Policies
```

---

## Inputs

```hcl
secret_name

kms_key_arn

rotation_enabled

tags
```

---

## Outputs

```hcl
secret_arn

secret_name
```

---

## Standards

Mandatory:

```text
KMS Encryption

IAM Access Controls
```

---

Never:

```text
Store Secret Values

Inside Terraform Code
```

---

# 18. Monitoring Module

Module Name:

```text
monitoring
```

---

## Purpose

Creates:

```text
CloudWatch Dashboards

CloudWatch Alarms

SNS Notifications

Metric Filters
```

---

## Inputs

```hcl
environment

notification_topic

services

tags
```

---

## Outputs

```hcl
dashboard_name

alarm_arns
```

---

## Standards

Production Monitoring Must Cover:

```text
Availability

Latency

Error Rates

Resource Utilization
```

---

## Default Alarms

```text
CPU

Memory

Disk

Network

Service Health
```

---

# 19. Logging Module

Module Name:

```text
logging
```

---

## Purpose

Creates:

```text
CloudWatch Log Groups

Retention Policies

Subscription Filters

Centralized Logging
```

---

## Inputs

```hcl
log_group_names

retention_days

kms_key_arn

tags
```

---

## Outputs

```hcl
log_group_arns

log_group_names
```

---

## Standards

Production Retention:

```text
90 Days Minimum
```

---

Security Logs:

```text
365 Days Recommended
```

---

# 20. CloudFront Module

Module Name:

```text
cloudfront
```

---

## Purpose

Creates:

```text
CloudFront Distribution

Origins

Cache Policies

OAC

Logging Configuration

TLS Configuration
```

---

## Inputs

```hcl
domain_name

certificate_arn

origins

enable_waf

enable_logging

tags
```

---

## Outputs

```hcl
distribution_id

distribution_arn

distribution_domain_name
```

---

## Defaults

```text
HTTPS Only

Compression Enabled

OAC Enabled
```

---

## Standards

Mandatory:

```text
TLS

Logging

OAC

WAF
```

for internet-facing applications.

---

## Example

```hcl
module "cloudfront" {

  source = "../../modules/cloudfront"

  domain_name = "app.example.com"

  certificate_arn =
    module.acm.certificate_arn
}
```

# 21. WAF Module

Module Name:

```text
waf
```

---

## Purpose

Creates:

```text
AWS WAF Web ACL

Managed Rules

Custom Rules

Rate Limiting Rules

IP Sets
```

---

## Inputs

```hcl
name

enable_managed_rules

rate_limit

allowed_ips

blocked_ips

tags
```

---

## Outputs

```hcl
web_acl_arn

web_acl_id
```

---

## Defaults

```text
AWS Managed Rules

IP Reputation Rules

Known Bad Inputs
```

---

## Production Standards

Mandatory for:

```text
CloudFront

Public ALB

Internet-Facing APIs
```

---

# 22. Bedrock Endpoint Module

Module Name:

```text
bedrock-endpoints
```

---

## Purpose

Creates:

```text
Bedrock Runtime Endpoint

Bedrock Agent Endpoint

Security Groups

IAM Integration
```

---

## Inputs

```hcl
vpc_id

subnet_ids

allowed_security_groups

tags
```

---

## Outputs

```hcl
runtime_endpoint_id

security_group_id
```

---

## Standards

Mandatory:

```text
Private Connectivity

Security Group Restrictions

Logging Enabled
```

---

## Common Usage

```text
Internal AI Assistant

RAG Platform

AI Agent Platform
```

---

# 23. VPC Endpoint Module

Module Name:

```text
vpc-endpoints
```

---

## Purpose

Creates:

```text
Gateway Endpoints

Interface Endpoints
```

for AWS services.

---

## Supported Services

```text
S3

DynamoDB

Secrets Manager

SSM

CloudWatch

Bedrock

ECR
```

---

## Inputs

```hcl
vpc_id

private_subnet_ids

endpoint_services

tags
```

---

## Outputs

```hcl
endpoint_ids

endpoint_dns_names
```

---

## Standards

Production VPCs should deploy:

```text
S3 Endpoint

Secrets Manager Endpoint

SSM Endpoint

CloudWatch Endpoint
```

by default.

---

# 24. Route53 Private DNS Module

Module Name:

```text
private-dns
```

---

## Purpose

Creates:

```text
Private Hosted Zones

Private DNS Records

Service Discovery Records
```

---

## Inputs

```hcl
zone_name

vpc_id

records

tags
```

---

## Outputs

```hcl
zone_id

record_names
```

---

## Common Usage

```text
Database Endpoints

Internal APIs

Service Discovery
```

---

## Example

```text
db.internal.infraguid.local

grafana.internal.infraguid.local

argocd.internal.infraguid.local
```

---

# 25. Backup Module

Module Name:

```text
backup
```

---

## Purpose

Creates:

```text
AWS Backup Vault

Backup Plans

Retention Policies

Backup Selections
```

---

## Inputs

```hcl
backup_plan_name

retention_days

resource_arns

tags
```

---

## Outputs

```hcl
backup_vault_arn

backup_plan_id
```

---

## Production Standards

Minimum:

```text
7 Day Retention
```

---

Recommended:

```text
30 Day Retention
```

---

## Protected Resources

```text
RDS

EFS

EBS

DynamoDB
```

---

# 26. Shared Tags Module

Module Name:

```text
shared-tags
```

---

## Purpose

Creates:

```text
Standardized Tag Set
```

used across all resources.

---

## Inputs

```hcl
environment

owner

project

cost_center
```

---

## Outputs

```hcl
common_tags
```

---

## Example

```hcl
module "tags" {

  source = "../../modules/shared-tags"

  environment = "prod"

  owner = "PlatformEngineering"

  project = "InfraGuid"
}
```

---

## Output Example

```hcl
{
  Environment = "prod"

  Owner = "PlatformEngineering"

  ManagedBy = "Terraform"

  Project = "InfraGuid"

  CostCenter = "Cloud"
}
```

---

# 27. Complete Architecture Blueprints

This section teaches AI assistants how approved modules should be combined.

---

# Blueprint 1

Standard Three-Tier Application

---

## Modules

```hcl
module "vpc"

module "alb"

module "eks"

module "rds"

module "monitoring"

module "logging"
```

---

## Architecture

```text
Internet

↓

CloudFront

↓

ALB

↓

EKS

↓

RDS
```

---

## Recommended Environment

```text
Production
```

---

# Blueprint 2

Static Website Platform

---

## Modules

```hcl
module "acm"

module "cloudfront"

module "route53"

module "waf"
```

---

## Architecture

```text
CloudFront

↓

S3

↓

Route53
```

---

## Recommended Environment

```text
Marketing Sites

Documentation Sites
```

---

# Blueprint 3

Internal AI Assistant

---

## Modules

```hcl
module "vpc"

module "eks"

module "bedrock-endpoints"

module "vpc-endpoints"

module "secrets-manager"

module "monitoring"

module "logging"
```

---

## Architecture

```text
User

↓

Application

↓

Bedrock

↓

Vector Store

↓

Knowledge Base
```

---

## Recommended Environment

```text
Enterprise AI Systems
```

---

# Blueprint 4

Production EKS Platform

---

## Modules

```hcl
module "vpc"

module "eks"

module "irsa"

module "ecr"

module "monitoring"

module "logging"
```

---

## Architecture

```text
Developers

↓

GitHub Actions

↓

ECR

↓

EKS
```

---

# 28. AI Terraform Generation Examples

This section provides canonical examples for AI assistants.

---

## User Request

```text
Create Production VPC
```

---

## Preferred Output

```hcl
module "vpc" {

  source = "../../modules/vpc"

  environment = "prod"

  vpc_cidr = "10.0.0.0/16"

  enable_nat_gateway = true
}
```

---

Avoid:

```hcl
resource "aws_vpc" "main" {}
resource "aws_subnet" "public" {}
resource "aws_route_table" "public" {}
```

unless explicitly requested.

---

## User Request

```text
Create Production PostgreSQL
```

---

## Preferred Output

```hcl
module "postgres" {

  source = "../../modules/rds"

  engine = "postgres"

  multi_az = true

  backup_retention_days = 30
}
```

---

## User Request

```text
Create EKS Cluster
```

---

## Preferred Output

```hcl
module "eks" {

  source = "../../modules/eks"

  cluster_name = "platform"

  cluster_version = "1.33"
}
```

---

## AI Generation Priority

Always prefer:

```text
Module

↓

Module

↓

Module
```

---

Instead of:

```text
Raw Resources
```

---

# 29. Module Selection Decision Matrix

This section helps AI systems choose the correct module.

---

| Requirement | Module |
|------------|---------|
| Networking | vpc |
| Security Groups | security-group |
| Load Balancer | alb |
| DNS | route53 |
| TLS Certificates | acm |
| Kubernetes | eks |
| Pod IAM | irsa |
| Container Registry | ecr |
| Database | rds |
| Cache | elasticache |
| Shared Storage | efs |
| IAM Roles | iam-role |
| Secrets | secrets-manager |
| CDN | cloudfront |
| WAF | waf |
| AI Connectivity | bedrock-endpoints |
| AWS Private Connectivity | vpc-endpoints |
| Monitoring | monitoring |
| Logging | logging |
| Backup | backup |

---

## AI Decision Rule

When multiple resources are requested:

```text
Choose Existing Modules

Combine Modules

Generate Composition
```

---

Avoid generating:

```text
Individual AWS Resources
```

when approved modules exist.

---

# 30. Module Catalog Governance Statement

This document defines the approved Terraform module ecosystem used by InfraGuid Technologies Pvt. Ltd.

All Terraform repositories, infrastructure deployments, AI-generated Terraform code, platform automation systems, and cloud provisioning workflows must use the modules defined within this catalog whenever applicable.

The objectives of this catalog are:

```text
Consistency

Reusability

Security

Scalability

Operational Excellence
```

Platform Engineering owns and maintains all approved Terraform modules.

Architecture is responsible for module design standards.

Security Engineering is responsible for module security validation.

Exceptions require approval from:

```text
Platform Engineering Lead

Solutions Architect

Security Engineering Lead
```

This document serves as the authoritative Terraform module reference for all InfraGuid-managed AWS environments.