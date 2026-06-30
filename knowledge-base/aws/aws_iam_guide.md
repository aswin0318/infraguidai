# AWS IAM Guide

Document ID: IG-AWS-IAM-001

Version: 1.0

Owner: Rahul Menon

Owner Role: Security Engineering Lead

Department: Security Engineering

Classification: Internal Use Only

Status: Approved

Review Cycle: 12 Months

Last Updated: June 2026

---

# 1. Purpose

This document provides the official Identity and Access Management (IAM) reference guide used by InfraGuid Technologies Pvt. Ltd.

The purpose of this guide is to help engineers understand, design, secure, troubleshoot, and maintain AWS identity and access management architectures.

This guide combines:

```text
AWS IAM Concepts

InfraGuid Security Standards

Terraform Examples

Operational Best Practices

Troubleshooting Procedures
```

to provide a practical IAM reference for engineering teams.

---

# 2. What Is IAM?

AWS Identity and Access Management (IAM) is the service responsible for authentication and authorization within AWS.

IAM determines:

```text
Who Can Access AWS

What They Can Do

Which Resources They Can Access

Under What Conditions
```

---

## Simple Definition

IAM answers two questions:

### Authentication

```text
Who Are You?
```

---

### Authorization

```text
What Are You Allowed To Do?
```

---

## Example

Engineer:

```text
Aswin
```

Attempts:

```text
Delete S3 Bucket
```

IAM evaluates:

```text
Does Aswin Have Permission?
```

---

If:

```text
Allow
```

Operation succeeds.

---

If:

```text
Deny
```

Operation fails.

---

# 3. IAM Components Overview

IAM consists of multiple components.

---

## Core Components

```text
IAM Users

IAM Groups

IAM Roles

IAM Policies

Permission Boundaries

Identity Providers
```

---

## Responsibility Of Each Component

| Component | Purpose |
|------------|----------|
| User | Human Identity |
| Group | User Collection |
| Role | Temporary Identity |
| Policy | Permissions |
| Boundary | Permission Limit |
| Identity Provider | External Authentication |

---

## InfraGuid Standard

Preferred:

```text
Roles
```

Over:

```text
Users
```

for production environments.

---

# 4. IAM Policies

Policies define permissions.

Policies are JSON documents.

---

## Example Policy

```json
{
  "Version": "2012-10-17",

  "Statement": [
    {
      "Effect": "Allow",

      "Action": "s3:GetObject",

      "Resource": "*"
    }
  ]
}
```

---

## Four Critical Elements

### Effect

```text
Allow

Deny
```

---

### Action

```text
What Operation?
```

Example:

```text
s3:GetObject

ec2:StartInstances
```

---

### Resource

```text
What Resource?
```

Example:

```text
Specific Bucket

Specific Role

Specific Instance
```

---

### Condition

```text
When Is Access Allowed?
```

---

# 5. IAM Evaluation Logic

Understanding IAM evaluation is critical.

Most permission issues occur because engineers misunderstand evaluation order.

---

## Simplified Evaluation Process

```text
Request Received
        │
        ▼
Explicit Deny?
        │
   Yes ▼ No
      Deny
        │
        ▼
Allow Exists?
        │
   Yes ▼ No
      Allow
      Deny
```

---

## Most Important Rule

```text
Explicit Deny
Always Wins
```

---

Example:

Policy A:

```text
Allow S3 Access
```

Policy B:

```text
Deny S3 Access
```

Result:

```text
Denied
```

---

# 6. IAM Users

Users represent long-term identities.

---

## Examples

```text
Administrator

Developer

Auditor
```

---

## Why Users Exist

Historically:

```text
Humans Needed AWS Access
```

---

## Modern Best Practice

Avoid creating users whenever possible.

Preferred:

```text
Identity Center

Federation

Roles
```

---

## InfraGuid Standard

Production AWS accounts should minimize IAM user creation.

---

Allowed:

```text
Emergency Break Glass Users
```

only.

---

# 7. IAM Groups

Groups simplify permission management.

---

## Example

```text
Developers Group
```

---

Permissions assigned:

```text
Read CloudWatch

Read S3

Read EC2
```

---

Users inherit permissions from groups.

---

## Benefits

```text
Simpler Administration

Centralized Access Management
```

---

## InfraGuid Standard

When users exist:

```text
Use Groups
```

instead of attaching permissions directly.

---

# 8. IAM Roles

Roles are temporary identities.

Roles are the preferred access mechanism within AWS.

---

## Examples

```text
EC2 Role

Lambda Role

EKS Role

GitHub Role
```

---

## Why Roles Are Better

Benefits:

```text
Temporary Credentials

Automatic Rotation

Improved Security
```

---

No long-lived secrets required.

---

## Example

EC2 Instance:

```text
Needs S3 Access
```

---

Bad:

```text
Store AWS Keys
```

---

Good:

```text
Attach IAM Role
```

---

## InfraGuid Standard

Production workloads must use:

```text
IAM Roles
```

---

# 9. Role Assumption

Roles become useful through:

```text
AssumeRole
```

---

## Concept

Identity:

```text
User

Application

AWS Service
```

temporarily becomes:

```text
Role
```

---

## Example

```text
Developer

↓

AssumeRole

↓

Production ReadOnly Role
```

---

## Benefits

```text
Temporary Access

Reduced Risk

Auditability
```

---

# 10. Trust Policies

Trust policies determine:

```text
Who Can Assume A Role
```

---

Example:

```json
{
  "Effect": "Allow",

  "Principal": {
    "Service": "ec2.amazonaws.com"
  },

  "Action": "sts:AssumeRole"
}
```

---

Meaning:

```text
EC2 Can Assume This Role
```

---

## Two Policies Required

For access:

### Trust Policy

```text
Who Can Assume
```

---

### Permission Policy

```text
What Can Be Done
```

---

Both are required.

# 11. Cross-Account Access

Modern AWS environments frequently use multiple AWS accounts.

Cross-account access allows identities in one account to access resources in another account securely.

---

## 11.1 Why Cross-Account Access Exists

Typical InfraGuid architecture:

```text
Development Account

Staging Account

Production Account

Shared Services Account

Security Account
```

---

Engineers often need:

```text
Access Across Accounts
```

without maintaining separate credentials.

---

## 11.2 Cross-Account Access Architecture

Example:

```text
Engineer

↓

Development Account

↓

AssumeRole

↓

Production ReadOnly Role

↓

Production Resources
```

---

## 11.3 Cross-Account Access Components

Required:

### Source Identity

```text
User

Role

Federated Identity
```

---

### Target Role

```text
IAM Role
```

in destination account.

---

### Trust Policy

Allows assumption.

---

### Permission Policy

Defines allowed actions.

---

## 11.4 Example Trust Policy

Production Role:

```json
{
  "Version": "2012-10-17",

  "Statement": [
    {
      "Effect": "Allow",

      "Principal": {
        "AWS": "arn:aws:iam::111111111111:root"
      },

      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

Meaning:

```text
Account 111111111111
Can Assume This Role
```

---

## 11.5 Benefits

```text
No Credential Sharing

Centralized Access

Improved Auditability

Reduced Risk
```

---

## 11.6 InfraGuid Standard

Cross-account access must use:

```text
IAM Roles

STS AssumeRole
```

---

Never:

```text
Share Access Keys

Create Duplicate Users
```

---

# 12. Permission Boundaries

Permission Boundaries define:

```text
Maximum Allowed Permissions
```

for an identity.

---

## 12.1 Why Boundaries Exist

Without boundaries:

```text
Developer Creates Role

↓

Attaches AdministratorAccess

↓

Privilege Escalation
```

---

Permission boundaries prevent this.

---

## 12.2 Evaluation Logic

Effective permissions are:

```text
Permission Policy

INTERSECT

Permission Boundary
```

---

Example:

Role Policy:

```text
AdministratorAccess
```

Boundary:

```text
S3 Only
```

Result:

```text
S3 Only
```

---

## 12.3 Common Use Cases

### Self-Service Infrastructure

Developers create resources.

Cannot exceed approved permissions.

---

### Platform Engineering

Delegated administration.

---

### Multi-Team Environments

Controlled privilege management.

---

## 12.4 Common Failure Scenario

Observed in:

```text
RCA-005
```

Issue:

```text
Permission Boundary

↓

Blocked Deployment Actions

↓

Pipeline Failure
```

---

## Investigation Checklist

Verify:

```text
Role Policy

Permission Boundary

SCP

Trust Policy
```

---

## 12.5 InfraGuid Standard

Permission boundaries required for:

```text
Developer Managed Roles

Self-Service Platforms

Delegated Administration
```

---

# 13. IAM Identity Center

IAM Identity Center (formerly AWS SSO) is the preferred authentication mechanism for human access.

---

## 13.1 Why Identity Center

Traditional model:

```text
IAM Users

Passwords

MFA
```

---

Modern model:

```text
Corporate Identity Provider

↓

IAM Identity Center

↓

AWS Accounts
```

---

## 13.2 Benefits

```text
Centralized Access

MFA Enforcement

Reduced IAM Users

Simplified Management
```

---

## 13.3 User Flow

```text
Engineer

↓

Identity Center

↓

Assigned Permission Set

↓

AWS Account Access
```

---

## 13.4 Permission Sets

Permission Sets define:

```text
AWS Permissions
```

---

Examples:

```text
ReadOnly

Developer

PlatformAdmin

SecurityAuditor
```

---

## 13.5 InfraGuid Standard

Human access should use:

```text
IAM Identity Center
```

---

Avoid:

```text
Direct IAM Users
```

for routine access.

---

# 14. OIDC Federation

OIDC allows external systems to authenticate into AWS without long-lived credentials.

---

## 14.1 Why OIDC Matters

Old Model:

```text
AWS Access Keys

↓

Stored In CI/CD
```

---

Problems:

```text
Credential Leakage

Rotation Complexity

Security Risk
```

---

New Model:

```text
OIDC

↓

Temporary Credentials

↓

No Stored Secrets
```

---

## 14.2 OIDC Authentication Flow

```text
GitHub

↓

OIDC Token

↓

AWS STS

↓

Temporary Credentials

↓

AWS Resources
```

---

## 14.3 Benefits

```text
No Long-Lived Keys

Automatic Rotation

Improved Security

Improved Auditability
```

---

## 14.4 Supported Providers

Examples:

```text
GitHub

GitLab

Azure AD

Google
```

---

## 14.5 InfraGuid Standard

CI/CD pipelines should use:

```text
OIDC Federation
```

whenever supported.

---

# 15. GitHub Actions Authentication

GitHub Actions is the primary CI/CD platform used by InfraGuid.

---

## 15.1 Legacy Approach

```text
GitHub Secret

↓

AWS Access Key

↓

AWS Access
```

---

Problems:

```text
Secret Management

Credential Rotation

Security Exposure
```

---

## 15.2 Modern Approach

```text
GitHub Workflow

↓

OIDC Token

↓

AWS Role

↓

Temporary Credentials
```

---

## 15.3 Architecture

```text
GitHub Actions

↓

OIDC Provider

↓

STS AssumeRoleWithWebIdentity

↓

Deployment Role

↓

AWS Resources
```

---

## 15.4 Benefits

```text
No Secrets

Automatic Rotation

Improved Security

Least Privilege
```

---

## 15.5 InfraGuid Standard

Production deployment pipelines must use:

```text
OIDC Authentication
```

---

Avoid:

```text
Static AWS Keys
```

---

# 16. IAM Security Best Practices

IAM is one of the most critical security domains within AWS.

Misconfigured IAM often leads to:

```text
Privilege Escalation

Unauthorized Access

Data Exposure
```

---

## 16.1 Least Privilege

Grant:

```text
Required Access Only
```

---

Avoid:

```text
AdministratorAccess
```

unless justified.

---

## 16.2 Role-Based Access

Preferred:

```text
Roles
```

Over:

```text
Users
```

---

## 16.3 MFA Enforcement

Required for:

```text
Administrators

Platform Engineers

Security Engineers
```

---

## 16.4 Temporary Credentials

Preferred:

```text
STS

Identity Center

OIDC
```

---

Avoid:

```text
Long-Lived Keys
```

---

## 16.5 Permission Reviews

Review:

```text
Roles

Policies

Users

Groups
```

quarterly.

---

## 16.6 Access Key Management

If access keys exist:

```text
Rotate Regularly

Monitor Usage

Remove Unused Keys
```

---

## 16.7 Logging Requirements

Enable:

```text
CloudTrail

IAM Event Monitoring

Security Alerting
```

---

## 16.8 Privilege Escalation Protection

Review:

```text
iam:PassRole

iam:CreateRole

iam:AttachRolePolicy
```

carefully.

---

## 16.9 Root Account Protection

Root account should:

```text
Enable MFA

Have No Access Keys

Be Rarely Used
```

---

## 16.10 InfraGuid Security Standard

All IAM implementations must follow:

```text
Least Privilege

Temporary Credentials

MFA

Role-Based Access
```

as mandatory security requirements.

# 17. Service Control Policies (SCPs)

Service Control Policies (SCPs) are AWS Organizations policies used to define the maximum permissions available within AWS accounts.

SCPs do not grant permissions.

They only:

```text
Allow

Or

Restrict
```

what accounts may ultimately do.

---

## 17.1 Why SCPs Exist

Without SCPs:

```text
Account Administrator

↓

Can Grant Any Permission
```

---

With SCPs:

```text
Organization

↓

Defines Maximum Allowed Permissions
```

---

This provides centralized governance.

---

## 17.2 SCP Evaluation Model

Permissions are granted only if:

```text
SCP Allows

AND

IAM Allows
```

---

Example:

IAM Policy:

```text
Allow EC2
```

SCP:

```text
Deny EC2
```

Result:

```text
Denied
```

---

## 17.3 SCP Hierarchy

Applied at:

```text
Organization

↓

Organizational Unit

↓

Account
```

---

Inherited downward.

---

## Example

```text
Root

↓

Production OU

↓

Prod Account
```

---

Account inherits OU SCPs.

---

## 17.4 Common SCP Use Cases

### Prevent Root Usage

### Restrict Regions

### Restrict Services

### Block IAM Escalation

### Prevent Resource Deletion

---

## Example

Deny:

```json
{
  "Effect": "Deny",

  "Action": [
    "iam:*"
  ],

  "Resource": "*"
}
```

---

## 17.5 Region Restriction Example

Allow only:

```text
ap-south-1

us-east-1
```

---

Block:

```text
All Other Regions
```

---

## 17.6 Common Failure Scenario

Symptoms:

```text
Administrator

↓

AccessDenied
```

even with:

```text
AdministratorAccess
```

---

Root Cause:

```text
SCP Deny
```

---

## Investigation Checklist

Verify:

```text
IAM Policy

Permission Boundary

SCP

Session Policy
```

---

## 17.7 InfraGuid SCP Standards

Mandatory controls:

```text
Root Protection

Region Restrictions

Security Service Protection

CloudTrail Protection
```

---

# 18. IAM Troubleshooting Guide

IAM issues are among the most common AWS operational problems.

This section provides a structured troubleshooting methodology.

---

# 18.1 Troubleshooting Workflow

Always investigate in this order:

```text
Authentication

↓

Authorization

↓

Policy Evaluation

↓

Organizations

↓

Resource Policies
```

---

# 18.2 Step 1

Who Is Making The Request?

Verify:

```text
IAM User

IAM Role

Federated Identity

GitHub OIDC

Lambda Role

EC2 Role
```

---

Useful Command:

```bash
aws sts get-caller-identity
```

---

Output:

```text
Account

ARN

User ID
```

---

# 18.3 Step 2

Is Authentication Successful?

Check:

```text
MFA

Credentials

OIDC Token

Role Assumption
```

---

# 18.4 Step 3

Check IAM Policies

Review:

```text
Attached Policies

Inline Policies

Group Policies
```

---

Question:

```text
Does Allow Exist?
```

---

# 18.5 Step 4

Check Explicit Deny

Remember:

```text
Explicit Deny

Always Wins
```

---

Common locations:

```text
IAM Policy

Boundary

SCP

Resource Policy
```

---

# 18.6 Step 5

Check Permission Boundary

Verify:

```text
Role Boundary

User Boundary
```

---

Common symptom:

```text
Policy Looks Correct

Still AccessDenied
```

---

# 18.7 Step 6

Check SCP

Verify:

```text
Organization Policies
```

---

Particularly for:

```text
Production Accounts
```

---

# 18.8 Step 7

Check Resource Policies

Examples:

```text
S3 Bucket Policy

KMS Key Policy

Secrets Manager Policy
```

---

Access may be denied even if IAM permissions appear correct.

---

# 18.9 Step 8

Use Policy Simulator

AWS IAM Policy Simulator helps validate:

```text
Allowed Actions

Denied Actions

Evaluation Logic
```

---

# 18.10 Step 9

Review CloudTrail

Investigate:

```text
Event History

Denied Requests

Identity Used
```

---

CloudTrail often provides the fastest root cause.

---

# 19. Terraform IAM Examples

This section provides IAM patterns approved by InfraGuid.

---

# 19.1 IAM Role

```hcl
resource "aws_iam_role" "app_role" {

  name = "app-role"

  assume_role_policy =
    data.aws_iam_policy_document.app_trust.json
}
```

---

# 19.2 Trust Policy

```hcl
data "aws_iam_policy_document" "app_trust" {

  statement {

    actions = [
      "sts:AssumeRole"
    ]

    principals {

      type = "Service"

      identifiers = [
        "ec2.amazonaws.com"
      ]
    }
  }
}
```

---

Purpose:

```text
Allow EC2 To Assume Role
```

---

# 19.3 IAM Policy

```hcl
resource "aws_iam_policy" "s3_read" {

  name = "s3-read"

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {

        Effect = "Allow"

        Action = [

          "s3:GetObject"
        ]

        Resource = "*"
      }
    ]
  })
}
```

---

# 19.4 Attach Policy To Role

```hcl
resource "aws_iam_role_policy_attachment" "attach" {

  role =
    aws_iam_role.app_role.name

  policy_arn =
    aws_iam_policy.s3_read.arn
}
```

---

# 19.5 EC2 Instance Profile

```hcl
resource "aws_iam_instance_profile" "app" {

  name = "app-profile"

  role = aws_iam_role.app_role.name
}
```

---

Purpose:

```text
Attach Role To EC2
```

---

# 19.6 GitHub OIDC Provider

```hcl
resource "aws_iam_openid_connect_provider" "github" {

  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    "xxxxxxxxxxxxxxxx"
  ]
}
```

---

# 19.7 OIDC Role Example

Allows:

```text
GitHub Actions

↓

Assume AWS Role
```

without access keys.

---

# 20. Common AccessDenied Scenarios

This section documents frequently encountered IAM incidents.

---

# Scenario 1

Administrator AccessDenied

---

## Symptoms

```text
Admin User

↓

AccessDenied
```

---

## Likely Cause

```text
SCP Deny
```

---

## Investigation

Check:

```text
Organizations

SCPs
```

---

# Scenario 2

EC2 Cannot Access S3

---

## Symptoms

```text
403 Forbidden
```

---

## Checklist

```text
Role Attached

Policy Attached

Bucket Policy

KMS Permissions
```

---

## Common Root Cause

```text
Missing IAM Role
```

---

# Scenario 3

Lambda Cannot Access Secrets Manager

---

## Checklist

Verify:

```text
Execution Role

Secrets Permission

KMS Access
```

---

## Common Root Cause

```text
Missing kms:Decrypt
```

---

# Scenario 4

GitHub Deployment Fails

---

## Symptoms

```text
AssumeRole Failure
```

---

## Checklist

Verify:

```text
OIDC Provider

Trust Policy

Repository Conditions

Role ARN
```

---

## Common Root Cause

```text
Incorrect Subject Claim
```

---

# Scenario 5

Role Assumption Failure

---

## Symptoms

```text
sts:AssumeRole

Denied
```

---

## Common Causes

```text
Trust Policy Missing

Wrong Principal

Cross Account Misconfiguration
```

---

# Scenario 6

KMS Access Denied

---

## Symptoms

```text
Decrypt Failure
```

---

## Common Cause

```text
IAM Allows

KMS Policy Denies
```

---

Remember:

```text
KMS Has Its Own Policy Layer
```

---

# 21. Best Practices

The following best practices apply to all InfraGuid-managed AWS environments.

---

## Authentication

Use:

```text
Identity Center
```

for human access.

---

Avoid:

```text
Long Lived IAM Users
```

---

## Authorization

Implement:

```text
Least Privilege
```

everywhere.

---

## Roles

Prefer:

```text
IAM Roles
```

over users.

---

## Federation

Use:

```text
OIDC

Identity Center

STS
```

for temporary credentials.

---

## Reviews

Review:

```text
Roles

Policies

Permissions
```

quarterly.

---

## Monitoring

Enable:

```text
CloudTrail

Security Hub

IAM Access Analyzer
```

---

## Root User

Required:

```text
MFA Enabled

No Access Keys

No Daily Usage
```

---

## Cross Account Access

Use:

```text
AssumeRole
```

Never:

```text
Shared Credentials
```

---

## CI/CD

Use:

```text
OIDC Authentication
```

Never:

```text
Static AWS Keys
```

---

# 22. Governance Statement

This document defines the official IAM standards, implementation patterns, and access control guidance used by InfraGuid Technologies Pvt. Ltd.

All AWS identities, authentication mechanisms, authorization controls, IAM roles, IAM policies, federated access configurations, and CI/CD authentication methods must align with the standards defined within this guide.

The objectives of this document are:

```text
Secure Authentication

Least Privilege Access

Operational Consistency

Regulatory Compliance

Identity Governance
```

The Security Engineering Team owns and maintains this document.

Platform Engineering is responsible for implementation and operational compliance.

Architecture is responsible for access model design and review.

Exceptions require approval from:

```text
Security Engineering Lead

Solutions Architect

CTO
```

This document serves as the authoritative IAM reference for all InfraGuid-managed AWS environments.

