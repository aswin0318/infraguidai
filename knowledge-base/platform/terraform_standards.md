# Terraform Standards Guide

Document ID: IG-TF-001

Version: 1.0

Owner: Sneha Iyer

Owner Role: Senior DevOps Engineer

Department: Platform Engineering

Classification: Internal Use Only

Status: Approved

Review Cycle: 6 Months

Last Updated: June 2026

---

# 1. Purpose

This document defines the official Terraform standards, practices, governance controls, and Infrastructure as Code (IaC) requirements used by InfraGuid Technologies Pvt. Ltd.

Terraform is the primary Infrastructure as Code platform used by InfraGuid for provisioning, managing, and maintaining cloud infrastructure across client environments and internal platforms.

The objective of this document is to ensure:

- Consistent infrastructure deployment practices
- Reusable infrastructure modules
- Secure infrastructure provisioning
- Controlled infrastructure changes
- Repeatable deployment workflows
- Reduced operational risk
- Improved maintainability
- Compliance with architectural standards

This document serves as the authoritative Terraform governance guide for all engineers working within InfraGuid-managed environments.

---

# 2. Scope

This standard applies to:

## AWS Infrastructure

Including but not limited to:

- VPC
- Route Tables
- NAT Gateways
- Security Groups
- Application Load Balancers
- CloudFront
- Route53
- IAM
- EKS
- EC2
- RDS
- EFS
- S3
- Lambda
- Bedrock Integrations

---

## Internal Platforms

Including:

- AI Knowledge Platforms
- Internal Automation Systems
- Monitoring Platforms
- Platform Tooling

---

## Client Environments

Including:

- Development
- Staging
- Production

---

## Exclusions

The following activities are excluded:

- Manual console experimentation in sandbox accounts
- Temporary proof-of-concept environments
- Local development environments

Even for excluded environments, Terraform usage is strongly encouraged.

---

# 3. Terraform Principles

All Terraform implementations at InfraGuid must follow the principles defined below.

These principles take precedence over individual implementation preferences.

---

## Infrastructure As Code First

All cloud infrastructure must be provisioned through Terraform.

Infrastructure changes performed manually through the AWS Console are prohibited unless:

- Emergency incident response requires immediate action
- AWS Support requests temporary intervention
- Disaster recovery activities require manual execution

Any manual changes must subsequently be imported into Terraform state or removed.

---

## Reproducibility

Infrastructure must be reproducible.

A complete environment should be deployable using:

```bash
terraform init
terraform plan
terraform apply
```

without requiring undocumented manual steps.

---

## Idempotency

Terraform deployments must be idempotent.

Multiple executions of:

```bash
terraform apply
```

must produce the same infrastructure state.

Terraform code should never rely on:

- Manual post-deployment actions
- One-time configuration procedures
- Hidden operational dependencies

---

## Least Privilege

Terraform-managed resources must follow least-privilege principles.

Examples:

- IAM roles should grant only required permissions
- Security groups should expose only required ports
- S3 buckets should deny public access unless explicitly approved

---

## Modular Design

Infrastructure must be implemented using reusable modules.

Terraform code duplication should be minimized.

Modules should represent reusable infrastructure building blocks.

Examples:

- VPC Module
- EKS Module
- ALB Module
- RDS Module
- Security Group Module

---

## Version Controlled Infrastructure

All Terraform code must be stored within approved Git repositories.

Terraform code must never be maintained:

- On engineer laptops
- In shared folders
- Outside version control systems

Git serves as the source of truth.

---

## Peer Review Requirement

No Terraform changes may be deployed directly to production.

All Terraform changes require:

- Pull Request
- Peer Review
- Approval

before deployment.

---

## Security By Default

Terraform code should implement secure defaults.

Examples:

- Encryption enabled
- Logging enabled
- Versioning enabled
- Public access blocked

Security controls should be enabled by default rather than added later.

---

## Drift Awareness

Terraform-managed resources must remain synchronized with Terraform state.

Configuration drift should be:

- Detected
- Investigated
- Remediated

on a regular basis.

---

## Automation First

Terraform workflows should be automated through CI/CD pipelines whenever possible.

Manual execution should be minimized.

Examples:

- Automated Validation
- Automated Plan Generation
- Automated Security Scanning
- Automated Deployment Approvals

---

# 4. Repository Structure Standards

Terraform repositories must follow a consistent structure across all InfraGuid projects.

Consistency improves:

- Maintainability
- Onboarding
- Troubleshooting
- Automation

---

## Standard Repository Structure

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
│   ├── alb/
│   ├── rds/
│   ├── efs/
│   ├── cloudfront/
│   └── security-group/
│
├── scripts/
│
├── policies/
│
├── docs/
│
└── .github/
```

---

## Environment Directory Purpose

The environments directory contains environment-specific configurations.

Examples:

```text
dev

staging

prod
```

Environment folders should contain:

- Backend Configuration
- Variable Definitions
- Module Invocations

Business logic should not be duplicated across environments.

---

## Module Directory Purpose

Modules contain reusable infrastructure components.

Modules should:

- Have a single responsibility
- Be reusable
- Be independently testable
- Follow semantic versioning

Examples:

```text
modules/vpc

modules/eks

modules/rds
```

---

## Script Directory Purpose

Contains:

- Validation Scripts
- Deployment Helpers
- Operational Utilities

Terraform business logic should never be hidden inside scripts.

Scripts should support Terraform, not replace Terraform.

---

## Policy Directory Purpose

Contains:

- OPA Policies
- Sentinel Policies
- Security Validation Rules
- Compliance Controls

---

## Documentation Directory Purpose

Contains:

- Architecture Notes
- Deployment Guides
- Module Documentation

Every Terraform repository must contain documentation.

---

# 5. Environment Structure Standards

InfraGuid environments must be logically separated.

Environment isolation reduces operational risk.

---

## Approved Environments

Every platform should contain:

```text
Development

Staging

Production
```

---

## Development Environment

Purpose:

```text
Feature Development

Testing

Experimentation
```

Characteristics:

- Lower cost
- Reduced redundancy
- Limited data

---

## Staging Environment

Purpose:

```text
Pre-Production Validation
```

Characteristics:

- Production-like architecture
- Full deployment testing
- Security validation

---

## Production Environment

Purpose:

```text
Customer Facing Workloads
```

Characteristics:

- High availability
- Monitoring enabled
- Backup enabled
- Disaster recovery enabled

# 6. Module Standards

Terraform modules are the foundational building blocks of all Infrastructure as Code implementations at InfraGuid.

Every module should be designed for:

- Reusability
- Maintainability
- Security
- Consistency
- Predictability

Modules should represent infrastructure components rather than entire environments.

---

## 6.1 Module Design Principles

Every module must:

- Have a single responsibility
- Be reusable
- Be environment agnostic
- Support versioning
- Include documentation
- Support automated validation

Examples:

Good:

```text
VPC Module

ALB Module

RDS Module

EKS Module
```

Bad:

```text
Entire Production Environment Module
```

---

## 6.2 Module Structure Standard

Every module must follow:

```text
module-name/
│
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── README.md
├── examples/
└── tests/
```

---

## 6.3 Required Files

### main.tf

Contains:

- Resource Definitions
- Data Sources
- Core Logic

Should remain focused.

Avoid excessively large files.

---

### variables.tf

Contains:

- Input Variables
- Validation Rules
- Defaults

Every variable should include:

```hcl
description
type
```

Example:

```hcl
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}
```

---

### outputs.tf

Contains exported values.

Example:

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}
```

---

### versions.tf

Defines:

```hcl
terraform {
  required_version = ">= 1.8"
}
```

and provider versions.

---

### README.md

Required.

Must contain:

- Purpose
- Inputs
- Outputs
- Usage Examples
- Owner

---

## 6.4 Module Ownership

Every module must have:

```text
Primary Owner

Backup Owner
```

Ownership information must be documented.

---

## 6.5 Module Versioning

Modules must follow:

```text
Semantic Versioning
```

Format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.2.3
```

---

### Major Version

Breaking Changes.

Example:

```text
v1 → v2
```

---

### Minor Version

Backward-compatible enhancements.

---

### Patch Version

Bug fixes.

---

## 6.6 Module Inputs

Inputs should be:

- Explicit
- Validated
- Documented

---

### Validation Example

```hcl
variable "environment" {

  type = string

  validation {
    condition = contains(
      ["dev","staging","prod"],
      var.environment
    )

    error_message = "Invalid environment."
  }
}
```

---

## 6.7 Module Outputs

Only expose necessary outputs.

Avoid exposing:

- Secrets
- Sensitive Tokens
- Passwords

---

## 6.8 Module Security Requirements

Modules must:

```text
Enable Encryption

Enable Logging

Block Public Access

Use Least Privilege
```

by default.

---

## 6.9 Module Testing Standards

All modules must be validated before release.

Required validation:

```bash
terraform validate
```

```bash
terraform fmt
```

```bash
tflint
```

---

## 6.10 Module Documentation Requirements

Every module must document:

```text
Purpose

Owner

Inputs

Outputs

Dependencies

Examples
```

---

# 7. Naming Standards

Consistent naming improves:

- Readability
- Operations
- Troubleshooting
- Governance

All Terraform-managed resources must follow InfraGuid naming standards.

---

## 7.1 Naming Convention Format

Standard format:

```text
<company>-<environment>-<service>-<resource>
```

Example:

```text
infraguid-prod-platform-vpc
```

---

## 7.2 Environment Identifiers

Approved values:

```text
dev

staging

prod
```

Only.

---

## 7.3 Resource Naming Examples

### VPC

```text
infraguid-prod-vpc
```

---

### ALB

```text
infraguid-prod-alb
```

---

### EKS

```text
infraguid-prod-eks
```

---

### RDS

```text
infraguid-prod-postgres
```

---

### EFS

```text
infraguid-prod-efs
```

---

## 7.4 Security Group Naming

Format:

```text
<service>-sg
```

Examples:

```text
alb-sg

eks-node-sg

rds-sg
```

---

## 7.5 IAM Naming

Roles:

```text
infraguid-prod-eks-role
```

Policies:

```text
infraguid-prod-s3-policy
```

---

## 7.6 S3 Naming

Format:

```text
company-environment-purpose
```

Example:

```text
infraguid-prod-tf-state
```

---

## 7.7 Terraform Resource Naming

Within Terraform code:

Use:

```hcl
resource "aws_vpc" "main"
```

not:

```hcl
resource "aws_vpc" "vpc1"
```

Names should describe purpose.

---

# 8. Tagging Standards

Tagging is mandatory.

Every resource must contain required tags.

Tagging enables:

- Cost Allocation
- Ownership Tracking
- Automation
- Governance

---

## 8.1 Mandatory Tags

Every resource must include:

```text
Name

Environment

Owner

Department

Project

ManagedBy

CostCenter

Criticality
```

---

## 8.2 Standard Example

```hcl
tags = {

  Name        = "infraguid-prod-eks"

  Environment = "prod"

  Owner       = "Platform Engineering"

  Department  = "Engineering"

  Project     = "InfraGuid Platform"

  ManagedBy   = "Terraform"

  CostCenter  = "ENG001"

  Criticality = "High"
}
```

---

## 8.3 Environment Tag Values

Allowed:

```text
dev

staging

prod
```

---

## 8.4 Criticality Levels

Allowed:

```text
Low

Medium

High

Critical
```

---

## 8.5 ManagedBy Values

Terraform-managed resources:

```text
ManagedBy=Terraform
```

required.

---

## 8.6 Tag Compliance

Resources missing required tags must be considered non-compliant.

---

# 9. Terraform State Management Standards

Terraform State is one of the most critical assets in the organization.

Loss or corruption of state can result in:

- Resource Drift
- Service Outages
- Infrastructure Recreation
- Data Loss

State management controls are mandatory.

---

## 9.1 State Management Principles

Terraform state must:

```text
Be Centralized

Be Encrypted

Be Backed Up

Be Access Controlled
```

---

## 9.2 Approved Backend

InfraGuid standard:

```text
Amazon S3
```

for state storage.

---

## 9.3 State File Storage

Every environment must use:

```text
Dedicated State Files
```

Example:

```text
prod.tfstate

staging.tfstate

dev.tfstate
```

---

## 9.4 State Isolation

Production state must never be shared.

Each environment requires:

```text
Separate State

Separate Locking

Separate Access Control
```

---

## 9.5 State Security Requirements

State buckets must:

```text
Block Public Access

Enable Versioning

Enable Encryption

Enable Logging
```

---

## 9.6 State Access Controls

Only approved deployment roles may access state.

Direct human access should be minimized.

---

## 9.7 State Backup Requirements

S3 Versioning must be enabled.

This provides:

```text
Rollback

Recovery

Auditability
```

---

## 9.8 Sensitive Data Protection

Sensitive values may exist in state.

Examples:

```text
ARNs

Secrets

Tokens

Passwords
```

State must be treated as sensitive information.

---

## 9.9 State Recovery Procedure

If state corruption occurs:

1. Stop deployments
2. Preserve current state
3. Restore previous version
4. Validate infrastructure
5. Resume deployments

---

# 10. Backend Configuration Standards

All Terraform projects must use approved backend configurations.

---

## 10.1 Standard Backend Architecture

```text
Terraform
      │
      ▼
S3 Backend
      │
      ▼
DynamoDB Locking
```

---

## 10.2 S3 Backend Requirements

Required:

```text
Encryption Enabled

Versioning Enabled

Access Logging Enabled

Private Bucket
```

---

### Example Backend

```hcl
terraform {

  backend "s3" {

    bucket         = "infraguid-prod-tf-state"

    key            = "platform/prod.tfstate"

    region         = "ap-south-1"

    dynamodb_table = "terraform-locks"

    encrypt        = true
  }
}
```

---

## 10.3 State Locking Standards

InfraGuid uses:

```text
DynamoDB State Locking
```

for concurrency protection.

---

### Purpose

Prevent:

```text
Multiple Applies

State Corruption

Race Conditions
```

---

## 10.4 Backend Access Controls

Access should be limited to:

```text
CI/CD Roles

Platform Engineering Roles
```

---

## 10.5 Backend Monitoring

Monitor:

```text
Unauthorized Access

State Changes

Bucket Policy Changes

Locking Failures
```

---

## 10.6 Backend Disaster Recovery

Recovery requirements:

```text
S3 Versioning

Cross Region Backup (Optional)

State Recovery Procedure
```

---

## 10.7 Backend Compliance Review

Backend configurations must be reviewed:

```text
Quarterly

After Security Incidents

After Major Architecture Changes
```

---

## 10.8 Backend Governance

No Terraform deployment may use:

```text
Local State

Shared State Files

Unencrypted Backends
```

in any production environment.

These configurations are considered non-compliant with InfraGuid standards.

# 11. Variable Standards

Variables provide flexibility and reusability within Terraform configurations.

Poor variable design frequently leads to:

- Configuration Errors
- Security Risks
- Operational Complexity
- Unpredictable Deployments

All Terraform variables must follow InfraGuid standards.

---

## 11.1 Variable Design Principles

Variables should be:

```text
Explicit

Validated

Documented

Predictable
```

---

Variables should never rely on:

```text
Hidden Defaults

Undocumented Behavior

Implicit Assumptions
```

---

## 11.2 Required Variable Attributes

Every variable must contain:

```hcl
description

type
```

Example:

```hcl
variable "environment" {

  description = "Deployment environment"

  type = string
}
```

---

## 11.3 Variable Validation

Validation is mandatory for critical variables.

Example:

```hcl
variable "environment" {

  type = string

  validation {

    condition = contains(
      ["dev","staging","prod"],
      var.environment
    )

    error_message = "Invalid environment."
  }
}
```

---

## 11.4 Variable Types

Approved variable types:

```text
string

number

bool

list

map

object
```

---

Avoid:

```text
any
```

unless absolutely necessary.

---

## 11.5 Environment Variables

Environment-specific values should reside in:

```text
terraform.tfvars

dev.tfvars

staging.tfvars

prod.tfvars
```

---

Never hardcode:

```text
CIDRs

Account IDs

Environment Names

Region Values
```

inside reusable modules.

---

## 11.6 Variable Naming Standards

Variable names should be:

```text
Lowercase

Underscore Separated

Descriptive
```

Examples:

```hcl
vpc_cidr

environment

eks_cluster_name
```

Avoid:

```hcl
v

cidr1

test_var
```

---

## 11.7 Sensitive Variables

Sensitive variables must use:

```hcl
sensitive = true
```

Example:

```hcl
variable "db_password" {

  type = string

  sensitive = true
}
```

---

## 11.8 Default Values

Defaults should only be used when:

```text
Safe

Predictable

Environment Independent
```

---

Bad Example:

```hcl
default = "prod"
```

---

Good Example:

```hcl
default = false
```

---

## 11.9 Variable Documentation

Every module README must document:

```text
Variable Name

Description

Type

Required

Default Value
```

---

## 11.10 Variable Governance

Variables should be reviewed during:

```text
Pull Requests

Module Reviews

Architecture Reviews
```

---

# 12. Secrets Management Standards

Secrets management is one of the highest-risk areas within Terraform.

Improper secret handling can result in:

- Credential Leakage
- Production Outages
- Security Incidents
- Regulatory Violations

---

## 12.1 Secret Management Principles

Secrets must never be:

```text
Hardcoded

Stored In Git

Stored In Code

Committed To Repositories
```

---

Secrets must be:

```text
Encrypted

Centralized

Rotated

Audited
```

---

## 12.2 Approved Secret Storage Platforms

InfraGuid approved solutions:

```text
AWS Secrets Manager

AWS Systems Manager Parameter Store
```

---

Preferred:

```text
AWS Secrets Manager
```

for production workloads.

---

## 12.3 Prohibited Practices

The following are prohibited:

```hcl
password = "SuperSecret123"
```

---

```text
Passwords In tfvars

Passwords In Variables

Passwords In Repositories
```

---

## 12.4 Secret Retrieval Pattern

Approved approach:

```hcl
data "aws_secretsmanager_secret_version" "db" {

  secret_id = "prod/database"
}
```

---

Applications should retrieve secrets dynamically.

---

## 12.5 Terraform State Risk

Important:

Terraform state may contain secrets.

Therefore:

```text
State Encryption Required

Access Control Required

Versioning Required
```

---

## 12.6 Secret Rotation

Production secrets must support:

```text
Scheduled Rotation

Emergency Rotation

Incident Response Rotation
```

---

## 12.7 CI/CD Secret Management

Pipelines must retrieve secrets from:

```text
Secrets Manager

Parameter Store
```

---

Secrets must never be injected through:

```text
Git Repositories

Configuration Files

Pull Requests
```

---

## 12.8 Secret Auditing

Review:

```text
Secret Age

Unused Secrets

Excessive Access

Rotation Compliance
```

Quarterly.

---

## 12.9 Emergency Secret Rotation

Trigger rotation when:

```text
Credential Exposure

Employee Departure

Security Incident

Compromised Workload
```

---

## 12.10 Governance

Any hardcoded secret is considered a:

```text
Critical Security Violation
```

requiring immediate remediation.

---

# 13. Provider Standards

Providers define Terraform interaction with external platforms.

InfraGuid primarily uses:

```text
AWS Provider
```

---

## 13.1 Approved Providers

Primary:

```text
hashicorp/aws
```

---

Secondary (when required):

```text
kubernetes

helm

tls

random

archive
```

---

## 13.2 Provider Versioning

All providers must use version constraints.

Example:

```hcl
required_providers {

  aws = {

    source = "hashicorp/aws"

    version = "~> 5.0"
  }
}
```

---

Avoid:

```text
Unpinned Versions
```

---

## 13.3 Region Standards

Regions must be variable driven.

Example:

```hcl
provider "aws" {

  region = var.aws_region
}
```

---

Hardcoded regions prohibited inside modules.

---

## 13.4 Multi-Provider Configurations

Use aliases when required.

Example:

```hcl
provider "aws" {

  alias = "dr"
}
```

---

Common use cases:

```text
Disaster Recovery

Cross Account Deployments

Multi Region Architectures
```

---

## 13.5 Provider Authentication

Approved authentication methods:

```text
IAM Roles

OIDC Federation

AWS Identity Center
```

---

Avoid:

```text
Static Access Keys
```

for production deployments.

---

## 13.6 Provider Governance

Provider upgrades require:

```text
Testing

Validation

Approval
```

before production rollout.

---

# 14. Resource Standards

Terraform resources must follow consistent design principles.

---

## 14.1 Resource Design Principles

Resources should be:

```text
Predictable

Reusable

Secure

Observable
```

---

## 14.2 Resource Ownership

Every resource must have:

```text
Owner

Cost Center

Environment
```

through tags.

---

## 14.3 Resource Lifecycle Management

Use lifecycle controls when appropriate.

Example:

```hcl
lifecycle {

  prevent_destroy = true
}
```

---

Recommended for:

```text
Production Databases

State Buckets

Critical Infrastructure
```

---

## 14.4 Destructive Changes

Destroy operations require:

```text
Approval

Validation

Backup Verification
```

---

## 14.5 Logging Requirements

Resources should enable logging where supported.

Examples:

```text
ALB Access Logs

CloudTrail

VPC Flow Logs

CloudFront Logs
```

---

## 14.6 Encryption Requirements

Encryption must be enabled for:

```text
EBS

RDS

EFS

S3

Secrets
```

---

## 14.7 Monitoring Requirements

Resources must expose metrics.

Examples:

```text
CloudWatch Metrics

CloudWatch Alarms

Dashboards
```

---

## 14.8 Public Exposure Controls

Resources must default to:

```text
Private
```

unless explicitly approved.

---

## 14.9 Resource Governance

Every resource should support:

```text
Monitoring

Backup

Recovery

Auditability
```

---

# 15. Networking Terraform Standards

Networking changes are considered:

```text
High Risk Changes
```

within InfraGuid environments.

---

## 15.1 Networking Principles

Networking configurations must prioritize:

```text
Security

Availability

Simplicity

Auditability
```

---

## 15.2 VPC Standards

Every production VPC must support:

```text
Multi-AZ

Private Subnets

Public Subnets

NAT Gateway

DNS Support
```

---

## 15.3 CIDR Management

CIDRs must be:

```text
Documented

Non Overlapping

Planned For Growth
```

---

Example:

```text
10.0.0.0/16
```

---

## 15.4 Route Table Standards

Every route table must be:

```text
Named

Tagged

Documented
```

---

Changes to:

```text
Route Tables

Associations

Default Routes
```

require enhanced review.

---

## 15.5 Security Group Standards

Security groups should use:

```text
Security Group References
```

instead of:

```text
Wide CIDR Access
```

whenever possible.

---

Bad:

```hcl
0.0.0.0/0
```

---

Preferred:

```hcl
source_security_group_id
```

---

## 15.6 Network ACL Standards

NACLs should remain:

```text
Simple

Documented

Minimal
```

Avoid unnecessary complexity.

---

## 15.7 NAT Gateway Standards

Production workloads:

```text
One NAT Gateway Per AZ
```

recommended.

---

Single NAT gateway architectures require documented approval.

---

## 15.8 VPC Flow Logs

Required:

```text
Production

Shared Services

Security Sensitive Environments
```

---

## 15.9 Internet Gateway Standards

Internet Gateway resources must be:

```text
Tagged

Monitored

Documented
```

---

## 15.10 Networking Validation Checklist

Required before deployment:

```text
CIDR Validation

Route Validation

Security Group Validation

Subnet Validation

NAT Validation
```

---

Required after deployment:

```text
Connectivity Testing

DNS Testing

Internet Access Validation

Application Validation
```

---

## 15.11 Networking Governance

The following require Architect approval:

```text
VPC Changes

CIDR Changes

Route Table Changes

Transit Gateway Changes

Production Security Group Changes
```

because networking incidents have historically represented the highest operational risk category within InfraGuid-managed environments.

# 16. IAM Terraform Standards

Identity and Access Management resources represent one of the highest-risk categories within AWS environments.

Misconfigured IAM resources can result in:

- Privilege Escalation
- Unauthorized Access
- Service Outages
- Security Incidents
- Compliance Violations

All IAM resources managed through Terraform must comply with the standards defined below.

---

## 16.1 IAM Design Principles

IAM configurations must follow:

```text
Least Privilege

Role Based Access

Temporary Credentials

Separation Of Duties

Auditability
```

---

## 16.2 IAM Resource Ownership

Every IAM resource must have:

```text
Owner

Purpose

Environment

Approval Record
```

documented.

---

## 16.3 IAM Roles Preferred Over Users

Production workloads must use:

```text
IAM Roles
```

instead of:

```text
IAM Users
```

whenever possible.

---

Examples:

Preferred:

```text
EC2 Role

EKS Role

GitHub OIDC Role

Lambda Role
```

---

Avoid:

```text
Long-Lived IAM Users
```

---

## 16.4 Least Privilege Requirements

Policies must grant:

```text
Required Access Only
```

---

Avoid:

```json
{
  "Action": "*",
  "Resource": "*"
}
```

except under formally approved exceptions.

---

## 16.5 IAM Policy Structure

Policies should:

```text
Be Modular

Be Reusable

Be Documented
```

---

Example:

```text
s3-read-policy

eks-admin-policy

cloudwatch-read-policy
```

---

## 16.6 Managed Policies vs Inline Policies

Preferred:

```text
Customer Managed Policies
```

---

Avoid excessive use of:

```text
Inline Policies
```

---

## 16.7 Role Assumption Standards

Cross-account access must use:

```text
AssumeRole
```

---

Trust policies must restrict:

```text
Account

Role

Service
```

appropriately.

---

## 16.8 OIDC Standards

Preferred for CI/CD:

```text
GitHub OIDC

Identity Center Federation
```

---

Avoid:

```text
Static AWS Credentials
```

---

## 16.9 Permission Boundary Standards

Permission boundaries required for:

```text
Delegated Administration

Self-Service Platforms

Developer Provisioning
```

---

## 16.10 IAM Change Review Requirements

The following require enhanced review:

```text
Administrator Access

Permission Boundaries

Trust Policies

Cross Account Access
```

---

## 16.11 IAM Monitoring Requirements

Monitor:

```text
Role Changes

Policy Changes

Root Usage

Failed Access Attempts

Privilege Escalation Events
```

---

## 16.12 IAM Governance

All IAM Terraform changes require:

```text
Peer Review

Security Review

Approval
```

before production deployment.

---

# 17. EKS Terraform Standards

Amazon EKS is the strategic Kubernetes platform used by InfraGuid.

EKS deployments must follow standardized patterns.

---

## 17.1 EKS Design Principles

Clusters should be:

```text
Secure

Observable

Scalable

Recoverable
```

---

## 17.2 Cluster Architecture Standards

Production clusters require:

```text
Multi-AZ

Private Nodes

Managed Node Groups

CloudWatch Logging
```

---

## 17.3 Cluster Naming Standards

Format:

```text
infraguid-prod-eks
```

---

## 17.4 Node Group Standards

Separate node groups should exist for:

```text
System Workloads

Application Workloads

AI Workloads
```

where appropriate.

---

## 17.5 Node Sizing Standards

Node sizing should be based on:

```text
CPU

Memory

Pod Density

Workload Type
```

---

## 17.6 Cluster Logging Requirements

Enable:

```text
API Logs

Audit Logs

Authenticator Logs

Controller Logs
```

---

## 17.7 EKS Security Standards

Mandatory:

```text
Private Endpoints

IRSA

RBAC

Encryption
```

---

## 17.8 IRSA Standards

Applications should use:

```text
IAM Roles For Service Accounts
```

---

Avoid:

```text
Node-Wide Permissions
```

---

## 17.9 Add-On Standards

Required:

```text
CoreDNS

VPC CNI

kube-proxy
```

---

Recommended:

```text
AWS Load Balancer Controller

ExternalDNS

Cluster Autoscaler
```

---

## 17.10 EKS Backup Requirements

Production clusters require:

```text
Configuration Backup

ETCD Backup Strategy

Disaster Recovery Documentation
```

---

## 17.11 EKS Monitoring Requirements

Required:

```text
CloudWatch

Prometheus

Grafana
```

or approved equivalent.

---

## 17.12 EKS Governance

Cluster upgrades require:

```text
Testing

Approval

Rollback Plan
```

before production rollout.

---

# 18. RDS Terraform Standards

RDS services frequently host critical business data.

Database infrastructure requires enhanced controls.

---

## 18.1 Database Design Principles

Databases must prioritize:

```text
Availability

Integrity

Recoverability

Security
```

---

## 18.2 Engine Standards

Approved engines:

```text
PostgreSQL

MySQL
```

---

Additional engines require approval.

---

## 18.3 Multi-AZ Requirements

Production databases:

```text
Multi-AZ Required
```

---

Exceptions require documented approval.

---

## 18.4 Backup Requirements

Enable:

```text
Automated Backups

Snapshots

Point-In-Time Recovery
```

---

## 18.5 Encryption Requirements

Mandatory:

```text
Encryption At Rest

Encryption In Transit
```

---

## 18.6 Database Security Groups

Access should be restricted using:

```text
Security Group References
```

---

Avoid:

```text
Open CIDRs
```

---

## 18.7 Monitoring Requirements

Required:

```text
Performance Insights

CloudWatch Metrics

CloudWatch Alarms
```

---

## 18.8 Storage Standards

Storage must support:

```text
Expected Growth

Backup Capacity

Recovery Requirements
```

---

## 18.9 Deletion Protection

Production databases must enable:

```text
Deletion Protection
```

---

## 18.10 Lifecycle Controls

Recommended:

```hcl
prevent_destroy = true
```

for production databases.

---

## 18.11 Database Governance

Database changes require:

```text
Peer Review

Backup Validation

Rollback Plan
```

---

# 19. CI/CD Standards

Terraform deployments should be automated through approved CI/CD platforms.

---

## 19.1 Approved Platforms

Approved:

```text
GitHub Actions

Jenkins
```

---

Additional platforms require approval.

---

## 19.2 Deployment Workflow

Standard workflow:

```text
Code Change
↓
Pull Request
↓
Validation
↓
Plan
↓
Review
↓
Approval
↓
Apply
```

---

## 19.3 Validation Requirements

Every pipeline must execute:

```bash
terraform fmt
```

---

```bash
terraform validate
```

---

```bash
tflint
```

---

## 19.4 Security Scanning

Required:

```text
Checkov

tfsec

Trivy
```

or approved equivalent.

---

## 19.5 Plan Review

Production plans must be reviewed before apply.

Reviewers should validate:

```text
Resource Creation

Resource Modification

Resource Destruction
```

---

## 19.6 Apply Controls

Production apply steps require:

```text
Approval

Audit Trail

Logging
```

---

## 19.7 Emergency Changes

Emergency deployments must follow:

```text
Emergency Change Process
```

defined in Deployment Runbook.

---

## 19.8 Pipeline Authentication

Pipelines must use:

```text
OIDC

Temporary Credentials
```

---

Avoid:

```text
Long Lived Access Keys
```

---

## 19.9 CI/CD Governance

All Terraform deployments must be:

```text
Traceable

Auditable

Reviewable
```

---

# 20. Pull Request Review Standards

Terraform pull requests represent infrastructure changes and must receive rigorous review.

---

## 20.1 Review Objectives

Reviewers should validate:

```text
Correctness

Security

Compliance

Operational Risk
```

---

## 20.2 Mandatory Review Areas

Review:

```text
Resources Added

Resources Modified

Resources Deleted

IAM Changes

Networking Changes
```

---

## 20.3 High-Risk Change Categories

Enhanced review required for:

```text
IAM

VPC

Route Tables

Security Groups

RDS

EKS
```

---

## 20.4 Terraform Plan Review

Reviewers must examine:

```text
Create

Update

Destroy
```

operations.

---

Special attention required for:

```text
Resource Replacement

Data Loss Risk

Downtime Risk
```

---

## 20.5 Destructive Change Review

Any:

```text
Destroy

Replace
```

action requires explicit acknowledgement.

---

## 20.6 Security Review Checklist

Validate:

```text
Least Privilege

Encryption

Logging

Public Access Controls
```

---

## 20.7 Operational Review Checklist

Validate:

```text
Monitoring

Backup

Recovery

Tagging
```

---

## 20.8 Documentation Review

Terraform changes should include:

```text
Documentation Updates

Runbook Updates

Architecture Updates
```

when applicable.

---

## 20.9 Approval Requirements

Production changes require:

```text
Minimum Two Approvals
```

including:

```text
Platform Engineer

Senior Engineer
```

or approved equivalent.

---

## 20.10 PR Governance

No Terraform code may be merged into protected branches without:

```text
Validation Success

Review Completion

Approval Completion
```

All approvals must be recorded and auditable.

# 21. Terraform Deployment Workflow

Terraform deployments must follow a standardized workflow to ensure:

- Consistency
- Auditability
- Security
- Recoverability

All infrastructure deployments performed by InfraGuid must follow the workflow defined in this section.

---

## 21.1 Deployment Objectives

The Terraform deployment process must ensure:

```text
Infrastructure Consistency

Controlled Changes

Risk Reduction

Operational Visibility
```

---

## 21.2 Standard Deployment Lifecycle

All deployments must follow:

```text
Requirements
↓
Code Development
↓
Pull Request
↓
Validation
↓
Plan Review
↓
Approval
↓
Apply
↓
Validation
↓
Monitoring
↓
Closure
```

---

## 21.3 Development Stage

Engineers should:

- Implement required changes
- Follow module standards
- Follow naming standards
- Follow security standards

All changes should remain isolated within feature branches.

---

## 21.4 Pull Request Stage

Terraform changes must be submitted through:

```text
Pull Request
```

No direct commits to protected branches are permitted.

---

## 21.5 Validation Stage

Required validations:

```bash
terraform fmt
```

---

```bash
terraform validate
```

---

```bash
terraform plan
```

---

```bash
tflint
```

---

```bash
checkov
```

---

Validation failures must block deployment.

---

## 21.6 Plan Review Stage

Reviewers must evaluate:

```text
Resources Created

Resources Modified

Resources Destroyed

Resource Replacements

IAM Changes

Networking Changes
```

---

## 21.7 Approval Stage

Required approvals:

### Development

```text
1 Approval
```

---

### Staging

```text
1 Approval
```

---

### Production

```text
2 Approvals
```

minimum.

---

## 21.8 Apply Stage

Terraform applies should be executed through:

```text
CI/CD Pipeline
```

whenever possible.

---

Manual production applies require documented approval.

---

## 21.9 Post Deployment Validation

Required:

```text
Resource Validation

Connectivity Validation

Monitoring Validation

Security Validation
```

---

## 21.10 Deployment Closure

Deployment considered complete only after:

```text
Validation Successful

Monitoring Healthy

Documentation Updated
```

---

# 22. Terraform Validation Checklist

Terraform validation reduces deployment risk.

This checklist must be completed before production deployment.

---

## 22.1 Code Validation

Verify:

```text
✓ terraform fmt Successful

✓ terraform validate Successful

✓ tflint Successful

✓ Security Scan Successful
```

---

## 22.2 Resource Validation

Verify:

```text
✓ Correct Resource Types

✓ Correct Resource Names

✓ Correct Tags

✓ Correct Ownership
```

---

## 22.3 IAM Validation

Verify:

```text
✓ Least Privilege

✓ No Wildcard Permissions

✓ Trust Policies Valid

✓ Cross Account Access Reviewed
```

---

## 22.4 Networking Validation

Verify:

```text
✓ CIDRs Valid

✓ Routes Valid

✓ NAT Configuration Valid

✓ Security Groups Valid
```

---

## 22.5 Database Validation

Verify:

```text
✓ Backup Enabled

✓ Encryption Enabled

✓ Monitoring Enabled

✓ Deletion Protection Enabled
```

---

## 22.6 Kubernetes Validation

Verify:

```text
✓ Logging Enabled

✓ Monitoring Enabled

✓ IRSA Configured

✓ Node Groups Healthy
```

---

## 22.7 Cost Validation

Verify:

```text
✓ Resource Sizing Appropriate

✓ Unnecessary Resources Removed

✓ Cost Impact Reviewed
```

---

## 22.8 Security Validation

Verify:

```text
✓ Encryption Enabled

✓ Public Access Restricted

✓ Logging Enabled

✓ Secrets Managed Correctly
```

---

## 22.9 Operational Validation

Verify:

```text
✓ Monitoring Exists

✓ Alerts Exist

✓ Runbooks Exist

✓ Recovery Procedures Exist
```

---

## 22.10 Production Approval Checklist

Required:

```text
✓ Validation Complete

✓ Plan Reviewed

✓ Security Approved

✓ Rollback Plan Exists

✓ Approvals Recorded
```

---

# 23. Terraform Security Controls

Terraform deployments must implement security controls throughout the infrastructure lifecycle.

---

## 23.1 Security Objectives

Terraform security controls should ensure:

```text
Confidentiality

Integrity

Availability

Auditability
```

---

## 23.2 Infrastructure Security Baselines

All infrastructure should implement:

```text
Encryption

Logging

Monitoring

Least Privilege
```

by default.

---

## 23.3 Secret Protection

Terraform must never contain:

```text
Hardcoded Passwords

Access Keys

Tokens

Certificates
```

---

Approved storage:

```text
AWS Secrets Manager

Parameter Store
```

---

## 23.4 State Security

Terraform state must:

```text
Be Encrypted

Be Versioned

Be Access Controlled
```

---

## 23.5 Security Scanning

Mandatory scans:

```text
Checkov

tfsec

Trivy
```

or approved alternatives.

---

## 23.6 Public Resource Controls

Resources should default to:

```text
Private
```

unless business requirements dictate otherwise.

---

## 23.7 Logging Controls

Enable where applicable:

```text
CloudTrail

ALB Logs

CloudFront Logs

VPC Flow Logs
```

---

## 23.8 IAM Security Controls

Review:

```text
Roles

Policies

Trust Relationships

Permission Boundaries
```

during every deployment.

---

## 23.9 Encryption Standards

Required:

```text
EBS Encryption

RDS Encryption

S3 Encryption

EFS Encryption
```

---

## 23.10 Security Governance

Security violations identified during review must block deployment until resolved.

---

# 24. Drift Management Standards

Configuration drift occurs when infrastructure no longer matches Terraform state.

Drift creates operational risk and must be managed proactively.

---

## 24.1 Drift Definition

Examples:

```text
Manual Console Changes

Manual Security Group Updates

Manual IAM Changes

Manual Route Changes
```

---

## 24.2 Drift Risks

Potential consequences:

```text
Unexpected Deployments

Infrastructure Failure

Security Exposure

Operational Confusion
```

---

## 24.3 Drift Detection Methods

Approved methods:

```text
Terraform Plan

AWS Config

CloudTrail Review

Periodic Audits
```

---

## 24.4 Drift Review Frequency

Production environments:

```text
Monthly
```

minimum.

---

Shared services environments:

```text
Bi-Weekly
```

recommended.

---

## 24.5 Drift Remediation Process

Workflow:

```text
Detect Drift
↓
Investigate Cause
↓
Assess Risk
↓
Remediate
↓
Validate
```

---

## 24.6 Approved Remediation Methods

Option 1:

```text
Update Terraform
```

to reflect intended change.

---

Option 2:

```text
Revert Infrastructure
```

to match Terraform.

---

## 24.7 Unauthorized Changes

Unauthorized manual changes must be:

```text
Documented

Reviewed

Corrected
```

---

## 24.8 Drift Governance

Persistent drift is considered:

```text
Operational Non-Compliance
```

and requires remediation.

---

# 25. Terraform Incident Handling

Terraform-related incidents require structured response procedures.

---

## 25.1 Incident Categories

Examples:

```text
Failed Apply

State Corruption

Accidental Resource Deletion

Drift Related Failure

Provider Failure
```

---

## 25.2 Immediate Response Principles

Priorities:

```text
Protect Production

Preserve State

Assess Impact

Restore Service
```

---

## 25.3 Failed Apply Procedure

Review:

```text
Terraform Logs

Pipeline Logs

CloudTrail Events
```

---

Determine:

```text
Partial Deployment?

Complete Failure?

State Inconsistency?
```

---

## 25.4 State Corruption Procedure

Immediately:

```text
Stop Deployments
```

---

Preserve:

```text
Current State

Previous State Versions

Deployment Evidence
```

---

Recovery:

```text
Restore State

Validate Infrastructure

Resume Deployments
```

---

## 25.5 Accidental Resource Deletion

Required:

```text
Impact Assessment

Recovery Plan

Incident Declaration
```

when production resources are affected.

---

## 25.6 Provider Failure Procedure

Examples:

```text
AWS API Failure

Provider Bug

Authentication Failure
```

---

Validate:

```text
AWS Health

Provider Version

Credentials
```

---

## 25.7 Post Incident Actions

Required:

```text
Root Cause Analysis

Corrective Actions

Preventive Actions

Runbook Updates
```

---

# 26. Governance Statement

This document defines the official Terraform standards used by InfraGuid Technologies Pvt. Ltd.

All Terraform code, modules, repositories, pipelines, and deployments must comply with the standards defined in this document.

The objectives of these standards are to ensure:

```text
Secure Infrastructure

Consistent Deployments

Operational Reliability

Infrastructure Reusability

Regulatory Compliance

Operational Excellence
```

The Platform Engineering Team owns and maintains this document.

All Terraform deployments performed within InfraGuid-managed environments are subject to the controls defined herein.

Exceptions require documented approval from:

```text
Platform Engineering Lead

Solutions Architect

Security Team
```

Non-compliance may result in:

```text
Deployment Rejection

Security Review

Architecture Review

Operational Escalation
```

This document represents the authoritative Terraform governance standard for all InfraGuid-managed cloud environments.