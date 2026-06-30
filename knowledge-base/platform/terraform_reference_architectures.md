# Terraform Reference Architectures

Document ID: IG-TF-ARCH-001

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

This document defines the approved Terraform reference architectures used by InfraGuid Technologies Pvt. Ltd.

The purpose of this document is to provide production-proven infrastructure blueprints that can be reused across multiple projects and environments.

Unlike individual AWS service guides, this document focuses on how infrastructure components are combined to create complete enterprise-grade platforms.

This document serves as the primary reference for:

```text
Platform Engineers

Cloud Engineers

DevOps Engineers

Solutions Architects

Security Engineers

AI Assistants
```

The architectures contained in this document have been selected because they represent the most common deployment patterns used within modern AWS environments.

---

# 2. Objectives

The objectives of this document are:

```text
Standardize Infrastructure Design

Reduce Architecture Drift

Improve Terraform Reusability

Accelerate Project Delivery

Enforce Security Standards

Improve AI Terraform Generation Quality
```

---

# 3. Architecture Design Principles

All reference architectures must follow the principles below.

---

## Security First

Infrastructure must be designed assuming:

```text
Public Networks Are Untrusted

Credentials Can Be Compromised

Applications Will Be Attacked
```

Security controls must be implemented at:

```text
Network Layer

Identity Layer

Application Layer

Data Layer
```

---

## Infrastructure As Code

All infrastructure must be:

```text
Terraform Managed

Version Controlled

Reviewable

Repeatable
```

Manual resource creation is discouraged.

---

## Multi-AZ Design

Production workloads must survive:

```text
Single Availability Zone Failure
```

Therefore production architectures should use:

```text
Multiple Availability Zones
```

whenever supported by AWS services.

---

## Least Privilege

Access permissions should follow:

```text
Minimum Required Access
```

at all times.

---

## Observability By Default

Every architecture should include:

```text
Metrics

Logs

Dashboards

Alerts
```

from the beginning.

---

## Cost Awareness

Infrastructure should be designed with:

```text
Scalability

Performance

Cost
```

in balance.

---

# 4. Architecture Selection Framework

Selecting the correct architecture is more important than selecting individual AWS services.

The following process should be used when designing infrastructure.

---

## Step 1

Determine Application Type.

Examples:

```text
Web Application

API

Kubernetes Platform

AI Assistant

Static Website

SaaS Product
```

---

## Step 2

Determine Scale.

Examples:

```text
Internal Team

Department

Entire Organization

External Customers
```

---

## Step 3

Determine Availability Requirements.

Examples:

```text
Development

Non-Critical Production

Business Critical

Mission Critical
```

---

## Step 4

Determine Compliance Requirements.

Examples:

```text
Internal Only

Customer Data

Financial Data

Regulated Workloads
```

---

## Step 5

Select Closest Reference Architecture.

Architectures should be adapted rather than built from scratch.

---

# Architecture 1

# Production Three-Tier Application

---

# Purpose

This architecture represents the standard enterprise web application deployment pattern.

It separates infrastructure into three logical layers:

```text
Presentation Layer

Application Layer

Data Layer
```

This design improves:

```text
Security

Scalability

Maintainability

Availability
```

---

# Typical Use Cases

Examples include:

```text
Customer Portals

Employee Portals

Enterprise Dashboards

Business Applications

Management Systems

ERP Platforms

CRM Platforms
```

---

# When To Use

Use this architecture when:

```text
Users Access Application Through Browser

Relational Database Required

High Availability Required

Application Logic Runs Continuously
```

---

# When Not To Use

Avoid this architecture when:

```text
Workload Is Serverless

Static Website Only

Simple Landing Page

Event Driven Processing
```

---

# Reference Architecture

```text
Users

↓

CloudFront

↓

AWS WAF

↓

Application Load Balancer

↓

EKS Cluster

↓

RDS PostgreSQL

↓

Backups
```

---

# Module Composition

```hcl
module "vpc"

module "alb"

module "eks"

module "rds"

module "backup"

module "monitoring"

module "logging"

module "waf"

module "cloudfront"
```

---

# Networking Design

---

## VPC

Single VPC.

Recommended CIDR:

```text
10.0.0.0/16
```

---

## Public Subnets

Used for:

```text
ALB

NAT Gateway
```

---

## Private Application Subnets

Used for:

```text
EKS Worker Nodes

Application Pods
```

---

## Private Database Subnets

Used for:

```text
RDS

Database Services
```

---

## Availability Zones

Minimum:

```text
2 AZs
```

Recommended:

```text
3 AZs
```

---

# Security Design

---

## Edge Security

Traffic enters through:

```text
CloudFront
```

Protected by:

```text
AWS WAF
```

---

## Network Security

Security groups enforce:

```text
CloudFront → ALB

ALB → EKS

EKS → RDS
```

communication paths.

---

## Database Security

Database access allowed from:

```text
Application Security Groups
```

only.

---

Database should never be publicly accessible.

---

## Encryption

Mandatory:

```text
RDS Encryption

EBS Encryption

Secrets Encryption

Backup Encryption
```

---

# IAM Design

---

## EKS

Use:

```text
IRSA
```

for workload permissions.

---

Avoid:

```text
Node-Wide Permissions
```

---

## CI/CD

Use:

```text
OIDC Authentication
```

for GitHub Actions.

---

## Database Access

Applications retrieve credentials from:

```text
Secrets Manager
```

---

# Monitoring Design

---

## Metrics

Monitor:

```text
CPU

Memory

Disk

Network

Application Latency

HTTP Error Rate
```

---

## Dashboards

Required dashboards:

```text
Platform Dashboard

Application Dashboard

Database Dashboard
```

---

## Alerts

Required alerts:

```text
High CPU

Database Failure

Pod CrashLoop

High Error Rate

High Latency
```

---

# Logging Design

---

Centralized logging required.

Sources:

```text
Application Logs

EKS Logs

ALB Logs

CloudFront Logs
```

---

Retention:

```text
90 Days Minimum
```

---

# Backup Design

---

RDS:

```text
30 Day Retention
```

---

EBS:

```text
AWS Backup
```

---

Secrets:

```text
Versioned Storage
```

---

# Cost Considerations

Largest cost drivers:

```text
EKS Nodes

RDS

NAT Gateway

CloudFront Traffic
```

---

Optimization Strategies:

```text
Right Size Nodes

Reserved Instances

Graviton Instances

Efficient Autoscaling
```

---

# Common Failure Scenarios

---

## Scenario 1

```text
ALB Returns 502
```

Possible Causes:

```text
Pod Failure

Target Group Failure

Application Crash
```

---

## Scenario 2

```text
Database Connection Failure
```

Possible Causes:

```text
Security Group

Credential Rotation

Database Failure
```

---

## Scenario 3

```text
High Latency
```

Possible Causes:

```text
Database Bottleneck

Node Saturation

Application Issues
```

---

# Production Checklist

```text
✓ Multi-AZ

✓ Private Database

✓ WAF Enabled

✓ Monitoring Enabled

✓ Logging Enabled

✓ Backups Enabled

✓ OIDC Enabled

✓ IRSA Enabled

✓ Encryption Enabled
```

---

# Related Documents

```text
aws_vpc_guide.md

aws_iam_guide.md

aws_cloudfront_guide.md

terraform_module_catalog.md

terraform_aws_provider_guide.md
```

---

# Architecture 2

# Production EKS Platform

---

# Purpose

This architecture provides a standardized Kubernetes platform for hosting multiple containerized workloads.

It is intended to serve as the primary platform for:

```text
Microservices

Internal Applications

APIs

Platform Services

Developer Platforms
```

within InfraGuid-managed environments.

---

# Typical Use Cases

```text
Container Platforms

Microservices

GitOps Platforms

Internal Developer Platforms

Enterprise Applications
```

---

# When To Use

Use this architecture when:

```text
Multiple Services Exist

Container Workloads Required

Kubernetes Skills Available

Platform Standardization Needed
```

---

# When Not To Use

Avoid when:

```text
Single Small Application

Simple Website

Serverless Workload

Low Operational Maturity
```

---

# Reference Architecture

```text
GitHub Actions

↓

OIDC

↓

Amazon ECR

↓

Amazon EKS

↓

IRSA

↓

AWS Services
```

---

# Module Composition

```hcl
module "vpc"

module "eks"

module "ecr"

module "irsa"

module "monitoring"

module "logging"

module "vpc-endpoints"
```

---

# Core Platform Components

```text
EKS Control Plane

Managed Node Groups

OIDC Provider

IRSA

ECR

CloudWatch

AWS Load Balancer Controller

Metrics Server
```

---

# Networking Design

Production EKS clusters must be deployed in:

```text
Private Subnets
```

---

Worker Nodes:

```text
Private Subnets
```

---

Ingress Traffic:

```text
ALB
```

---

Outbound Internet:

```text
NAT Gateway
```

---

VPC Endpoints Recommended:

```text
S3

ECR

CloudWatch

SSM

Secrets Manager
```

---

# Security Design

Mandatory:

```text
Private Nodes

IRSA

OIDC

Security Groups

Network Policies
```

---

Cluster API endpoint:

```text
Private Preferred

Public Restricted
```

---

# IAM Design

Use:

```text
IRSA
```

for all workloads requiring AWS access.

---

Examples:

```text
External DNS

ALB Controller

EBS CSI Driver

Application Pods
```

---

Avoid:

```text
Using Node Role Permissions
```

for applications.

---

# Monitoring Design

Mandatory:

```text
Cluster Metrics

Node Metrics

Pod Metrics

API Server Metrics
```

---

Key Alerts:

```text
Node Not Ready

Pod CrashLoopBackOff

High Memory

High CPU

Disk Pressure
```

---

# Architecture 2 (Continued)

# Logging Design

All cluster logs must be centralized.

Sources:

```text
Control Plane Logs

Application Logs

Node Logs

Ingress Logs
```

---

Recommended retention:

```text
90 Days
```

minimum.

---

Production environments should enable:

```text
API Server Logs

Audit Logs

Scheduler Logs

Controller Manager Logs
```

---

# Backup Design

Kubernetes workloads require backup strategies beyond EC2 backups.

---

## Cluster Configuration

Store:

```text
Terraform State

Git Repositories

Helm Charts
```

in version-controlled repositories.

---

## Persistent Volumes

Backup:

```text
EBS Volumes

EFS Volumes
```

using AWS Backup.

---

## Critical Data

Database backups remain the responsibility of:

```text
RDS

Aurora

External Database Systems
```

---

# Cost Considerations

Largest cost drivers:

```text
Worker Nodes

Load Balancers

NAT Gateways

CloudWatch Logs
```

---

Optimization recommendations:

```text
Cluster Autoscaler

Karpenter

Graviton Nodes

Spot Instances

Right-Sized Node Groups
```

---

# Common Failure Scenarios

---

## Scenario 1

```text
Pod CrashLoopBackOff
```

Possible Causes:

```text
Application Bug

Missing Secret

Configuration Error

Database Connectivity Issue
```

---

## Scenario 2

```text
Pods Stuck Pending
```

Possible Causes:

```text
Insufficient CPU

Insufficient Memory

Node Group Scaling Issue

PVC Problems
```

---

## Scenario 3

```text
Service Unreachable
```

Possible Causes:

```text
Ingress Misconfiguration

Service Misconfiguration

Security Group Issue

DNS Issue
```

---

## Scenario 4

```text
IRSA Not Working
```

Possible Causes:

```text
Incorrect Trust Policy

Missing OIDC Provider

Wrong Service Account Annotation
```

---

# Production Checklist

```text
✓ Multi-AZ

✓ Managed Node Groups

✓ OIDC Enabled

✓ IRSA Enabled

✓ Monitoring Enabled

✓ Logging Enabled

✓ VPC Endpoints Enabled

✓ Cluster Autoscaling Enabled

✓ Backup Strategy Defined
```

---

# Related Documents

```text
kubernetes_guide.md

aws_iam_guide.md

aws_vpc_guide.md

terraform_module_catalog.md
```

---

# Architecture 3

# Production SaaS Platform

---

# Purpose

This architecture represents the standard deployment model for customer-facing SaaS applications.

The architecture is designed to provide:

```text
High Availability

Horizontal Scalability

Security

Global Performance

Operational Visibility
```

for internet-facing production systems.

---

# Typical Use Cases

```text
B2B SaaS Platforms

Customer Portals

Subscription Platforms

Enterprise Products

Multi-Tenant Applications
```

---

# Business Objectives

The architecture must support:

```text
Thousands Of Users

Multiple Customers

Rapid Scaling

Continuous Deployment

Zero Downtime Releases
```

---

# When To Use

Use this architecture when:

```text
Application Serves External Customers

Multi-Tenant Design Required

Relational Database Required

High Availability Required

Customer Data Stored
```

---

# When Not To Use

Avoid when:

```text
Simple Internal Application

Static Website

Single-Team Tool

Prototype Environment
```

---

# Reference Architecture

```text
Users

↓

Route53

↓

CloudFront

↓

AWS WAF

↓

Application Load Balancer

↓

Amazon EKS

↓

Redis

↓

PostgreSQL

↓

Backups
```

---

# Module Composition

```hcl
module "vpc"

module "cloudfront"

module "waf"

module "alb"

module "eks"

module "rds"

module "elasticache"

module "backup"

module "monitoring"

module "logging"

module "route53"

module "acm"

module "secrets-manager"
```

---

# High Level Architecture

The platform consists of:

```text
Edge Layer

Application Layer

Caching Layer

Data Layer

Observability Layer
```

---

## Edge Layer

Components:

```text
Route53

CloudFront

WAF
```

Responsibilities:

```text
DNS

TLS

Caching

DDoS Protection

Request Filtering
```

---

## Application Layer

Components:

```text
ALB

EKS

Microservices
```

Responsibilities:

```text
Business Logic

Authentication

Authorization

API Processing
```

---

## Caching Layer

Components:

```text
Redis
```

Responsibilities:

```text
Session Storage

Application Cache

Rate Limiting

Frequently Accessed Data
```

---

## Data Layer

Components:

```text
PostgreSQL

Backups
```

Responsibilities:

```text
Persistent Data

Transactions

Customer Records
```

---

# Networking Design

---

## VPC Design

Recommended CIDR:

```text
10.0.0.0/16
```

---

## Public Subnets

Used for:

```text
ALB

NAT Gateway
```

---

## Private Application Subnets

Used for:

```text
EKS Worker Nodes

Application Pods
```

---

## Private Database Subnets

Used for:

```text
RDS

Redis
```

---

## Availability Zones

Minimum:

```text
3 AZs
```

for production SaaS.

---

# Security Design

---

## Edge Security

Requests pass through:

```text
CloudFront

↓

WAF
```

before reaching the application.

---

## Application Security

Authentication mechanisms:

```text
OIDC

OAuth2

SAML
```

depending on business requirements.

---

## Secrets Management

All secrets stored in:

```text
AWS Secrets Manager
```

---

Never:

```text
Hardcode Credentials
```

---

## Database Security

Access restricted to:

```text
Application Security Groups
```

only.

---

Public access:

```text
Disabled
```

---

## Encryption Requirements

Mandatory:

```text
TLS

RDS Encryption

Redis Encryption

EBS Encryption

Secrets Encryption
```

---

# IAM Design

---

## CI/CD

Use:

```text
GitHub OIDC
```

---

## EKS

Use:

```text
IRSA
```

for workload permissions.

---

## Administrative Access

Use:

```text
IAM Identity Center
```

---

Avoid:

```text
Long-Lived IAM Users
```

---

# Observability Design

Production SaaS platforms require deep observability.

---

## Metrics

Track:

```text
Requests Per Second

Latency

Error Rate

Database Connections

Cache Hit Ratio

CPU

Memory
```

---

## Business Metrics

Track:

```text
Active Users

Customer Usage

Subscription Activity

Feature Usage
```

---

## Alerting

Mandatory alerts:

```text
High Error Rate

Database Failure

Redis Failure

Pod CrashLoop

Certificate Expiration

Latency Spike
```

---

# Logging Design

Sources:

```text
Application Logs

Audit Logs

ALB Logs

CloudFront Logs

WAF Logs

Database Logs
```

---

Retention:

```text
90 Days Minimum

365 Days Preferred
```

for customer-facing platforms.

---

# Backup Design

RDS:

```text
30 Day Retention
```

---

Redis:

```text
Snapshots Enabled
```

---

Secrets:

```text
Versioned
```

---

Terraform State:

```text
Remote Backup
```

---

# Cost Considerations

Largest SaaS cost drivers:

```text
CloudFront Data Transfer

EKS Compute

RDS

Redis

NAT Gateways
```

---

Optimization Strategies:

```text
CloudFront Caching

Graviton Nodes

Reserved Instances

Read Replicas

Autoscaling
```

---

# Architecture 5 (Continued)

# Common Failure Scenarios

---

## Scenario 1

```text
Website Returns 403
```

Possible Causes:

```text
Incorrect OAC Configuration

Bucket Policy Error

CloudFront Misconfiguration
```

---

## Scenario 2

```text
Website Serving Old Content
```

Possible Causes:

```text
Long TTL

Browser Cache

Missing Invalidation
```

---

## Scenario 3

```text
High CloudFront Cost
```

Possible Causes:

```text
Poor Cache Configuration

Large Files

Excessive Traffic
```

---

# Production Checklist

```text
✓ HTTPS Enabled

✓ ACM Certificate

✓ OAC Enabled

✓ WAF Enabled

✓ Logging Enabled

✓ Compression Enabled

✓ Route53 Configured

✓ Cache Policies Configured
```

---

# Related Documents

```text
aws_cloudfront_guide.md

security_standards.md

terraform_module_catalog.md
```

---

# Architecture 6

# Serverless API Platform

---

# Purpose

This architecture provides a fully serverless backend platform capable of scaling automatically without infrastructure management.

The architecture is intended for:

```text
APIs

Microservices

Event Processing

Webhook Platforms

Backend Services
```

---

# Typical Use Cases

```text
REST APIs

Webhook Receivers

Mobile Backends

Internal APIs

Event Processing Systems
```

---

# When To Use

Use when:

```text
Workloads Are Event Driven

Traffic Is Variable

Operational Simplicity Required

Infrastructure Management Should Be Minimal
```

---

# When Not To Use

Avoid when:

```text
Long Running Processes

Heavy Compute

Complex Kubernetes Workloads

Persistent Connections Required
```

---

# Reference Architecture

```text
Users

↓

Route53

↓

CloudFront

↓

API Gateway

↓

Lambda

↓

DynamoDB

↓

CloudWatch
```

---

# Architecture Components

---

## Route53

Responsibilities:

```text
DNS Resolution

Domain Management
```

---

## CloudFront

Responsibilities:

```text
Caching

TLS

Performance Optimization
```

---

## API Gateway

Responsibilities:

```text
Request Routing

Authentication

Rate Limiting

API Management
```

---

## Lambda

Responsibilities:

```text
Business Logic

Request Processing

Event Handling
```

---

## DynamoDB

Responsibilities:

```text
Data Storage

High Scalability

Low Latency
```

---

# Module Composition

```hcl
module "route53"

module "acm"

module "cloudfront"

module "waf"

module "monitoring"

module "logging"
```

---

# Security Design

---

## Authentication

Recommended:

```text
Cognito

OIDC

JWT Validation
```

---

## Edge Protection

Use:

```text
CloudFront

WAF
```

---

## Lambda Permissions

Use:

```text
Least Privilege IAM
```

---

Never:

```text
AdministratorAccess
```

---

# Monitoring Design

Track:

```text
Invocations

Errors

Duration

Throttles

Latency
```

---

## API Metrics

Track:

```text
Request Count

Response Time

4XX Errors

5XX Errors
```

---

# Logging Design

Sources:

```text
API Gateway Logs

Lambda Logs

WAF Logs

CloudFront Logs
```

---

Retention:

```text
90 Days Minimum
```

---

# Cost Considerations

Largest cost drivers:

```text
Lambda Invocations

API Gateway Requests

CloudFront Traffic
```

---

Optimization:

```text
Caching

Efficient Lambda Design

Right-Sized Timeouts
```

---

# Common Failure Scenarios

---

## Scenario 1

```text
Lambda Timeout
```

Possible Causes:

```text
Slow Database

External API Delay

Poor Code Design
```

---

## Scenario 2

```text
API Returning 502
```

Possible Causes:

```text
Lambda Failure

Permission Error

Bad Integration Configuration
```

---

## Scenario 3

```text
High Costs
```

Possible Causes:

```text
Excessive Requests

Large Responses

Poor Caching
```

---

# Production Checklist

```text
✓ CloudFront Enabled

✓ WAF Enabled

✓ Monitoring Enabled

✓ Logging Enabled

✓ Least Privilege IAM

✓ JWT Validation

✓ Rate Limiting Enabled
```

---

# Related Documents

```text
aws_iam_guide.md

aws_cloudfront_guide.md

security_standards.md
```

---

# Architecture 7

# Multi-Account Landing Zone

---

# Purpose

This architecture establishes the foundational AWS organizational structure used by enterprises.

It provides:

```text
Security

Governance

Account Isolation

Centralized Management
```

---

# Typical Use Cases

```text
Enterprise AWS Adoption

Regulated Environments

Large Engineering Teams

Multiple Business Units
```

---

# Business Objectives

Provide:

```text
Isolation

Governance

Security

Scalability
```

for AWS operations.

---

# Reference Architecture

```text
AWS Organization

│

├── Management Account

├── Security Account

├── Shared Services Account

├── Development Account

├── Staging Account

└── Production Account
```

---

# Account Structure

---

## Management Account

Purpose:

```text
Organization Management

Billing

Governance
```

---

## Security Account

Purpose:

```text
Security Hub

GuardDuty

Audit Logs

CloudTrail
```

---

## Shared Services Account

Purpose:

```text
Identity Center

DNS

Shared Tooling

Central Services
```

---

## Development Account

Purpose:

```text
Developer Workloads

Testing

Experiments
```

---

## Staging Account

Purpose:

```text
Pre-Production Validation
```

---

## Production Account

Purpose:

```text
Customer Workloads

Critical Systems
```

---

# Security Design

---

## Identity

Use:

```text
IAM Identity Center
```

---

Avoid:

```text
IAM Users
```

---

## Governance

Implement:

```text
Service Control Policies

Tag Policies

Backup Policies
```

---

## Logging

Centralize:

```text
CloudTrail

Config

Security Findings
```

into Security Account.

---

# Networking Design

Preferred:

```text
Separate VPCs

Per Environment
```

---

Cross-account communication:

```text
Transit Gateway

VPC Peering

PrivateLink
```

depending on requirements.

---

# Monitoring Design

Centralize:

```text
Metrics

Logs

Security Events
```

into Shared Services or Security Account.

---

# Cost Design

Track:

```text
Per Account

Per Team

Per Environment
```

---

Mandatory Tags:

```text
Environment

Owner

Project

CostCenter
```

---

# Common Failure Scenarios

---

## Scenario 1

```text
Cross Account Access Failure
```

Possible Causes:

```text
Trust Policy Issues

SCP Restrictions

Role Misconfiguration
```

---

## Scenario 2

```text
Administrator Access Denied
```

Possible Causes:

```text
Service Control Policies
```

---

## Scenario 3

```text
Central Logging Failure
```

Possible Causes:

```text
Cross Account Permissions

CloudTrail Configuration Issues
```

---

# Production Checklist

```text
✓ Identity Center Enabled

✓ SCPs Configured

✓ Security Account Exists

✓ Central Logging Enabled

✓ CloudTrail Enabled

✓ GuardDuty Enabled

✓ Security Hub Enabled

✓ Backup Policies Enabled
```

---

# Related Documents

```text
aws_iam_guide.md

security_standards.md

terraform_module_catalog.md
```

---

# Architecture 8

# Complete Enterprise Platform

---

# Purpose

This architecture represents the most comprehensive platform architecture used within InfraGuid-managed environments.

It combines:

```text
Networking

Security

Kubernetes

Databases

Caching

Storage

Observability

CDN

Identity

AI Services
```

into a unified enterprise platform.

This architecture is intended for:

```text
Large Internal Platforms

Enterprise SaaS Products

Multi-Team Platforms

AI-Enabled Products

Developer Platforms
```

---

# Business Objectives

Provide:

```text
High Availability

Scalability

Security

Compliance

Operational Excellence

Platform Standardization
```

---

# Reference Architecture

```text
Users

↓

Route53

↓

CloudFront

↓

AWS WAF

↓

Application Load Balancer

↓

Amazon EKS

├── Application Services
├── Internal APIs
├── AI Services
├── Background Workers
└── Platform Services

↓

Redis

↓

PostgreSQL

↓

EFS

↓

AWS Backup

↓

Monitoring & Logging
```

---

# Module Composition

```hcl
module "vpc"

module "cloudfront"

module "waf"

module "route53"

module "acm"

module "alb"

module "eks"

module "irsa"

module "ecr"

module "rds"

module "elasticache"

module "efs"

module "backup"

module "monitoring"

module "logging"

module "secrets-manager"

module "vpc-endpoints"

module "bedrock-endpoints"
```

---

# Platform Layers

---

## Edge Layer

Services:

```text
Route53

CloudFront

WAF
```

Responsibilities:

```text
DNS

TLS

Caching

DDoS Protection

Request Filtering
```

---

## Traffic Layer

Services:

```text
Application Load Balancer
```

Responsibilities:

```text
Traffic Routing

SSL Termination

Health Checks
```

---

## Compute Layer

Services:

```text
Amazon EKS
```

Responsibilities:

```text
Application Hosting

Microservices

Platform Services

AI Services
```

---

## Data Layer

Services:

```text
PostgreSQL

Redis

EFS
```

Responsibilities:

```text
Persistent Storage

Caching

Shared Filesystems
```

---

## Observability Layer

Services:

```text
CloudWatch

Grafana

Prometheus
```

Responsibilities:

```text
Metrics

Logs

Dashboards

Alerting
```

---

# Networking Design

---

## VPC

Recommended CIDR:

```text
10.0.0.0/16
```

---

## Availability Zones

Production:

```text
3 AZ Minimum
```

---

## Public Subnets

Used for:

```text
ALB

NAT Gateway
```

---

## Private Application Subnets

Used for:

```text
EKS Worker Nodes

Application Pods
```

---

## Private Data Subnets

Used for:

```text
RDS

Redis

Storage Services
```

---

## VPC Endpoints

Mandatory:

```text
S3

Secrets Manager

CloudWatch

ECR

SSM
```

---

Recommended:

```text
Bedrock

STS

KMS
```

---

# Security Design

---

## Identity

Use:

```text
IAM Identity Center
```

---

Avoid:

```text
Long-Lived IAM Users
```

---

## Kubernetes Security

Implement:

```text
IRSA

Network Policies

RBAC

Pod Security Standards
```

---

## Secrets

Store:

```text
Database Credentials

API Keys

Certificates

Tokens
```

inside:

```text
Secrets Manager
```

---

## Edge Protection

Mandatory:

```text
CloudFront

WAF

TLS
```

---

## Data Protection

Mandatory:

```text
Encryption At Rest

Encryption In Transit
```

---

# IAM Design

---

## Human Access

Use:

```text
IAM Identity Center
```

---

## Workload Access

Use:

```text
IRSA
```

---

## CI/CD Access

Use:

```text
OIDC Federation
```

---

## Cross-Account Access

Use:

```text
IAM Roles

Trust Policies
```

---

# Observability Design

---

## Metrics

Track:

```text
Infrastructure Metrics

Application Metrics

Business Metrics

Security Metrics
```

---

## Dashboards

Required:

```text
Executive Dashboard

Platform Dashboard

Application Dashboard

Security Dashboard
```

---

## Alerts

Required:

```text
Availability Alerts

Latency Alerts

Security Alerts

Capacity Alerts
```

---

# Logging Design

Sources:

```text
Application Logs

Audit Logs

Infrastructure Logs

Security Logs

CloudFront Logs

ALB Logs

Kubernetes Logs
```

---

## Retention

Recommended:

```text
365 Days
```

for enterprise workloads.

---

# Backup Design

---

## Database

```text
30 Day Retention
```

minimum.

---

## EFS

```text
Daily Backup
```

---

## Terraform State

```text
Versioned

Encrypted

Replicated
```

---

## Secrets

```text
Versioned
```

---

# Cost Considerations

Major cost drivers:

```text
EKS

RDS

Redis

CloudFront

Data Transfer

Observability Stack
```

---

Optimization:

```text
Graviton

Reserved Instances

Spot Nodes

Autoscaling

CloudFront Caching
```

---

# Common Failure Scenarios

---

## Scenario 1

```text
Regional Failure
```

Mitigation:

```text
Backups

Disaster Recovery

Cross-Region Strategy
```

---

## Scenario 2

```text
Database Saturation
```

Mitigation:

```text
Read Replicas

Query Optimization

Scaling
```

---

## Scenario 3

```text
Node Exhaustion
```

Mitigation:

```text
Autoscaling

Karpenter

Capacity Monitoring
```

---

## Scenario 4

```text
Credential Compromise
```

Mitigation:

```text
Rotation

Least Privilege

Identity Center
```

---

# Production Checklist

```text
✓ Multi-AZ

✓ CloudFront

✓ WAF

✓ EKS

✓ Redis

✓ PostgreSQL

✓ EFS

✓ Monitoring

✓ Logging

✓ Backups

✓ Secrets Manager

✓ IRSA

✓ OIDC

✓ VPC Endpoints

✓ Encryption
```

---

# Related Documents

```text
terraform_module_catalog.md

terraform_aws_provider_guide.md

aws_vpc_guide.md

aws_iam_guide.md

aws_cloudfront_guide.md

aws_bedrock_guide.md

security_standards.md
```

---

# AI Architecture Selection Matrix

This matrix helps engineers and AI assistants select the appropriate architecture.

| Requirement | Architecture |
|------------|-------------|
| Internal Web Application | Three-Tier Application |
| Kubernetes Platform | Production EKS Platform |
| SaaS Product | Production SaaS Platform |
| Internal AI Assistant | Internal AI Assistant Platform |
| Documentation Site | Static Website Platform |
| Serverless Backend | Serverless API Platform |
| Enterprise AWS Environment | Multi-Account Landing Zone |
| Enterprise Platform | Complete Enterprise Platform |

---

# Terraform Composition Rules

All Terraform generation should follow the architecture-first approach.

---

## Rule 1

Select:

```text
Reference Architecture
```

before selecting services.

---

## Rule 2

Select:

```text
Modules
```

before selecting AWS resources.

---

## Rule 3

Prefer:

```text
Composition
```

instead of:

```text
Resource Creation
```

---

## Example

Preferred:

```hcl
module "vpc"

module "eks"

module "rds"
```

---

Avoid:

```hcl
resource "aws_vpc"

resource "aws_subnet"

resource "aws_route_table"
```

unless explicitly requested.

---

# Architecture Review Framework

Every architecture should be reviewed across the following domains.

---

## Security

Review:

```text
IAM

Encryption

Secrets

Network Exposure
```

---

## Reliability

Review:

```text
Multi-AZ

Backups

Monitoring

Recovery
```

---

## Performance

Review:

```text
Scaling

Caching

Latency
```

---

## Cost

Review:

```text
Compute

Storage

Data Transfer

Monitoring
```

---

## Operations

Review:

```text
Logging

Alerting

Runbooks

Ownership
```

---

# AI Generation Rules

This section defines mandatory rules for AI systems generating Terraform.

---

## Rule 1

Always attempt to map requests to:

```text
Reference Architecture
```

first.

---

## Rule 2

Always prefer:

```text
Approved Modules
```

over:

```text
Raw AWS Resources
```

---

## Rule 3

Always generate:

```text
Multi-AZ
```

for production environments.

---

## Rule 4

Always include:

```text
Monitoring

Logging

Backups
```

for production workloads.

---

## Rule 5

Always enforce:

```text
Encryption

Least Privilege

Secrets Management
```

---

## Rule 6

Use:

```text
OIDC

IRSA

Identity Center
```

where applicable.

---

## Rule 7

Prefer:

```text
Private Networking
```

for internal services.

---

## Rule 8

Never generate:

```text
Public Databases

Hardcoded Secrets

AdministratorAccess
```

unless explicitly requested.

---

## Rule 9

Generated architectures should prioritize:

```text
Security

Maintainability

Scalability

Operational Excellence
```

over minimal resource count.

---

# Governance Statement

This document defines the approved Terraform reference architectures used by InfraGuid Technologies Pvt. Ltd.

All Terraform code, infrastructure deployments, AI-generated infrastructure designs, platform implementations, and cloud architecture proposals should align with the architectures defined within this document whenever applicable.

Platform Engineering owns and maintains these architectures.

Architecture Team is responsible for architectural governance and approval.

Security Engineering is responsible for security validation and compliance.

Exceptions require approval from:

```text
Platform Engineering Lead

Solutions Architect

Security Engineering Lead
```

This document serves as the authoritative reference architecture catalog for all InfraGuid-managed AWS environments.
