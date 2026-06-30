# Architecture Standards Guide

**Document ID:** IG-ARCH-001
**Version:** 1.0
**Owner:** Rahul Varma (Principal Platform Engineer)
**Department:** Platform Engineering
**Classification:** Internal Use Only
**Review Cycle:** Every 6 Months
**Last Updated:** June 2026

---

# 1. Purpose

This document defines the official cloud architecture standards used by InfraGuid Technologies Pvt. Ltd. when designing, implementing, reviewing, and operating client cloud environments.

The objective of these standards is to ensure all delivered solutions are:

* Secure
* Scalable
* Highly Available
* Operationally Manageable
* Cost Efficient
* Compliant with Organizational Standards

These standards apply to all cloud architecture engagements delivered by InfraGuid unless an approved exception exists.

The standards described in this document represent the minimum acceptable architectural baseline for production environments.

---

# 2. Scope

This document applies to:

* AWS Landing Zone Implementations
* Cloud Migration Projects
* DevOps Modernization Projects
* Kubernetes Platform Deployments
* Managed Cloud Operations Environments
* Terraform-Based Infrastructure Deployments
* Internal Corporate Infrastructure

These standards must be followed by:

* Solutions Architects
* Platform Engineers
* DevOps Engineers
* Cloud Engineers
* Security Engineers
* Technical Reviewers

---

# 3. Architecture Governance Principles

InfraGuid follows a set of architecture principles that guide all design decisions.

These principles take precedence over implementation preferences.

---

## 3.1 Security by Default

Security controls must be integrated into the architecture from the beginning of the design process.

Security controls must never be treated as post-implementation enhancements.

Required controls include:

* Least Privilege Access
* Encryption at Rest
* Encryption in Transit
* Audit Logging
* Centralized Monitoring

Every architecture review must validate compliance with security standards.

---

## 3.2 Infrastructure as Code

All infrastructure must be provisioned through Infrastructure as Code.

Approved tooling:

```text
Terraform
```

Manual resource creation within production environments is prohibited unless formally approved.

Infrastructure must be:

* Version Controlled
* Peer Reviewed
* Reproducible
* Auditable

---

## 3.3 High Availability by Design

Production environments must be designed to tolerate infrastructure failures without service disruption.

Minimum requirements:

* Multi-AZ Deployments
* Redundant Network Paths
* Load Balancing
* Automated Recovery Mechanisms

Single points of failure must be identified and eliminated during architecture reviews.

---

## 3.4 Operational Excellence

Architectures must be designed with operations in mind.

Required operational capabilities include:

* Monitoring
* Logging
* Alerting
* Incident Response
* Backup and Recovery

Operational readiness is considered a mandatory architecture requirement.

---

## 3.5 Cost Awareness

Solutions should balance reliability, security, and performance with cost efficiency.

Cost optimization should occur throughout the lifecycle of the environment.

Architectures should avoid:

* Unnecessary Resource Duplication
* Overprovisioning
* Idle Infrastructure

---

# 4. AWS Account Standards

InfraGuid follows a multi-account AWS strategy for all production client environments.

Single-account production architectures are strongly discouraged.

---

## 4.1 Multi-Account Model

Recommended structure:

```text
AWS Organization

├── Management Account
├── Security Account
├── Log Archive Account
├── Shared Services Account
├── Development Account
├── Staging Account
└── Production Account
```

---

## 4.2 Management Account Standards

The Management Account exists solely for AWS Organizations administration.

Prohibited activities:

* Application Hosting
* Workload Deployment
* Database Hosting

The Management Account must not host business workloads.

---

## 4.3 Security Account Standards

The Security Account centralizes security tooling.

Typical services:

* Security Hub
* GuardDuty
* IAM Identity Center
* AWS Config Aggregation

This account should be accessible only to authorized security personnel.

---

## 4.4 Log Archive Account Standards

The Log Archive Account stores immutable audit logs.

Sources include:

* CloudTrail
* VPC Flow Logs
* AWS Config
* Security Findings

Log retention requirements must align with client compliance requirements.

---

# 5. Multi-Account Strategy

The primary goals of the multi-account strategy are:

* Security Isolation
* Operational Separation
* Blast Radius Reduction
* Governance Enforcement

Benefits include:

* Independent Security Boundaries
* Environment Isolation
* Simplified Access Management
* Reduced Operational Risk

All client production environments should adopt this model whenever practical.

# 6. Organizational Unit Standards

AWS Organizational Units (OUs) provide governance boundaries within AWS Organizations.

InfraGuid requires Organizational Units to be structured according to business purpose rather than individual teams.

---

## 6.1 Standard OU Structure

Recommended structure:

```text
Root

├── Security
├── Infrastructure
├── Production
├── Non-Production
├── Sandbox
└── Suspended
```

---

## 6.2 Security OU

Purpose:

Centralized security management.

Typical Accounts:

* Security Account
* Audit Account
* Compliance Account

Mandatory Controls:

* SCP Enforcement
* Centralized Logging
* Security Monitoring

---

## 6.3 Production OU

Purpose:

Host customer-facing workloads.

Requirements:

* Strict SCP Controls
* MFA Enforcement
* Centralized Logging
* Security Monitoring Enabled

---

## 6.4 Non-Production OU

Purpose:

Development and testing activities.

Examples:

* Development
* QA
* Staging

Restrictions may be relaxed compared to production environments.

---

## 6.5 Sandbox OU

Purpose:

Experimentation and learning.

Characteristics:

* Reduced Governance Controls
* Budget Restrictions
* Automatic Cleanup Policies

Sandbox environments must never contain production data.

---

# 7. VPC Architecture Standards

Virtual Private Clouds form the foundational networking layer for all AWS environments.

Every VPC must be designed with scalability, security, and operational manageability in mind.

---

## 7.1 VPC Design Principles

All VPC designs must:

* Support High Availability
* Support Growth
* Enable Secure Connectivity
* Avoid Network Overlap

---

## 7.2 CIDR Allocation Standards

CIDR ranges must be planned before implementation.

Recommended allocation:

```text
10.0.0.0/16
10.1.0.0/16
10.2.0.0/16
```

Avoid:

```text
192.168.x.x
```

when future hybrid connectivity is expected.

These ranges frequently overlap with on-premises environments.

---

## 7.3 Production VPC Standards

Production VPCs must include:

```text
Minimum 3 Availability Zones
```

for business-critical workloads.

---

## 7.4 Shared Services VPC

Shared services should be isolated.

Examples:

* Monitoring
* CI/CD
* Directory Services
* Shared Security Services

Recommended deployment:

```text
Dedicated Shared Services VPC
```

---

## 7.5 VPC Peering Restrictions

VPC Peering should not be used for large-scale architectures.

Preferred alternatives:

* Transit Gateway
* PrivateLink

VPC Peering creates operational complexity as environments grow.

---

# 8. Networking Standards

Networking design must prioritize security, scalability, and operational simplicity.

---

## 8.1 Network Segmentation

Infrastructure should be segmented according to function.

Recommended segmentation:

```text
Internet Layer

Application Layer

Data Layer

Management Layer
```

Each layer should have independent security controls.

---

## 8.2 East-West Traffic Control

Traffic between application tiers should be explicitly controlled.

Examples:

```text
Web Tier
↓
Application Tier
↓
Database Tier
```

Direct communication should be allowed only when required.

---

## 8.3 Network Access Model

Recommended model:

```text
Deny By Default
```

Access should be explicitly granted.

---

## 8.4 Security Group Standards

Security Groups should:

* Be Service-Oriented
* Avoid Wide CIDR Rules
* Use Security Group References

Preferred:

```text
ALB-SG
↓
Application-SG
```

Avoid:

```text
0.0.0.0/0
```

for internal communication.

---

## 8.5 NACL Standards

Network ACLs should remain simple.

Use NACLs for:

* Additional Security Boundaries
* Regulatory Requirements

Primary access control should remain:

```text
Security Groups
```

---

# 9. Public Subnet Standards

Public subnets host resources requiring direct internet accessibility.

---

## 9.1 Approved Public Resources

Examples:

* Application Load Balancers
* NAT Gateways
* Bastion Hosts (if approved)

---

## 9.2 Prohibited Public Resources

Examples:

* Databases
* Internal APIs
* Kubernetes Worker Nodes
* ChromaDB Servers
* Application Servers

These resources must remain private.

---

## 9.3 Internet Gateway Standards

Each VPC may contain:

```text
One Internet Gateway
```

attached at the VPC level.

---

## 9.4 Public Route Table Standards

Public route tables must include:

```text
0.0.0.0/0
↓
Internet Gateway
```

No other internet egress method should be used for public subnets.

---

# 10. Private Subnet Standards

Private subnets host business-critical workloads.

---

## 10.1 Approved Private Resources

Examples:

* EC2 Application Servers
* EKS Worker Nodes
* RDS Databases
* Internal APIs
* Internal Services

---

## 10.2 Private Route Standards

Internet-bound traffic should flow through:

```text
Private Subnet
↓
NAT Gateway
↓
Internet Gateway
```

Direct internet access is prohibited.

---

## 10.3 Database Placement Standards

Databases must always reside within private subnets.

Examples:

* RDS
* Aurora
* Self-Managed Databases

Public database endpoints are prohibited unless specifically approved.

---

## 10.4 Private Endpoint Standards

AWS services should be accessed using:

* Interface Endpoints
* Gateway Endpoints

where appropriate.

Examples:

* S3
* DynamoDB
* Secrets Manager
* Systems Manager

---

# 11. Transit Gateway Standards

Transit Gateway is the preferred connectivity hub for multi-VPC architectures.

---

## 11.1 Use Cases

Transit Gateway should be used when:

* More than 3 VPCs exist
* Multiple AWS Accounts exist
* Hybrid Connectivity exists

---

## 11.2 Design Principles

Recommended model:

```text
Transit Gateway

├── Shared Services VPC
├── Production VPC
├── Development VPC
├── Security VPC
└── On-Premises Network
```

---

## 11.3 Route Table Segmentation

Transit Gateway route tables should be segmented.

Examples:

* Production Route Table
* Non-Production Route Table
* Shared Services Route Table

---

## 11.4 Security Requirements

Transit Gateway deployments must include:

* Route Table Reviews
* Network Documentation
* Connectivity Validation

---

## 11.5 Prohibited Configurations

Avoid:

* Full Mesh VPC Peering
* Uncontrolled Route Propagation
* Shared Production and Development Routes

These increase operational and security risk.

---

# 12. Hybrid Connectivity Standards

Hybrid connectivity integrates client AWS environments with external networks.

Examples:

* Corporate Data Centers
* Branch Offices
* Third-Party Networks

---

## 12.1 Approved Connectivity Methods

Preferred options:

```text
AWS Direct Connect
```

Secondary option:

```text
Site-to-Site VPN
```

---

## 12.2 Connectivity Selection Criteria

Direct Connect:

* High Bandwidth
* Low Latency
* Long-Term Connectivity

VPN:

* Lower Cost
* Faster Deployment
* Temporary Connectivity

---

## 12.3 Routing Requirements

Hybrid routing must:

* Avoid Overlapping CIDRs
* Support Failover
* Be Documented

---

## 12.4 High Availability Requirements

Production hybrid environments must support:

* Redundant VPN Tunnels
* Redundant Direct Connect Links

Single-path connectivity is not acceptable for critical workloads.

---

## 12.5 Documentation Requirements

Every hybrid deployment must include:

* Network Diagram
* Routing Documentation
* Failover Procedure
* Recovery Procedure

Hybrid connectivity designs are subject to mandatory architecture review.

# 13. DNS Standards

Domain Name System (DNS) architecture is a critical component of cloud infrastructure.

Poor DNS design can result in:

* Service Outages
* Routing Failures
* Security Risks
* Operational Complexity

All client environments must implement DNS according to the standards defined in this section.

---

# 13.1 DNS Design Principles

DNS architecture must be:

* Highly Available
* Simple to Operate
* Secure
* Scalable
* Documented

DNS should never become a single point of failure.

---

# 13.2 Authoritative DNS Standard

InfraGuid standardizes on:

```text
Amazon Route53
```

for authoritative DNS management unless client requirements dictate otherwise.

Benefits:

* Native AWS Integration
* High Availability
* Health Checks
* Traffic Routing Policies
* DNSSEC Support

---

# 13.3 DNS Namespace Design

DNS namespaces should follow predictable patterns.

Recommended examples:

```text
client.com

www.client.com

api.client.com

portal.client.com

dev.client.com

staging.client.com
```

Avoid:

```text
app-new-prod.client.com

temp-api.client.com

test123.client.com
```

DNS names should clearly indicate purpose.

---

# 13.4 Environment Naming Standards

Recommended structure:

```text
dev.client.com

qa.client.com

staging.client.com

prod.client.com
```

Production should never share records with non-production environments.

---

# 13.5 Private DNS Standards

Private workloads must use:

```text
Private Hosted Zones
```

Examples:

```text
internal.client.local

corp.internal

services.internal
```

Private service discovery should never depend on public DNS.

---

# 13.6 DNS TTL Standards

Recommended values:

| Record Type          | TTL         |
| -------------------- | ----------- |
| Static Records       | 300 Seconds |
| Load Balancers       | 60 Seconds  |
| Migration Activities | 30 Seconds  |
| DR Failover Records  | 30 Seconds  |

Lower TTLs increase flexibility during incidents.

---

# 13.7 DNS Change Management

All DNS changes must:

* Be Documented
* Be Reviewed
* Be Tracked

Production DNS modifications require peer review.

---

# 13.8 DNS Security Requirements

Required controls:

* Route53 Access Restrictions
* IAM Least Privilege
* MFA Enforcement
* DNS Logging

DNS administration should be restricted to authorized personnel.

---

# 13.9 DNS Monitoring Requirements

Monitor:

* DNS Availability
* DNS Failures
* Health Check Status
* Domain Expiration

Expired domains are considered a critical operational failure.

---

# 14. Route53 Standards

Route53 is the approved DNS platform for AWS environments.

---

# 14.1 Hosted Zone Standards

Separate hosted zones should exist for:

```text
Production

Non-Production

Internal
```

This reduces operational risk.

---

# 14.2 Record Management Standards

Approved record types:

* A
* AAAA
* CNAME
* TXT
* MX
* NS

Use aliases whenever supported.

---

# 14.3 Alias Record Standards

Preferred:

```text
Route53 Alias
↓
CloudFront
```

```text
Route53 Alias
↓
ALB
```

Benefits:

* No DNS Query Charges
* Native AWS Integration
* Simplified Management

---

# 14.4 Health Check Standards

Critical endpoints must have Route53 health checks.

Examples:

* Production APIs
* Customer Portals
* Authentication Services

---

# 14.5 Failover Routing Standards

Critical applications should support:

```text
Primary Region
↓
Failure
↓
Secondary Region
```

where business requirements justify the cost.

---

# 14.6 DNSSEC Requirements

Public domains should implement:

```text
DNSSEC
```

when supported by the client's registrar.

---

# 15. Application Load Balancer Standards

Application Load Balancers (ALBs) are the standard ingress layer for web applications hosted within AWS.

---

# 15.1 ALB Design Principles

ALBs provide:

* High Availability
* SSL Termination
* Traffic Routing
* Health Checks
* Observability

ALBs must be deployed across multiple Availability Zones.

---

# 15.2 Availability Zone Requirements

Minimum standard:

```text
Two Availability Zones
```

Preferred standard:

```text
Three Availability Zones
```

for production workloads.

---

# 15.3 Public ALB Standards

Public ALBs may be used for:

* Web Applications
* APIs
* Customer Portals

Public ALBs must:

* Use HTTPS
* Integrate with WAF
* Log Requests

---

# 15.4 Internal ALB Standards

Internal ALBs should be used for:

* Internal Services
* Shared Services
* Service-to-Service Communication

Internal ALBs must not be internet accessible.

---

# 15.5 Listener Standards

Required:

```text
HTTPS
```

Preferred ports:

```text
443
```

HTTP listeners should redirect to HTTPS.

---

# 15.6 TLS Standards

Approved TLS versions:

```text
TLS 1.2
TLS 1.3
```

Prohibited:

```text
TLS 1.0
TLS 1.1
```

---

# 15.7 Health Check Standards

Every target group must define:

* Health Check Path
* Healthy Threshold
* Unhealthy Threshold
* Timeout Values

Recommended health endpoint:

```text
/health
```

---

# 15.8 Target Group Standards

Target groups should represent a single service.

Example:

```text
Frontend Service
↓
Frontend Target Group
```

Avoid mixing unrelated applications.

---

# 15.9 Logging Requirements

ALBs must send access logs to:

```text
Centralized S3 Bucket
```

Retention requirements must align with client compliance requirements.

---

# 15.10 Security Requirements

Public ALBs must integrate with:

```text
AWS WAF
```

before production approval.

---

# 15.11 Monitoring Requirements

Required metrics:

* Request Count
* Error Rate
* Latency
* Healthy Hosts
* Unhealthy Hosts

CloudWatch alarms must exist for critical thresholds.

---

# 16. CloudFront Standards

CloudFront is the preferred content delivery platform for internet-facing applications.

---

# 16.1 CloudFront Usage Criteria

CloudFront should be used for:

* Static Websites
* Public APIs
* Media Delivery
* Global Applications

---

# 16.2 Architecture Pattern

Standard pattern:

```text
User
↓
CloudFront
↓
WAF
↓
ALB
↓
Application
```

CloudFront should be the primary public entry point whenever possible.

---

# 16.3 Origin Standards

Approved origins:

* S3
* ALB
* API Gateway

---

# 16.4 S3 Origin Security

Public S3 buckets are prohibited.

Required architecture:

```text
CloudFront
↓
Origin Access Control
↓
Private S3 Bucket
```

---

# 16.5 Caching Standards

Static assets should be aggressively cached.

Examples:

```text
Images

CSS

JavaScript

Fonts
```

Dynamic content should use shorter cache durations.

---

# 16.6 Compression Standards

Enable:

* GZIP
* Brotli

where supported.

---

# 16.7 Geographic Restrictions

Geo-restrictions may be enabled when:

* Regulatory Requirements Exist
* Licensing Restrictions Exist

---

# 16.8 CloudFront Logging

Required:

```text
CloudFront Access Logs
```

or

```text
Real-Time Logs
```

for production environments.

---

# 16.9 Security Requirements

CloudFront must integrate with:

* AWS WAF
* TLS Certificates
* Security Headers

---

# 16.10 Monitoring Requirements

Monitor:

* Cache Hit Ratio
* Origin Latency
* Error Rates
* Request Volume

---

# 17. AWS WAF Standards

AWS WAF provides Layer 7 application protection.

All internet-facing applications must be evaluated for WAF protection.

---

# 17.1 WAF Deployment Standards

Required architecture:

```text
Internet
↓
CloudFront
↓
WAF
↓
Application
```

---

# 17.2 Managed Rule Standards

Minimum baseline:

* AWS Core Rule Set
* Known Bad Inputs
* IP Reputation Lists

---

# 17.3 Custom Rule Standards

Custom rules should address:

* Business Logic Abuse
* API Abuse
* Application-Specific Threats

---

# 17.4 Rate Limiting Standards

Rate limiting should be enabled for:

* Login Endpoints
* Public APIs
* Registration Pages

---

# 17.5 IP Restriction Standards

Examples:

```text
Administrative Interfaces

Internal Dashboards

Management Portals
```

may require IP restrictions.

---

# 17.6 Logging Requirements

All WAF deployments must send logs to:

```text
Amazon S3

or

CloudWatch Logs
```

---

# 17.7 Security Monitoring Requirements

Monitor:

* Blocked Requests
* Allowed Requests
* Rate-Limited Requests
* Top Attack Sources

---

# 17.8 WAF Change Management

WAF rule changes must:

* Be Tested
* Be Reviewed
* Include Rollback Procedures

Poorly designed WAF rules can create production outages.

---

# 18. API Architecture Standards

API design standards apply to:

* Public APIs
* Internal APIs
* Service APIs

---

# 18.1 API Design Principles

APIs must be:

* Secure
* Observable
* Versioned
* Documented

---

# 18.2 API Versioning Standard

Recommended:

```text
/api/v1
/api/v2
```

Avoid breaking existing consumers.

---

# 18.3 Authentication Standards

Approved methods:

* OAuth2
* OpenID Connect
* JWT

API Keys alone are insufficient for sensitive systems.

---

# 18.4 Rate Limiting Standards

All public APIs must implement:

* Request Limits
* Abuse Protection
* Monitoring

---

# 18.5 API Documentation Standards

Every API must provide:

* Endpoint Documentation
* Authentication Documentation
* Error Documentation
* Version Information

---

# 18.6 API Monitoring Requirements

Required metrics:

* Request Count
* Error Rate
* Latency
* Authentication Failures
* Throttling Events

---

# 18.7 API Security Requirements

APIs must:

* Use TLS
* Validate Input
* Sanitize Data
* Log Security Events

---

# 18.8 API Availability Targets

Production APIs should target:

```text
99.9% Availability
```

minimum.

Business-critical systems may require higher availability objectives.

# 19. EC2 Standards

Amazon EC2 remains the default compute platform for workloads that require operating system-level control.

All EC2 deployments must follow the standards defined in this section.

---

# 19.1 EC2 Design Principles

EC2 environments must be:

* Secure
* Highly Available
* Observable
* Automated
* Recoverable

Production environments must never rely on manually managed instances.

---

# 19.2 Approved Operating Systems

Approved operating systems:

### Linux

Preferred:

```text
Amazon Linux 2023
```

Supported:

```text
Ubuntu LTS
```

### Windows

Only when application requirements exist.

---

# 19.3 Instance Selection Standards

Instance selection must align with workload requirements.

Examples:

| Workload          | Recommended Family |
| ----------------- | ------------------ |
| General Purpose   | t3, t4g, m7i       |
| Compute Intensive | c7i                |
| Memory Intensive  | r7i                |
| Storage Intensive | i4i                |

Oversized instances are prohibited.

---

# 19.4 High Availability Requirements

Production EC2 workloads must use:

```text
Auto Scaling Groups
```

Single-instance production deployments are prohibited unless approved through an architecture exception.

---

# 19.5 AMI Standards

Custom AMIs must be:

* Version Controlled
* Security Hardened
* Scanned Regularly

Golden AMIs are preferred.

---

# 19.6 Access Standards

Direct SSH access should be minimized.

Preferred access:

```text
AWS Systems Manager Session Manager
```

Benefits:

* No Bastion Hosts
* Audit Logging
* Reduced Attack Surface

---

# 19.7 Security Requirements

All EC2 instances must:

* Use IAM Roles
* Enable CloudWatch Agent
* Enable Patch Management
* Enable Centralized Logging

Long-term access keys are prohibited.

---

# 19.8 Storage Standards

Root volumes must use:

```text
Amazon EBS
```

Encryption:

```text
Mandatory
```

---

# 19.9 Monitoring Standards

Required metrics:

* CPU Utilization
* Memory Utilization
* Disk Usage
* Network Throughput

---

# 19.10 Backup Requirements

Critical workloads require:

* Daily Backups
* Automated Snapshot Policies
* Recovery Testing

---

# 20. Auto Scaling Standards

Auto Scaling is mandatory for production workloads.

---

# 20.1 Design Objectives

Auto Scaling should provide:

* High Availability
* Elastic Capacity
* Fault Tolerance

---

# 20.2 Availability Zone Distribution

Production Auto Scaling Groups must span:

```text
Minimum Two Availability Zones
```

Preferred:

```text
Three Availability Zones
```

---

# 20.3 Scaling Policies

Approved scaling methods:

### Target Tracking

Preferred.

Example:

```text
CPU > 60%
```

---

### Step Scaling

Used for predictable workloads.

---

### Scheduled Scaling

Used for known traffic patterns.

---

# 20.4 Capacity Requirements

Production workloads must define:

* Minimum Capacity
* Desired Capacity
* Maximum Capacity

Example:

```text
Min: 2

Desired: 2

Max: 10
```

---

# 20.5 Health Check Standards

Required:

```text
EC2 Health Checks
ALB Health Checks
```

---

# 20.6 Instance Refresh Standards

Auto Scaling deployments should use:

```text
Instance Refresh
```

instead of manual replacement.

---

# 21. Amazon EKS Standards

Amazon EKS is the preferred Kubernetes platform.

---

# 21.1 EKS Design Principles

EKS clusters must be:

* Secure
* Highly Available
* Observable
* Upgradeable

---

# 21.2 Cluster Architecture

Recommended architecture:

```text
Amazon EKS

├── Control Plane
├── Managed Node Groups
├── Ingress Layer
├── Monitoring Stack
└── Security Controls
```

---

# 21.3 Control Plane Standards

Use:

```text
AWS Managed Control Plane
```

Self-managed Kubernetes control planes are prohibited.

---

# 21.4 Node Group Standards

Preferred:

```text
Managed Node Groups
```

Benefits:

* Reduced Operations
* Managed Updates
* Simplified Maintenance

---

# 21.5 Namespace Standards

Namespaces must separate workloads.

Example:

```text
production

staging

monitoring

security

shared-services
```

---

# 21.6 Workload Isolation Standards

Sensitive workloads should use:

* Dedicated Node Groups
* Taints
* Tolerations

---

# 21.7 Ingress Standards

Approved ingress:

```text
AWS Load Balancer Controller
```

---

# 21.8 Container Registry Standards

Approved registry:

```text
Amazon ECR
```

Public container registries should be minimized.

---

# 21.9 Secrets Management Standards

Secrets must never be stored in:

* Git Repositories
* Helm Charts
* ConfigMaps

Approved storage:

```text
AWS Secrets Manager
```

---

# 21.10 Monitoring Requirements

Required tooling:

```text
Prometheus

Grafana

CloudWatch Container Insights
```

---

# 21.11 Security Requirements

Required controls:

* RBAC
* Network Policies
* Image Scanning
* Pod Security Standards

---

# 21.12 Upgrade Standards

Clusters must remain within:

```text
N-1 Kubernetes Version
```

of supported AWS versions.

---

# 22. Amazon RDS Standards

RDS is the preferred relational database platform.

---

# 22.1 Approved Database Engines

Preferred:

* PostgreSQL
* MySQL

Use SQL Server only when required.

---

# 22.2 High Availability Standards

Production databases must use:

```text
Multi-AZ
```

deployments.

---

# 22.3 Backup Standards

Mandatory:

* Automated Backups
* Point-In-Time Recovery

---

# 22.4 Encryption Standards

Encryption at rest:

```text
Mandatory
```

Encryption in transit:

```text
Mandatory
```

---

# 22.5 Database Placement

RDS instances must reside in:

```text
Private Subnets
```

Publicly accessible databases are prohibited.

---

# 22.6 Monitoring Requirements

Required metrics:

* CPU
* Connections
* Storage
* Replication Lag

---

# 22.7 Read Replica Standards

Read replicas should be considered for:

* Read-heavy workloads
* Reporting systems

---

# 22.8 Database Access Standards

Applications must connect through:

```text
Application Security Groups
```

CIDR-based database access should be avoided.

---

# 23. Amazon S3 Standards

Amazon S3 is the standard object storage platform.

---

# 23.1 Security Requirements

Public buckets:

```text
Prohibited
```

unless explicitly approved.

---

# 23.2 Encryption Requirements

All buckets must enable:

```text
SSE-KMS
```

Preferred.

Alternative:

```text
SSE-S3
```

---

# 23.3 Bucket Naming Standards

Recommended format:

```text
client-environment-purpose-region
```

Example:

```text
acme-prod-logs-ap-south-1
```

---

# 23.4 Versioning Standards

Required for:

* Critical Data
* Logs
* Terraform State

---

# 23.5 Lifecycle Policies

Lifecycle policies should manage:

* Cost Optimization
* Retention
* Archival

---

# 23.6 Access Logging

Critical buckets should enable:

```text
Access Logging
```

---

# 23.7 Cross-Region Replication

Use when:

* Disaster Recovery Requirements Exist
* Compliance Requirements Exist

---

# 23.8 Terraform State Storage

Terraform state buckets must:

* Enable Versioning
* Enable Encryption
* Restrict Access

---

# 24. Backup Standards

Backups are mandatory for all critical systems.

---

# 24.1 Backup Objectives

Backups must support:

* Recovery
* Disaster Recovery
* Compliance

---

# 24.2 Protected Resources

Required:

* RDS
* EBS
* EFS
* Critical S3 Data

---

# 24.3 Backup Automation

Backups must be:

```text
Automated
```

Manual backups are insufficient.

---

# 24.4 Backup Validation

Backups must be tested regularly.

A backup that cannot be restored is considered invalid.

---

# 24.5 Recovery Objectives

Architectures must define:

```text
RPO
Recovery Point Objective

RTO
Recovery Time Objective
```

---

# 24.6 Retention Standards

Recommended baseline:

| Data Type | Retention |
| --------- | --------- |
| Daily     | 30 Days   |
| Weekly    | 12 Weeks  |
| Monthly   | 12 Months |

Client requirements may override these values.

---

# 25. Disaster Recovery Standards

Disaster Recovery planning is required for all production environments.

---

# 25.1 DR Strategy Selection

Approved strategies:

### Backup & Restore

Lowest cost.

---

### Pilot Light

Moderate cost.

---

### Warm Standby

Higher availability.

---

### Active/Active

Highest availability.

---

# 25.2 Business Impact Analysis

Every production workload must define:

* Criticality
* RTO
* RPO

---

# 25.3 Regional Failure Planning

Critical workloads should evaluate:

```text
Region Failure
```

scenarios.

---

# 25.4 Recovery Documentation

Required:

* Recovery Runbook
* Escalation Procedure
* Validation Checklist

---

# 25.5 Recovery Testing

Production recovery procedures must be tested:

```text
At Least Annually
```

---

# 25.6 Disaster Recovery Review

Architecture reviews must validate:

* Recovery Procedures
* Recovery Automation
* Backup Coverage
* Recovery Testing Results

A disaster recovery strategy that has not been tested should be considered unverified.

# 26. Terraform Standards

Terraform is the approved Infrastructure as Code platform for all client and internal cloud infrastructure deployments.

All Terraform implementations must follow the standards defined in this section.

The objective is to ensure:

* Consistency
* Maintainability
* Security
* Reusability
* Operational Excellence

---

# 26.1 Terraform Design Principles

Terraform implementations must be:

* Modular
* Reusable
* Version Controlled
* Peer Reviewed
* Environment Agnostic

Infrastructure code should be treated with the same engineering rigor as application code.

---

# 26.2 Approved Terraform Version

All projects must standardize on a single Terraform version.

Example:

```text
Terraform 1.11.x
```

Version pinning is mandatory.

Example:

```hcl
terraform {
  required_version = "~> 1.11"
}
```

---

# 26.3 Provider Version Management

Provider versions must be explicitly defined.

Example:

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

Uncontrolled provider upgrades are prohibited.

---

# 26.4 State Management Standards

Production state files must use:

```text
Remote Backend
```

Approved backend:

```text
Amazon S3
```

with:

```text
DynamoDB State Locking
```

---

# 26.5 Terraform State Architecture

Required architecture:

```text
Terraform

↓

S3 Backend

↓

Versioning Enabled

↓

DynamoDB Lock Table
```

---

# 26.6 Local State Restrictions

Local state files are prohibited for:

* Production
* Staging
* Shared Infrastructure

Allowed only for:

* Sandboxes
* Personal Labs

---

# 26.7 Terraform Code Review Requirements

All Terraform changes require:

* Pull Request
* Peer Review
* Plan Review

Required reviewers:

* Platform Engineer
* Infrastructure Owner

---

# 26.8 Terraform Apply Restrictions

Terraform Apply must occur through:

```text
CI/CD Pipeline
```

Direct local applies are discouraged.

Production applies require documented approval.

---

# 26.9 Terraform Validation Standards

Required pipeline steps:

```bash
terraform fmt

terraform validate

terraform plan
```

All steps must pass before deployment approval.

---

# 26.10 Resource Ownership Standards

Every Terraform-managed resource must include:

* Owner
* Environment
* Project
* Cost Center

through standardized tags.

---

# 27. Terraform Module Standards

Modules improve consistency and maintainability.

All infrastructure components should use approved modules.

---

# 27.1 Module Design Principles

Modules must be:

* Reusable
* Environment Independent
* Well Documented
* Version Controlled

---

# 27.2 Approved Module Structure

```text
modules/

├── vpc
├── security-group
├── alb
├── ec2
├── rds
├── eks
├── cloudfront
└── monitoring
```

---

# 27.3 Module Inputs

Inputs must be:

* Explicit
* Typed
* Documented

Example:

```hcl
variable "environment" {
  type = string
}
```

---

# 27.4 Module Outputs

Outputs should expose only required values.

Examples:

```hcl
output "vpc_id"

output "subnet_ids"
```

Avoid exposing unnecessary resources.

---

# 27.5 Module Versioning

Modules must use semantic versioning.

Example:

```text
v1.0.0

v1.1.0

v2.0.0
```

---

# 27.6 Module Documentation Requirements

Every module must include:

* Purpose
* Inputs
* Outputs
* Examples
* Limitations

---

# 28. Repository Standards

Infrastructure repositories must follow a consistent structure.

---

# 28.1 Repository Structure

Recommended structure:

```text
terraform-live/

├── dev
├── staging
├── prod
├── modules
├── docs
└── scripts
```

---

# 28.2 Branching Strategy

Approved branches:

```text
main

develop

feature/*
```

Direct commits to main are prohibited.

---

# 28.3 Pull Request Standards

Every PR must include:

* Change Description
* Risk Assessment
* Rollback Plan
* Terraform Plan Output

---

# 28.4 Protected Branch Requirements

Production branches must enforce:

* Pull Requests
* Review Approval
* CI Validation

---

# 29. CI/CD Standards

CI/CD pipelines are mandatory for infrastructure and application deployments.

---

# 29.1 Design Principles

Pipelines must be:

* Automated
* Auditable
* Repeatable
* Secure

---

# 29.2 Approved CI/CD Platforms

Preferred:

```text
GitHub Actions
```

Supported:

```text
Jenkins
```

---

# 29.3 Pipeline Stages

Required stages:

```text
Code Commit

↓

Validation

↓

Security Checks

↓

Plan

↓

Approval

↓

Deployment

↓

Verification
```

---

# 29.4 Secret Management Standards

Secrets must never be stored in:

* Git Repositories
* Pipeline Variables
* Source Code

Approved storage:

```text
AWS Secrets Manager
```

---

# 29.5 Deployment Approval Standards

Production deployments require:

* Change Approval
* Peer Review
* Validation Results

---

# 30. Monitoring Standards

Monitoring is mandatory for all production workloads.

---

# 30.1 Monitoring Objectives

Monitoring must detect:

* Failures
* Performance Issues
* Capacity Risks
* Security Events

---

# 30.2 Three Pillars of Observability

All architectures must support:

```text
Metrics

Logs

Traces
```

---

# 30.3 Monitoring Architecture

Recommended architecture:

```text
Application

↓

CloudWatch

↓

Alerts

↓

Operations Team
```

---

# 30.4 Infrastructure Monitoring Requirements

Required metrics:

* CPU
* Memory
* Disk
* Network

---

# 30.5 Application Monitoring Requirements

Required metrics:

* Request Rate
* Error Rate
* Latency

---

# 30.6 Alerting Standards

Alerts must be:

* Actionable
* Relevant
* Prioritized

Avoid alert fatigue.

---

# 30.7 Severity Classification

| Severity | Description       |
| -------- | ----------------- |
| Critical | Service Outage    |
| High     | Major Degradation |
| Medium   | Partial Impact    |
| Low      | Informational     |

---

# 31. Logging Standards

Logs are essential for troubleshooting, auditing, and security investigations.

---

# 31.1 Logging Principles

Logs must be:

* Centralized
* Searchable
* Retained
* Protected

---

# 31.2 Mandatory Log Sources

Required:

* CloudTrail
* VPC Flow Logs
* Application Logs
* ALB Logs
* CloudFront Logs

---

# 31.3 Log Retention Standards

Recommended minimum:

| Log Type    | Retention |
| ----------- | --------- |
| Application | 90 Days   |
| Security    | 1 Year    |
| Audit       | 7 Years   |

---

# 31.4 Sensitive Data Logging

The following must never be logged:

* Passwords
* API Keys
* Tokens
* Secrets
* Credit Card Data

---

# 31.5 Centralized Logging Architecture

Recommended:

```text
Applications

↓

CloudWatch Logs

↓

Central Storage

↓

Analysis Platform
```

---

# 32. Security Baseline Requirements

All environments must satisfy minimum security requirements.

---

# 32.1 Identity Security

Mandatory:

* MFA
* Least Privilege
* IAM Roles

---

# 32.2 Encryption Requirements

Required:

* Encryption At Rest
* Encryption In Transit

---

# 32.3 Logging Requirements

Mandatory:

* CloudTrail
* Security Monitoring
* Audit Logging

---

# 32.4 Vulnerability Management

Requirements:

* Patch Management
* Image Scanning
* Dependency Scanning

---

# 32.5 Security Review Requirement

Production environments require:

```text
Formal Security Review
```

prior to go-live.

---

# 33. Tagging Standards

Tagging enables governance, automation, cost allocation, and operational management.

All resources must be tagged.

---

# 33.1 Mandatory Tags

Required tags:

| Tag         | Purpose         |
| ----------- | --------------- |
| Name        | Resource Name   |
| Environment | Environment     |
| Owner       | Resource Owner  |
| Project     | Project Name    |
| CostCenter  | Cost Allocation |
| ManagedBy   | Automation Tool |

---

# 33.2 Example

```text
Name=prod-web-alb

Environment=prod

Owner=platform-team

Project=client-portal

CostCenter=cc-001

ManagedBy=terraform
```

---

# 33.3 Tag Enforcement

Tag compliance should be enforced through:

* SCPs
* AWS Config
* CI/CD Validation

---

# 34. Naming Convention Standards

Naming consistency improves operational clarity.

---

# 34.1 General Format

Recommended format:

```text
environment-application-resource
```

Example:

```text
prod-portal-alb
```

---

# 34.2 EC2 Naming Standard

Example:

```text
prod-web-01

prod-web-02
```

---

# 34.3 ALB Naming Standard

Example:

```text
prod-portal-alb
```

---

# 34.4 S3 Naming Standard

Example:

```text
client-prod-logs-ap-south-1
```

---

# 34.5 Security Group Naming Standard

Example:

```text
prod-web-sg

prod-db-sg
```

---

# 35. Architecture Review Process

Every production architecture must undergo formal review.

---

# 35.1 Review Objectives

Validate:

* Security
* Scalability
* Reliability
* Compliance

---

# 35.2 Review Participants

Required:

* Solutions Architect
* Platform Engineer
* Security Engineer

---

# 35.3 Review Checklist

Review:

* Networking
* IAM
* Encryption
* Monitoring
* Backup Strategy
* Disaster Recovery

---

# 35.4 Review Outcomes

Possible outcomes:

```text
Approved

Approved With Conditions

Rejected
```

---

# 36. Exception Management Process

Exceptions allow controlled deviation from standards.

---

# 36.1 Exception Criteria

Valid reasons:

* Client Requirement
* Technical Limitation
* Regulatory Requirement

---

# 36.2 Exception Request Requirements

Must include:

* Business Justification
* Risk Assessment
* Mitigation Plan
* Expiration Date

---

# 36.3 Approval Requirements

Required approvers:

* Solutions Architect
* Security Engineer
* CTO

---

# 36.4 Exception Review Cycle

Exceptions must be reviewed:

```text
Every 6 Months
```

---

# 37. Governance Statement

This document defines the official architecture standards of InfraGuid Technologies Pvt. Ltd.

These standards establish the minimum acceptable baseline for all client and internal cloud environments.

All employees involved in architecture, implementation, operations, and security activities must comply with these standards.

Exceptions require formal approval through the Exception Management Process.

The Platform Engineering team owns and maintains this document.

The objective of these standards is to ensure:

* Secure Architectures
* Reliable Systems
* Scalable Platforms
* Operational Excellence
* Consistent Delivery

Across all client engagements and internal environments.
