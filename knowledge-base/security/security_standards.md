# Security Standards Guide

**Document ID:** IG-SEC-001
**Version:** 1.0
**Owner:** Nikhil Sharma (Cloud Security Engineer)
**Department:** Security Engineering
**Classification:** Internal Use Only
**Review Cycle:** Every 6 Months
**Last Updated:** June 2026

---

# 1. Purpose

This document defines the official security standards adopted by InfraGuid Technologies Pvt. Ltd.

The purpose of these standards is to establish a consistent security baseline across all client and internal cloud environments.

These standards define:

* Security Governance
* Identity Management
* Access Control
* Secrets Management
* Encryption Requirements
* Security Monitoring
* Incident Response Requirements
* Compliance Expectations

All personnel responsible for designing, deploying, managing, or supporting infrastructure must comply with these standards.

---

# 2. Scope

These standards apply to:

* AWS Environments
* Internal Corporate Systems
* Managed Client Environments
* Kubernetes Platforms
* CI/CD Platforms
* Infrastructure as Code Repositories
* Operational Tooling

Applicable personnel:

* Solutions Architects
* Platform Engineers
* DevOps Engineers
* Cloud Engineers
* Security Engineers
* Operations Engineers

---

# 3. Security Principles

Security decisions must align with the following principles.

---

# 3.1 Security By Default

Security controls must be enabled by default.

Security should never be optional.

Every environment must begin from a secure baseline.

---

# 3.2 Least Privilege

Users, applications, and systems should receive only the permissions required to perform their responsibilities.

Access should be:

```text
Minimum Required Access
```

rather than:

```text
Maximum Possible Access
```

---

# 3.3 Zero Trust Mindset

Trust must never be assumed.

Every request should be validated.

Every access attempt should be authenticated and authorized.

---

# 3.4 Defense In Depth

Multiple security controls should protect critical systems.

Example:

```text
IAM
↓
Security Group
↓
WAF
↓
Application Authentication
↓
Audit Logging
```

No single control should be solely relied upon.

---

# 3.5 Security As Code

Security controls should be implemented through automation.

Examples:

* Terraform
* Policy Enforcement
* Automated Security Validation

Manual security configuration should be minimized.

---

# 3.6 Continuous Verification

Security posture must be continuously monitored.

Security is not a one-time activity.

---

# 4. Security Governance Model

InfraGuid follows a shared security responsibility model.

---

# 4.1 Executive Leadership Responsibilities

Owner:

```text
Chief Technology Officer
```

Responsibilities:

* Security Governance
* Policy Approval
* Risk Acceptance
* Security Budget Approval

---

# 4.2 Security Engineering Responsibilities

Owner:

```text
Security Engineering Team
```

Responsibilities:

* Security Standards
* Security Reviews
* Compliance Validation
* Security Monitoring

---

# 4.3 Platform Engineering Responsibilities

Owner:

```text
Platform Engineering Team
```

Responsibilities:

* Secure Infrastructure Design
* Security Control Implementation
* Infrastructure Compliance

---

# 4.4 Operations Responsibilities

Owner:

```text
Cloud Operations Team
```

Responsibilities:

* Monitoring
* Incident Detection
* Security Escalation

---

# 5. Identity and Access Management Standards

Identity is the primary security boundary.

Strong IAM governance is mandatory.

---

# 5.1 IAM Design Principles

Identity systems must support:

* Authentication
* Authorization
* Accountability
* Auditability

---

# 5.2 Human Access Model

Preferred access model:

```text
User
↓
IAM Identity Center
↓
Role Assumption
↓
AWS Account
```

Long-lived IAM users should be avoided.

---

# 5.3 Root Account Standards

Root accounts must:

* Enable MFA
* Use Hardware MFA when possible
* Remain Unused for Daily Operations

Root credentials should only be used for account recovery.

---

# 5.4 IAM User Restrictions

IAM users are prohibited except when:

* Service Limitations Exist
* Legacy Requirements Exist

Approval is required.

---

# 5.5 Role-Based Access Control

Access should be granted through roles.

Examples:

```text
ReadOnly

Developer

PlatformEngineer

SecurityEngineer

Administrator
```

Role definitions must be documented.

---

# 5.6 Permission Assignment Standards

Permissions must be:

* Role Based
* Reviewed
* Approved

Direct user permissions should be avoided.

---

# 5.7 MFA Requirements

Mandatory for:

* AWS Access
* GitHub Access
* Administrative Systems
* Security Tooling

Production access without MFA is prohibited.

---

# 5.8 Privileged Access Management

Privileged access includes:

* Administrator Access
* Security Administration
* Production Modification Rights

Requirements:

* MFA
* Logging
* Approval Process

---

# 5.9 Access Reviews

Access reviews must occur:

```text
Quarterly
```

Minimum.

Review objectives:

* Remove Excess Access
* Remove Inactive Users
* Validate Role Assignments

---

# 5.10 Employee Offboarding Requirements

Employee offboarding must include:

* Identity Disablement
* Credential Revocation
* Access Review

Target completion:

```text
Within 24 Hours
```

---

# 6. Password Standards

Passwords remain relevant for certain systems.

---

# 6.1 Password Requirements

Minimum:

```text
Length: 14 Characters
```

Requirements:

* Uppercase
* Lowercase
* Numeric
* Special Character

---

# 6.2 Password Reuse

Password reuse is prohibited.

---

# 6.3 Shared Credentials

Shared accounts are prohibited.

Individual accountability must exist.

---

# 6.4 Password Storage

Passwords must never be stored:

* In Source Code
* In Documentation
* In Chat Systems
* In Terraform Variables

---

# 6.5 Password Managers

Approved storage:

```text
Enterprise Password Manager
```

or

```text
AWS Secrets Manager
```

where applicable.

# 7. Secrets Management Standards

Secrets are among the most sensitive assets within any cloud environment.

Improper handling of secrets is one of the most common causes of security incidents.

Examples of secrets include:

* Database Passwords
* API Keys
* OAuth Credentials
* Encryption Keys
* Certificates
* Service Credentials
* Access Tokens

---

# 7.1 Secrets Management Principles

Secrets must be:

* Centralized
* Encrypted
* Auditable
* Rotatable
* Access Controlled

Secrets should never be manually distributed between employees.

---

# 7.2 Approved Secret Storage Platforms

Approved platforms:

```text
AWS Secrets Manager
```

Supported:

```text
AWS Systems Manager Parameter Store
```

for non-sensitive configuration data.

---

# 7.3 Prohibited Secret Storage Locations

Secrets must never be stored in:

* Git Repositories
* Terraform Variables Files
* Documentation
* Slack
* Microsoft Teams
* Jira Tickets
* Source Code

Violations are considered security incidents.

---

# 7.4 Application Secret Retrieval

Applications should retrieve secrets dynamically.

Recommended pattern:

```text
Application
↓
IAM Role
↓
Secrets Manager
↓
Runtime Retrieval
```

Hardcoded secrets are prohibited.

---

# 7.5 Secret Rotation Standards

Critical secrets must support rotation.

Examples:

* Database Credentials
* Administrative Credentials
* Service Credentials

Recommended rotation:

| Secret Type                | Rotation Frequency |
| -------------------------- | ------------------ |
| Database Credentials       | 90 Days            |
| Administrative Credentials | 60 Days            |
| Service Credentials        | 90 Days            |
| API Keys                   | 90 Days            |

---

# 7.6 Secret Access Controls

Access should follow:

```text
Least Privilege
```

Only systems and users requiring access should receive permissions.

---

# 7.7 Secret Auditing Requirements

Required logging:

* Secret Retrieval
* Secret Updates
* Secret Deletions
* Permission Changes

All events must be auditable.

---

# 7.8 Emergency Secret Rotation

Emergency rotation must occur when:

* Credential Exposure
* Employee Termination
* Security Incident
* Third-Party Compromise

Target completion:

```text
Within 24 Hours
```

---

# 8. Encryption Standards

Encryption is mandatory for all production and sensitive environments.

---

# 8.1 Encryption Objectives

Encryption protects:

* Confidentiality
* Integrity
* Compliance Requirements

---

# 8.2 Encryption Requirements

Mandatory:

```text
Encryption At Rest
```

Mandatory:

```text
Encryption In Transit
```

No exceptions without formal approval.

---

# 8.3 Encryption At Rest Standards

The following resources must be encrypted:

* EBS Volumes
* RDS Databases
* S3 Buckets
* EFS File Systems
* Backup Repositories
* Secrets

---

# 8.4 Encryption In Transit Standards

Approved protocols:

```text
TLS 1.2
TLS 1.3
```

---

# 8.5 Prohibited Encryption Protocols

The following are prohibited:

```text
SSL

TLS 1.0

TLS 1.1
```

---

# 8.6 Client Data Encryption

Client data must always be encrypted.

This applies to:

* Production Data
* Backup Data
* Replicated Data

---

# 8.7 Cross-Region Replication Encryption

Replicated data must remain encrypted throughout replication.

---

# 8.8 Encryption Validation

Architecture reviews must verify:

* Encryption Enabled
* Key Ownership Defined
* Rotation Configured

---

# 9. Key Management Standards

Encryption is only effective when keys are managed securely.

---

# 9.1 Approved Key Management Platform

Standard platform:

```text
AWS KMS
```

---

# 9.2 Key Ownership Requirements

Every KMS key must have:

* Owner
* Purpose
* Rotation Policy

documented.

---

# 9.3 Customer Managed Keys

Preferred for:

* Production Systems
* Sensitive Data
* Compliance Workloads

---

# 9.4 AWS Managed Keys

Acceptable for:

* Non-Critical Workloads
* Internal Services

when business requirements permit.

---

# 9.5 Key Rotation Standards

Automatic key rotation should be enabled whenever supported.

---

# 9.6 Key Access Control

KMS permissions must follow:

```text
Least Privilege
```

---

# 9.7 Key Monitoring

Monitor:

* Key Usage
* Key Deletion Attempts
* Permission Changes

---

# 9.8 Key Deletion Controls

Key deletion must require:

* Approval
* Risk Assessment
* Recovery Planning

---

# 10. Security Group Standards

Security Groups represent the primary network security control within AWS.

---

# 10.1 Security Group Design Principles

Security Groups must:

* Restrict Access
* Minimize Exposure
* Be Service-Oriented

---

# 10.2 Default Deny Model

Recommended model:

```text
No Access
↓
Explicit Allow Rules
```

---

# 10.3 Ingress Rule Standards

Ingress rules should be:

* Specific
* Documented
* Justified

Avoid broad CIDR ranges.

---

# 10.4 Preferred Security Group References

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

for internal traffic.

---

# 10.5 Administrative Access Standards

Administrative access should originate only from:

* VPN
* Approved Management Networks
* Session Manager

---

# 10.6 Database Security Group Standards

Database Security Groups must allow access only from:

* Application Security Groups
* Approved Administrative Systems

---

# 10.7 Security Group Reviews

Security Groups must be reviewed:

```text
Quarterly
```

minimum.

---

# 11. Network Security Standards

Network architecture must support multiple security layers.

---

# 11.1 Network Segmentation

Recommended segmentation:

```text
Internet Layer

Application Layer

Data Layer

Management Layer
```

---

# 11.2 Public Exposure Controls

Public internet exposure should be minimized.

Only approved resources may be public.

Examples:

* CloudFront
* ALB
* API Gateway

---

# 11.3 Private Resource Requirements

Examples:

* Databases
* EKS Nodes
* Internal APIs
* Shared Services

must remain private.

---

# 11.4 VPC Flow Logs

Mandatory for:

```text
Production VPCs
```

Recommended for all environments.

---

# 11.5 Network Monitoring

Monitor:

* Unexpected Traffic
* Port Scanning
* Traffic Spikes
* Suspicious Connections

---

# 11.6 Hybrid Connectivity Security

Required controls:

* VPN Encryption
* Route Restrictions
* Access Reviews

---

# 11.7 Bastion Host Standards

Bastion Hosts should be avoided.

Preferred access:

```text
AWS Systems Manager Session Manager
```

---

# 12. Production Access Controls

Production environments require enhanced controls.

---

# 12.1 Production Access Principles

Production access must be:

* Justified
* Logged
* Audited
* Temporary

---

# 12.2 Standing Administrative Access

Standing administrative access is discouraged.

Preferred model:

```text
Just-In-Time Access
```

---

# 12.3 Production Change Requirements

Production modifications require:

* Change Request
* Peer Review
* Approval

---

# 12.4 Emergency Access Procedure

Emergency access must:

* Be Approved
* Be Logged
* Be Reviewed After Use

---

# 12.5 Production Session Logging

Administrative sessions should be logged whenever technically possible.

---

# 12.6 Privileged Access Reviews

Privileged access reviews must occur:

```text
Quarterly
```

minimum.

---

# 12.7 Production Account Restrictions

Production accounts must enforce:

* MFA
* Logging
* Role-Based Access

---

# 12.8 Break Glass Accounts

Break Glass Accounts may exist for emergency recovery.

Requirements:

* MFA
* Secure Storage
* Restricted Usage
* Audit Logging

Use of Break Glass accounts must trigger a security review.

# 13. Vulnerability Management Standards

Vulnerability Management ensures security weaknesses are identified, assessed, prioritized, and remediated before they can be exploited.

All production and non-production environments must participate in the vulnerability management program.

---

# 13.1 Objectives

The vulnerability management program exists to:

* Reduce Security Risk
* Improve Security Posture
* Maintain Compliance
* Prevent Exploitation

---

# 13.2 Scope

Applies to:

* EC2 Instances
* Containers
* Kubernetes Clusters
* Operating Systems
* Third-Party Software
* CI/CD Platforms
* Internal Applications

---

# 13.3 Vulnerability Lifecycle

InfraGuid follows the process below:

```text
Discover
↓
Assess
↓
Prioritize
↓
Remediate
↓
Validate
↓
Close
```

---

# 13.4 Vulnerability Classification

Severity is determined using CVSS scoring.

| Severity | CVSS      |
| -------- | --------- |
| Critical | 9.0 – 10  |
| High     | 7.0 – 8.9 |
| Medium   | 4.0 – 6.9 |
| Low      | 0.1 – 3.9 |

---

# 13.5 Remediation Targets

| Severity | Target  |
| -------- | ------- |
| Critical | 7 Days  |
| High     | 14 Days |
| Medium   | 30 Days |
| Low      | 90 Days |

Exceptions require documented approval.

---

# 13.6 Vulnerability Scanning Requirements

Required scans:

* Operating System Scans
* Container Scans
* Dependency Scans
* Infrastructure Scans

---

# 13.7 Vulnerability Exceptions

Exception requests must include:

* Business Justification
* Risk Assessment
* Mitigation Plan
* Expiration Date

---

# 14. Patch Management Standards

Patch management reduces exposure to known vulnerabilities.

---

# 14.1 Patch Management Principles

Patching must be:

* Scheduled
* Tested
* Documented
* Verified

---

# 14.2 Patch Categories

### Security Patches

Highest priority.

---

### Bug Fixes

Applied according to maintenance schedules.

---

### Feature Updates

Evaluated separately.

---

# 14.3 Operating System Patching

Production servers must receive:

* Security Updates
* Critical Updates
* Kernel Updates

according to maintenance windows.

---

# 14.4 Patch Validation

Before production deployment:

* Validate Functionality
* Validate Monitoring
* Validate Connectivity

---

# 14.5 Patch Compliance Targets

Target compliance:

```text
95%+
```

for production systems.

---

# 14.6 Emergency Patching

Emergency patching may be initiated when:

* Active Exploitation Exists
* Critical Vulnerability Exists
* Regulatory Requirement Exists

---

# 15. Container Security Standards

Containers introduce unique security considerations.

These standards apply to:

* Docker
* Amazon EKS
* Kubernetes Workloads

---

# 15.1 Approved Base Images

Preferred:

```text
Official Vendor Images
```

or

```text
Company Approved Base Images
```

---

# 15.2 Container Image Scanning

Mandatory before deployment.

Scan for:

* Vulnerabilities
* Malware
* Exposed Secrets

---

# 15.3 Container Registry Standards

Approved registry:

```text
Amazon ECR
```

---

# 15.4 Image Versioning

Images must use explicit versions.

Avoid:

```text
latest
```

---

Preferred:

```text
v1.2.3
```

---

# 15.5 Privileged Containers

Privileged containers are prohibited unless formally approved.

---

# 15.6 Root User Restrictions

Containers should not run as:

```text
root
```

---

# 15.7 Secret Management

Secrets must be injected dynamically.

Never embed secrets inside images.

---

# 15.8 Container Logging

Container logs must be centralized.

---

# 16. Kubernetes Security Standards

Kubernetes clusters require additional controls beyond infrastructure security.

---

# 16.1 RBAC Requirements

Role-Based Access Control must be enabled.

Required roles:

* Read Only
* Developer
* Platform Engineer
* Administrator

---

# 16.2 Namespace Isolation

Namespaces should separate:

```text
Production

Staging

Monitoring

Security
```

---

# 16.3 Network Policies

Network Policies should restrict:

* Pod-to-Pod Traffic
* Namespace Traffic

---

# 16.4 Admission Controls

Admission policies should validate:

* Security Settings
* Image Sources
* Resource Limits

---

# 16.5 Image Source Restrictions

Only approved registries may be used.

---

# 16.6 Cluster Administrator Access

Cluster Admin access must be tightly controlled.

Approval required.

---

# 16.7 Audit Logging

Kubernetes audit logging must be enabled.

---

# 16.8 Kubernetes Upgrades

Clusters must remain within supported versions.

---

# 17. CI/CD Security Standards

CI/CD pipelines have access to critical systems and therefore require enhanced security controls.

---

# 17.1 Pipeline Security Principles

Pipelines must be:

* Auditable
* Secure
* Reproducible

---

# 17.2 Source Code Protection

Repositories must enforce:

* Pull Requests
* Review Requirements
* Branch Protection

---

# 17.3 Pipeline Permissions

Pipelines should receive:

```text
Minimum Required Permissions
```

---

# 17.4 Secret Handling

Secrets must be retrieved dynamically.

Approved source:

```text
AWS Secrets Manager
```

---

# 17.5 Artifact Security

Artifacts should be:

* Signed
* Versioned
* Traceable

---

# 17.6 Deployment Controls

Production deployments require:

* Approval
* Audit Trail
* Validation

---

# 17.7 Pipeline Logging

Pipeline activity must be logged.

Examples:

* Deployments
* Rollbacks
* Permission Changes

---

# 18. Logging and Audit Standards

Logging provides visibility into infrastructure and security events.

---

# 18.1 Logging Objectives

Logs support:

* Troubleshooting
* Auditing
* Forensics
* Compliance

---

# 18.2 Mandatory Log Sources

Required:

* CloudTrail
* VPC Flow Logs
* ALB Logs
* CloudFront Logs
* Application Logs

---

# 18.3 Audit Logging Requirements

Administrative actions must be logged.

Examples:

* IAM Changes
* Security Group Changes
* Route Table Changes
* KMS Changes

---

# 18.4 Log Integrity

Logs must be protected from tampering.

---

# 18.5 Centralized Log Storage

Recommended architecture:

```text
CloudTrail
↓
Central S3 Bucket
↓
Security Analysis
```

---

# 18.6 Log Retention

Minimum retention:

| Log Type    | Retention |
| ----------- | --------- |
| Application | 90 Days   |
| Operational | 1 Year    |
| Audit       | 7 Years   |

---

# 18.7 Sensitive Information

Logs must never contain:

* Passwords
* Secrets
* Tokens
* Private Keys

---

# 19. Security Monitoring Standards

Security monitoring provides continuous visibility into threats and risks.

---

# 19.1 Monitoring Objectives

Detect:

* Unauthorized Access
* Suspicious Activity
* Configuration Drift
* Security Incidents

---

# 19.2 Required Security Services

Production environments should enable:

```text
GuardDuty

Security Hub

CloudTrail

AWS Config
```

---

# 19.3 Alert Categories

Required alerts:

### Identity Alerts

* Failed Logins
* Privilege Escalation
* MFA Failures

---

### Network Alerts

* Port Scanning
* Suspicious Connections

---

### Infrastructure Alerts

* Security Group Changes
* Route Table Changes
* IAM Changes

---

### Data Protection Alerts

* Public S3 Exposure
* KMS Changes
* Secret Access Events

---

# 19.4 Alert Response Targets

| Severity | Response Target |
| -------- | --------------- |
| Critical | Immediate       |
| High     | 15 Minutes      |
| Medium   | 1 Hour          |
| Low      | 1 Business Day  |

---

# 20. Security Incident Management Standards

Security incidents require structured response procedures.

---

# 20.1 Security Incident Definition

A security incident includes:

* Unauthorized Access
* Credential Exposure
* Data Breach
* Malware Detection
* Infrastructure Compromise

---

# 20.2 Security Incident Severity

| Severity | Description              |
| -------- | ------------------------ |
| Sev-1    | Critical Business Impact |
| Sev-2    | Major Security Event     |
| Sev-3    | Limited Security Impact  |
| Sev-4    | Informational Event      |

---

# 20.3 Incident Response Process

```text
Detect
↓
Assess
↓
Contain
↓
Investigate
↓
Recover
↓
Review
```

---

# 20.4 Containment Requirements

Containment actions may include:

* Account Disablement
* Credential Rotation
* Network Isolation
* Resource Shutdown

---

# 20.5 Evidence Preservation

Preserve:

* CloudTrail Logs
* Security Findings
* Audit Records
* System Logs

---

# 20.6 Post Incident Reviews

Required for:

* Sev-1
* Sev-2

incidents.

---

# 20.7 Corrective Actions

Every major incident must produce:

* Root Cause Analysis
* Corrective Actions
* Preventive Actions

---

# 21. Security Review Process

All production environments require formal security review.

---

# 21.1 Security Review Triggers

Required before:

* Production Go-Live
* Major Architecture Changes
* Significant IAM Changes
* Compliance Assessments

---

# 21.2 Review Scope

Review:

* IAM
* Networking
* Encryption
* Monitoring
* Logging
* Backup Strategy

---

# 21.3 Review Outcomes

Possible outcomes:

```text
Approved

Approved With Conditions

Rejected
```

---

# 21.4 Security Review Documentation

Required outputs:

* Findings Report
* Risk Register
* Remediation Plan

---

# 22. Compliance Requirements

InfraGuid aligns with commonly accepted security and compliance frameworks.

---

# 22.1 Guiding Frameworks

Reference frameworks:

* CIS Benchmarks
* AWS Well-Architected Framework
* NIST Cybersecurity Framework
* ISO 27001 Principles

---

# 22.2 Compliance Objectives

Objectives include:

* Confidentiality
* Integrity
* Availability
* Accountability

---

# 22.3 Data Protection Requirements

Client data must be:

* Protected
* Encrypted
* Auditable

throughout its lifecycle.

---

# 22.4 Audit Readiness

Production environments should maintain:

* Documentation
* Audit Logs
* Security Records

sufficient for security reviews.

---

# 23. Security Exception Management

Security exceptions allow temporary deviations from standards.

---

# 23.1 Valid Exception Reasons

Examples:

* Client Requirements
* Technical Constraints
* Regulatory Requirements

---

# 23.2 Exception Documentation

Must include:

* Business Justification
* Risk Assessment
* Mitigation Plan
* Expiration Date

---

# 23.3 Approval Requirements

Required approvers:

* Security Engineer
* Solutions Architect
* CTO

---

# 23.4 Review Frequency

Exceptions must be reviewed:

```text
Every 6 Months
```

minimum.

---

# 24. Governance Statement

This document defines the official security standards of InfraGuid Technologies Pvt. Ltd.

All employees, contractors, consultants, and third parties operating within InfraGuid-managed environments are required to comply with these standards.

These requirements establish the minimum acceptable security baseline for all cloud environments managed, deployed, reviewed, or supported by InfraGuid.

Failure to comply with these standards may result in:

* Security Findings
* Operational Escalation
* Compliance Violations
* Risk Acceptance Reviews

The Security Engineering team owns and maintains this document.

The objective of these standards is to ensure:

* Secure Infrastructure
* Protected Client Data
* Strong Identity Controls
* Effective Incident Response
* Continuous Security Improvement

across all client and internal environments.


