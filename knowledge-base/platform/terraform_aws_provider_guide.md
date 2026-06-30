# Terraform AWS Provider Guide

Document ID: IG-TF-AWS-001

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

This document defines the official Terraform development standards used by InfraGuid Technologies Pvt. Ltd. when provisioning AWS infrastructure.

The purpose of this guide is to ensure:

```text
Consistent Infrastructure

Reusable Terraform Code

Secure Deployments

Predictable Resource Naming

Operational Maintainability
```

across all AWS environments.

This document serves as the authoritative reference for Terraform code generation, review, deployment, and maintenance.

---

# 2. Core Terraform Philosophy

Terraform code must be:

```text
Readable

Reusable

Idempotent

Version Controlled

Environment Agnostic
```

---

## Primary Objectives

Infrastructure should be:

```text
Automated

Repeatable

Auditable

Recoverable
```

---

## Anti-Patterns

Avoid:

```text
Hardcoded Values

Copy-Paste Modules

Inline Secrets

Environment-Specific Logic
```

---

# 3. Approved Terraform Version

## Production Standard

```hcl
terraform {

  required_version = ">= 1.8.0"
}
```

---

## Reason

Provides:

```text
Long-Term Support

Bug Fixes

Provider Compatibility
```

---

## Version Pinning

All repositories must explicitly define:

```text
required_version
```

---

# 4. AWS Provider Standards

Every repository must define:

```hcl
terraform {

  required_providers {

    aws = {

      source  = "hashicorp/aws"

      version = "~> 6.0"
    }
  }
}
```

---

## Provider Configuration

```hcl
provider "aws" {

  region = var.aws_region
}
```

---

## Rules

Never:

```text
Hardcode Regions
```

---

Always:

```text
Use Variables
```

---

# 5. Repository Structure Standard

All Terraform repositories must follow:

```text
terraform/
│
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
│
├── modules/
│   ├── vpc/
│   ├── eks/
│   ├── rds/
│   ├── alb/
│   └── security-group/
│
├── global/
│
├── versions.tf
├── providers.tf
├── variables.tf
├── outputs.tf
└── README.md
```

---

## Benefits

```text
Consistency

Maintainability

Reusability
```

---

# 6. Module Design Standards

Terraform modules are mandatory for reusable infrastructure.

---

## Module Objectives

Modules must be:

```text
Reusable

Composable

Environment Independent
```

---

## Module Structure

```text
module/
│
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
└── README.md
```

---

## Module Rules

Modules must never:

```text
Contain Backend Configurations

Contain Environment-Specific Values
```

---

# 7. Variable Standards

Variables must be strongly typed.

---

## Good Example

```hcl
variable "vpc_cidr" {

  description = "CIDR block for VPC"

  type = string
}
```

---

## Bad Example

```hcl
variable "vpc_cidr" {}
```

---

## Requirements

Every variable must include:

```text
Description

Type

Validation (when applicable)
```

---

## Validation Example

```hcl
variable "environment" {

  type = string

  validation {

    condition = contains(
      ["dev","staging","prod"],
      var.environment
    )

    error_message =
      "Invalid environment."
  }
}
```

---

# 8. Output Standards

Outputs expose important resource attributes.

---

## Example

```hcl
output "vpc_id" {

  value = aws_vpc.main.id

  description = "VPC Identifier"
}
```

---

## Rules

Outputs should expose:

```text
IDs

ARNs

DNS Names

Endpoints
```

---

Do not expose:

```text
Secrets

Passwords

Tokens
```

---

# 9. Naming Convention Standards

Consistent naming is mandatory.

---

## Pattern

```text
company-environment-resource
```

---

Example:

```text
infraguid-prod-vpc

infraguid-prod-alb

infraguid-dev-rds
```

---

## Terraform Resource Names

Use:

```hcl
resource "aws_vpc" "main"
```

---

Avoid:

```hcl
resource "aws_vpc" "my_vpc_prod"
```

---

## Preferred Resource Labels

```text
main

public

private

db

app

eks
```

---

# 10. Tagging Standards

Every resource must contain tags.

---

## Required Tags

```hcl
tags = {

  Name        = "infraguid-prod-vpc"

  Environment = "prod"

  ManagedBy   = "Terraform"

  Owner       = "PlatformEngineering"

  CostCenter  = "Cloud"

  Project     = "InfraGuid"
}
```

---

## Purpose

Supports:

```text
Cost Allocation

Ownership

Automation

Governance
```

---

# 11. Local Values Standards

Use locals for derived values.

---

## Example

```hcl
locals {

  name_prefix =
    "infraguid-${var.environment}"
}
```

---

Benefits:

```text
Reduced Duplication

Improved Readability
```

---

## Rule

Prefer:

```text
locals
```

for reusable calculations.

---

Avoid:

```text
Repeated String Construction
```
# 12. Backend Standards

Terraform state is the source of truth for deployed infrastructure.

Loss or corruption of state can result in:

```text
Infrastructure Drift

Failed Deployments

Resource Recreation

Operational Outages
```

---

## 12.1 Approved Backend

InfraGuid standard:

```text
S3 Backend
+
DynamoDB Locking
```

---

## Architecture

```text
Terraform

↓

S3 State File

↓

DynamoDB Lock
```

---

## Example

```hcl
terraform {

  backend "s3" {

    bucket = "infraguid-tf-state"

    key = "prod/networking/terraform.tfstate"

    region = "ap-south-1"

    dynamodb_table = "terraform-locks"

    encrypt = true
  }
}
```

---

## Requirements

All production deployments must use:

```text
Remote State

Encryption

State Locking
```

---

Never:

```text
Store State Locally
```

for production environments.

---

# 13. Remote State Standards

Remote state enables:

```text
Collaboration

Consistency

Disaster Recovery
```

---

## 13.1 State Organization

Recommended structure:

```text
prod/

staging/

dev/
```

---

Example:

```text
prod/networking

prod/eks

prod/security
```

---

## 13.2 State Separation

Separate state files by:

```text
Networking

Security

Compute

Databases
```

---

Avoid:

```text
Single Giant State File
```

---

## Bad Example

```text
500+ Resources

One State File
```

---

## Good Example

```text
networking.tfstate

eks.tfstate

rds.tfstate
```

---

## Benefits

```text
Faster Plans

Reduced Blast Radius

Easier Recovery
```

---

## 13.3 Remote State Access

Use:

```hcl
data "terraform_remote_state"
```

when required.

---

Example:

```hcl
data "terraform_remote_state" "networking" {

  backend = "s3"

  config = {

    bucket = "infraguid-tf-state"

    key = "prod/networking/terraform.tfstate"

    region = "ap-south-1"
  }
}
```

---

## Rule

Consume outputs only.

Never depend on:

```text
Internal Resource Structure
```

of another state.

---

# 14. State Locking Standards

State locking prevents concurrent modifications.

---

## Why Locking Exists

Without locking:

```text
Engineer A Apply

↓

Engineer B Apply

↓

State Corruption
```

---

## Approved Locking Method

```text
DynamoDB
```

---

## Lock Table Requirements

Partition Key:

```text
LockID
```

---

Billing Mode:

```text
PAY_PER_REQUEST
```

---

## InfraGuid Standard

All production state files must use:

```text
State Locking
```

---

## Operational Procedure

Never manually delete lock entries unless:

```text
Deployment Confirmed Stopped

Lock Verified Stale
```

---

# 15. Data Source Standards

Data sources retrieve information from existing infrastructure.

---

## Purpose

Used when:

```text
Resource Already Exists
```

---

## Example

```hcl
data "aws_vpc" "existing" {

  tags = {

    Name = "infraguid-prod-vpc"
  }
}
```

---

## Benefits

```text
Reduced Duplication

Infrastructure Reuse

Cleaner Code
```

---

## Data Source Rules

Use data sources for:

```text
Shared VPC

Shared KMS

Shared Route53

Shared IAM
```

---

Avoid:

```text
Hardcoded IDs
```

---

## Bad Example

```hcl
vpc_id = "vpc-123456"
```

---

## Good Example

```hcl
vpc_id = data.aws_vpc.main.id
```

---

# 16. Terraform Security Standards

Security must be embedded into Terraform design.

---

## 16.1 Secrets Management

Never store:

```text
Passwords

API Keys

Tokens

Certificates
```

inside:

```text
Terraform Code

Variables Files

Git Repositories
```

---

## Approved Storage

```text
AWS Secrets Manager

AWS SSM Parameter Store
```

---

## Example

```hcl
data "aws_secretsmanager_secret_version" "db" {

  secret_id = "database-password"
}
```

---

## 16.2 Encryption Standards

Enable encryption for:

```text
S3

EBS

RDS

EFS
```

---

## Requirement

Encryption enabled by default.

---

## 16.3 Public Exposure

Avoid:

```text
0.0.0.0/0
```

unless justified.

---

Must be reviewed during:

```text
Code Review
```

---

## 16.4 Logging Standards

Enable:

```text
CloudTrail

VPC Flow Logs

CloudWatch Logs
```

for production systems.

---

# 17. IAM Standards

Terraform-generated IAM resources must follow least privilege principles.

---

## IAM Policy Design

Preferred:

```text
Specific Actions

Specific Resources
```

---

Avoid:

```json
{
  "Action": "*",
  "Resource": "*"
}
```

---

## IAM Role Standards

Preferred:

```text
Roles
```

instead of:

```text
Users
```

---

## Terraform Example

```hcl
resource "aws_iam_role" "app" {

  name = "app-role"
}
```

---

## OIDC Standard

GitHub Actions must use:

```text
OIDC Authentication
```

---

Avoid:

```text
Static Access Keys
```

---

## IAM Module Rule

All IAM resources should be managed through:

```text
Reusable Modules
```

---

# 18. Networking Standards

Networking resources must align with:

```text
aws_vpc_guide.md
```

---

## VPC Standard

Production:

```text
/16 CIDR
```

---

## Availability

Production networking must be:

```text
Multi-AZ
```

---

## NAT Standard

Production:

```text
One NAT Per AZ
```

---

## Route Tables

Every subnet must have:

```text
Explicit Route Association
```

---

## Security Groups

Preferred:

```text
Security Group References
```

instead of CIDR-based rules.

---

## Endpoint Standard

Use:

```text
Gateway Endpoints

Interface Endpoints
```

whenever appropriate.

---

# 19. EKS Standards

Terraform-generated Kubernetes platforms must follow InfraGuid EKS standards.

---

## Cluster Design

Production clusters require:

```text
Multi-AZ Deployment
```

---

## Node Groups

Use:

```text
Managed Node Groups
```

---

Avoid:

```text
Self Managed Nodes
```

unless justified.

---

## Authentication

Use:

```text
IAM Roles

IRSA
```

---

Avoid:

```text
Long-Lived Credentials
```

inside pods.

---

## Logging

Enable:

```text
Control Plane Logs
```

---

## Terraform Structure

Separate modules:

```text
Cluster

Node Groups

Addons
```

---

## Addon Standards

Mandatory:

```text
VPC CNI

CoreDNS

kube-proxy
```

---

Recommended:

```text
EBS CSI Driver

Metrics Server
```

---

# 20. RDS Standards

Terraform-generated databases must follow enterprise standards.

---

## Availability

Production:

```text
Multi-AZ Required
```

---

## Backups

Minimum:

```text
7 Days
```

---

Recommended:

```text
30 Days
```

---

## Encryption

Mandatory:

```text
KMS Encryption
```

---

## Public Access

Production:

```text
Publicly Accessible = false
```

---

## Security Groups

Allow access from:

```text
Application Security Groups
```

---

Avoid:

```text
CIDR-Based Broad Access
```

---

## Parameter Groups

Must be explicitly managed.

---

Avoid:

```text
Default Parameter Groups
```

for production.

---

## Monitoring

Enable:

```text
Enhanced Monitoring

Performance Insights
```

---

## Terraform Design

Database modules should expose:

```text
Endpoint

Port

ARN

Security Group
```

---

Must never expose:

```text
Passwords

Secrets

Credentials
```
# 21. ALB Standards

Application Load Balancers must follow consistent deployment patterns.

---

## 21.1 Purpose

ALBs provide:

```text
Layer 7 Routing

SSL Termination

Load Distribution

Health Checks
```

---

## 21.2 Production Standard

Deploy ALBs across:

```text
Minimum 2 AZs
```

---

## 21.3 Subnet Placement

Internet-facing ALBs:

```text
Public Subnets
```

---

Internal ALBs:

```text
Private Subnets
```

---

## 21.4 Health Checks

Mandatory.

Must monitor:

```text
Application Endpoint
```

---

Avoid:

```text
/
```

when dedicated health endpoints exist.

---

Preferred:

```text
/health

/ready

/live
```

---

## 21.5 SSL Standard

Use:

```text
AWS ACM
```

for certificates.

---

Never:

```text
Store Certificates
Inside Terraform
```

---

## 21.6 Logging

Enable:

```text
ALB Access Logs
```

for production.

---

## 21.7 Terraform Design

ALB module should expose:

```text
DNS Name

ARN

Target Group ARN

Security Group
```

---

# 22. CloudFront Standards

CloudFront deployments must align with:

```text
aws_cloudfront_guide.md
```

---

## Distribution Design

Preferred:

```text
CloudFront

↓

ALB

↓

Application
```

---

## Security

Mandatory:

```text
HTTPS

WAF

OAC
```

---

## Caching

Static Assets:

```text
Long TTL
```

---

Dynamic APIs:

```text
Short TTL
```

---

## Compression

Enable:

```text
Brotli

Gzip
```

---

## Logging

Enable:

```text
CloudFront Logs
```

for production.

---

## Terraform Modules

CloudFront modules should support:

```text
Multiple Origins

WAF

Custom Domains

TLS
```

---

# 23. Bedrock Standards

Terraform deployments involving AI workloads must follow Bedrock standards.

---

## Access Pattern

Preferred:

```text
Private VPC Endpoint
```

---

Avoid:

```text
Public Internet Access
```

when possible.

---

## IAM

Grant:

```text
bedrock:InvokeModel
```

only when required.

---

Avoid:

```text
bedrock:*
```

---

## Observability

AI workloads must include:

```text
Logging

Metrics

Cost Monitoring
```

---

## RAG Systems

Terraform should provision:

```text
Vector Store

Secrets

Networking

IAM

Monitoring
```

as separate modules.

---

# 24. Terraform Code Style Guide

Code consistency improves maintainability.

---

## Resource Ordering

Preferred order:

```text
Locals

Data Sources

Resources

Outputs
```

---

## Resource Formatting

Good:

```hcl
resource "aws_vpc" "main" {

  cidr_block = var.vpc_cidr

  tags = local.common_tags
}
```

---

Avoid:

```hcl
resource "aws_vpc" "main"{cidr_block=var.vpc_cidr}
```

---

## Variable Naming

Use:

```text
snake_case
```

---

Example:

```hcl
vpc_cidr

cluster_name

environment
```

---

Avoid:

```hcl
VpcCIDR

ClusterName
```

---

## Resource Naming

Use:

```text
main

public

private

db

app
```

---

Avoid:

```text
random names
```

---

## Comments

Explain:

```text
Why
```

not:

```text
What
```

---

# 25. Reusable Module Patterns

Infrastructure should be modular.

---

## Recommended Modules

```text
VPC

ALB

EKS

RDS

IAM

Security Groups

CloudFront

Bedrock
```

---

## Module Inputs

Accept:

```text
Environment

Tags

Names

Configuration
```

---

## Module Outputs

Expose:

```text
IDs

ARNs

Endpoints

DNS Names
```

---

## Module Independence

Modules must not assume:

```text
Specific Environments
```

---

Bad:

```hcl
environment = "prod"
```

inside module.

---

Good:

```hcl
environment = var.environment
```

---

# 26. Environment Design Standards

Infrastructure must support:

```text
Development

Staging

Production
```

---

## Isolation

Each environment should have:

```text
Separate State

Separate Variables

Separate Resources
```

---

## Environment Variables

Recommended:

```hcl
terraform.tfvars

dev.tfvars

prod.tfvars
```

---

## Resource Naming

Examples:

```text
infraguid-dev-vpc

infraguid-staging-vpc

infraguid-prod-vpc
```

---

## Production Controls

Production requires:

```text
Approvals

Code Review

State Protection
```

---

# 27. CI/CD Standards

Terraform execution must occur through pipelines.

---

## Approved Platforms

```text
GitHub Actions

GitLab CI

Jenkins
```

---

## Authentication

Mandatory:

```text
OIDC
```

---

Avoid:

```text
Static AWS Keys
```

---

## Deployment Workflow

```text
Commit

↓

PR

↓

Terraform Validate

↓

Terraform Plan

↓

Review

↓

Terraform Apply
```

---

## Pipeline Stages

Required:

```text
fmt

validate

lint

plan

apply
```

---

## Security Scanning

Recommended:

```text
Checkov

tfsec

Trivy
```

---

# 28. Pull Request Standards

Every Terraform change requires review.

---

## Required Review Items

Verify:

```text
Security

Cost Impact

Naming

Tags

State Impact
```

---

## Reviewer Checklist

Confirm:

```text
No Secrets

Least Privilege

Proper Tags

Module Reuse
```

---

## Production Changes

Require:

```text
Platform Review

Architecture Review
```

for significant infrastructure changes.

---

# 29. Common Terraform Anti-Patterns

These patterns must be avoided.

---

## Anti-Pattern 1

Hardcoded Values

Bad:

```hcl
region = "ap-south-1"
```

---

Good:

```hcl
region = var.aws_region
```

---

## Anti-Pattern 2

Copy-Paste Infrastructure

Bad:

```text
Duplicated Resources
```

---

Good:

```text
Reusable Modules
```

---

## Anti-Pattern 3

Inline Secrets

Bad:

```hcl
password = "admin123"
```

---

Good:

```text
Secrets Manager
```

---

## Anti-Pattern 4

AdministratorAccess Everywhere

Bad:

```text
Excessive Permissions
```

---

Good:

```text
Least Privilege
```

---

## Anti-Pattern 5

Single Massive State File

Bad:

```text
1000+ Resources
```

---

Good:

```text
Logical State Separation
```

---

## Anti-Pattern 6

Public Databases

Bad:

```hcl
publicly_accessible = true
```

---

Good:

```hcl
publicly_accessible = false
```

---

# 30. Terraform Generation Rules For AI Systems

This section defines mandatory rules that AI assistants must follow when generating Terraform code.

This section is specifically intended for:

```text
Internal AI Assistants

Code Generation Systems

RAG-Based Terraform Copilots
```

---

## Rule 1

Always generate:

```hcl
terraform {

  required_version = ">= 1.8.0"

  required_providers {

    aws = {

      source = "hashicorp/aws"

      version = "~> 6.0"
    }
  }
}
```

unless explicitly instructed otherwise.

---

## Rule 2

Always use:

```text
Variables
```

for:

```text
Region

CIDR

Environment

Names
```

---

Never hardcode.

---

## Rule 3

Always include:

```text
Tags
```

on supported resources.

---

Required tags:

```text
Name

Environment

ManagedBy

Owner

Project
```

---

## Rule 4

Use:

```text
Least Privilege IAM
```

---

Never generate:

```json
{
  "Action": "*",
  "Resource": "*"
}
```

unless explicitly requested.

---

## Rule 5

Production infrastructure must be:

```text
Multi-AZ
```

---

Examples:

```text
ALB

EKS

RDS

NAT Gateway
```

---

## Rule 6

Databases must default to:

```hcl
publicly_accessible = false
```

---

## Rule 7

Storage services must default to:

```text
Encryption Enabled
```

---

Examples:

```text
S3

EBS

RDS

EFS
```

---

## Rule 8

Prefer:

```text
Modules
```

for:

```text
VPC

EKS

RDS

IAM

CloudFront
```

---

## Rule 9

Never generate:

```text
Secrets

Passwords

Tokens
```

inside Terraform code.

---

Use:

```text
Secrets Manager

SSM Parameter Store
```

---

## Rule 10

Always expose useful outputs.

Examples:

```text
VPC ID

ALB DNS

RDS Endpoint

Cluster Endpoint
```

---

## Rule 11

Prefer:

```text
Data Sources
```

over:

```text
Hardcoded IDs
```

---

## Rule 12

For production architectures generate:

```text
VPC Endpoints

CloudTrail

Flow Logs

Monitoring
```

when applicable.

---

## Rule 13

GitHub Actions integrations must use:

```text
OIDC
```

---

Never generate:

```text
AWS Access Keys
```

for CI/CD.

---

## Rule 14

Generated Terraform must be:

```text
terraform fmt compliant
```

---

## Rule 15

Generated Terraform should include:

```text
Brief Comments

Descriptions

Output Descriptions
```

to improve maintainability.

---

## Final Generation Objective

When generating Terraform, the AI assistant must prioritize:

```text
Security

Maintainability

Reusability

Scalability

Operational Excellence
```

over minimal code length.
