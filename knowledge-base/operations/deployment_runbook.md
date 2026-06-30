# Deployment Runbook

**Document ID:** IG-DEP-001
**Version:** 1.0
**Owner:** Sneha Iyer (Senior DevOps Engineer)
**Department:** Platform Engineering
**Classification:** Internal Use Only
**Review Cycle:** Every 6 Months
**Last Updated:** June 2026

---

# 1. Purpose

This document defines the standard deployment procedures followed by InfraGuid Technologies Pvt. Ltd.

The objective of this runbook is to ensure:

* Safe Deployments
* Repeatable Processes
* Reduced Operational Risk
* Controlled Change Management
* Rapid Recovery Capability

This document serves as the authoritative deployment guide for all managed infrastructure and client environments.

---

# 2. Scope

This runbook applies to:

* AWS Infrastructure Deployments
* Terraform Deployments
* Landing Zone Deployments
* Kubernetes Deployments
* CI/CD Deployments
* Production Changes
* Managed Client Environments

Applicable personnel:

* Platform Engineers
* DevOps Engineers
* Cloud Engineers
* Cloud Operations Engineers

---

# 3. Deployment Principles

All deployments must adhere to the following principles.

---

# 3.1 Automation First

Deployments should be executed through automation whenever possible.

Preferred mechanisms:

* Terraform
* GitHub Actions
* Jenkins Pipelines

Manual deployments should be minimized.

---

# 3.2 Reproducibility

Every deployment must be repeatable.

A deployment should produce identical results regardless of who executes it.

---

# 3.3 Rollback Capability

Every deployment must have a documented rollback plan.

Deployments without rollback procedures must not proceed.

---

# 3.4 Auditability

All deployment activities must be:

* Logged
* Traceable
* Reviewable

Deployment history must be preserved.

---

# 3.5 Least Privilege

Deployment systems should operate with minimum required permissions.

---

# 4. Deployment Governance

Deployment governance ensures changes are controlled and reviewed.

---

# 4.1 Change Classification

Changes are categorized according to risk.

### Standard Change

Low risk.

Examples:

* Tag Updates
* Monitoring Configuration
* Documentation Changes

---

### Normal Change

Moderate risk.

Examples:

* Infrastructure Updates
* CI/CD Changes
* Security Configuration Updates

---

### High Risk Change

Significant impact potential.

Examples:

* Network Changes
* IAM Changes
* Production Database Changes

---

### Emergency Change

Urgent production recovery activity.

Examples:

* Security Incident Response
* Service Outage Recovery

---

# 4.2 Change Approval Requirements

| Change Type | Approval              |
| ----------- | --------------------- |
| Standard    | Team Lead             |
| Normal      | Team Lead + Owner     |
| High Risk   | Team Lead + Architect |
| Emergency   | Incident Commander    |

---

# 4.3 Deployment Windows

Production deployments should occur during approved deployment windows.

Recommended:

```text
Monday – Thursday

09:00 – 17:00 Local Time
```

Avoid:

* Weekends
* Holidays
* Major Business Events

unless approved.

---

# 5. Change Management Process

All deployments follow the standard change process.

```text
Request
↓
Review
↓
Approval
↓
Deployment
↓
Validation
↓
Closure
```

---

# 5.1 Change Request Creation

Every deployment requires:

* Description
* Scope
* Risk Assessment
* Rollback Plan

---

# 5.2 Technical Review

Review areas:

* Architecture Impact
* Security Impact
* Operational Impact

---

# 5.3 Deployment Approval

Required approvals must be obtained before deployment.

---

# 5.4 Change Execution

Deployment must follow approved procedures.

---

# 5.5 Post Deployment Validation

Validation confirms:

* Service Availability
* Infrastructure Health
* Monitoring Functionality

---

# 5.6 Change Closure

Deployment records must include:

* Results
* Validation Evidence
* Issues Encountered

---

# 6. Infrastructure Deployment Process

Infrastructure deployments create or modify cloud resources.

---

# 6.1 Infrastructure Deployment Workflow

```text
Code Commit
↓
Review
↓
Terraform Plan
↓
Approval
↓
Terraform Apply
↓
Validation
↓
Monitoring Review
```

---

# 6.2 Deployment Requirements

Before deployment verify:

* Approved Pull Request
* Successful Validation
* Rollback Plan Exists
* Monitoring Exists

---

# 6.3 Deployment Ownership

Infrastructure deployments are owned by:

```text
Platform Engineering Team
```

---

# 6.4 Production Deployment Requirements

Additional requirements:

* Change Approval
* Security Review
* Architecture Review (when applicable)

---

# 6.5 Deployment Evidence

Capture:

* Terraform Plan
* Approval Records
* Validation Results
* Deployment Logs

Deployment evidence must be retained for audit purposes.

---

# 7. Terraform Deployment Procedure

Terraform is the standard infrastructure deployment mechanism.

---

# 7.1 Pre-Deployment Checklist

Verify:

* Code Reviewed
* Validation Successful
* State Backend Healthy
* Variables Verified

---

# 7.2 Validation Commands

Required:

```bash
terraform fmt

terraform validate

terraform plan
```

All commands must complete successfully.

---

# 7.3 Plan Review

Review:

* Resource Creation
* Resource Modification
* Resource Deletion

Resource destruction requires explicit approval.

---

# 7.4 Deployment Execution

Preferred execution:

```text
GitHub Actions Pipeline
```

Direct local execution is discouraged.

---

# 7.5 Post Apply Validation

Verify:

* Resources Created
* Security Groups Correct
* IAM Policies Correct
* Monitoring Active

---

# 7.6 Terraform Failure Handling

If deployment fails:

```text
Stop
↓
Investigate
↓
Rollback
↓
Revalidate
```

Do not repeatedly rerun failed deployments without investigation.

# 8. AWS Landing Zone Deployment Procedure

AWS Landing Zone deployments establish the foundational cloud environment for client workloads.

Landing Zone deployments are considered high-risk infrastructure changes and require enhanced validation.

---

# 8.1 Deployment Objectives

The Landing Zone deployment process must establish:

* AWS Organizations
* Organizational Units
* Security Controls
* Centralized Logging
* Identity Federation
* Governance Controls

---

# 8.2 Deployment Prerequisites

Verify:

* AWS Organization Access
* Approved Architecture Design
* Security Review Completion
* Network Design Approval

---

# 8.3 Deployment Workflow

```text
Landing Zone Design
↓
Architecture Review
↓
Security Review
↓
Deployment Approval
↓
Foundation Deployment
↓
Validation
↓
Operational Handover
```

---

# 8.4 Deployment Sequence

Recommended deployment order:

```text
AWS Organization
↓
Organizational Units
↓
Accounts
↓
Identity Center
↓
Security Services
↓
Logging Services
↓
Networking Services
↓
Monitoring Services
```

---

# 8.5 Validation Requirements

Verify:

* Account Creation
* SCP Enforcement
* IAM Identity Center Access
* CloudTrail Logging
* Security Hub Integration
* GuardDuty Integration

---

# 8.6 Security Validation

Validate:

* MFA Enforcement
* SCP Configuration
* Cross-Account Roles
* Logging Configuration

---

# 8.7 Handover Requirements

Required deliverables:

* Landing Zone Documentation
* Network Diagrams
* Access Procedures
* Operational Runbooks

---

# 9. Amazon EKS Deployment Procedure

This procedure governs deployment of Kubernetes platforms.

---

# 9.1 Deployment Objectives

Ensure:

* Secure Cluster Deployment
* Operational Readiness
* Monitoring Coverage
* Security Baseline Compliance

---

# 9.2 Deployment Prerequisites

Required:

* Approved Architecture
* Approved VPC Design
* Container Registry Available
* Monitoring Design Approved

---

# 9.3 Deployment Workflow

```text
Cluster Configuration
↓
Cluster Deployment
↓
Node Group Deployment
↓
Security Configuration
↓
Monitoring Configuration
↓
Application Validation
↓
Go Live Approval
```

---

# 9.4 Cluster Validation Checklist

Verify:

* Control Plane Active
* Node Groups Healthy
* Cluster Connectivity Functional
* DNS Functional
* Ingress Functional

---

# 9.5 Security Validation

Verify:

* RBAC Enabled
* Secrets Management Configured
* Image Scanning Enabled
* Logging Enabled

---

# 9.6 Monitoring Validation

Verify:

* Prometheus Available
* Grafana Available
* Container Insights Enabled
* Alerting Functional

---

# 9.7 Production Readiness Requirements

Before production approval:

* Security Review Complete
* Disaster Recovery Plan Exists
* Monitoring Coverage Verified
* Runbooks Completed

---

# 10. Application Deployment Procedure

Application deployments include:

* Web Applications
* APIs
* Containerized Workloads
* Background Services

---

# 10.1 Deployment Objectives

Ensure:

* Zero Data Loss
* Minimal Downtime
* Rapid Recovery
* Controlled Release

---

# 10.2 Deployment Strategy Selection

Approved strategies:

### Rolling Deployment

Default strategy.

---

### Blue-Green Deployment

Recommended for:

* Critical Applications
* Customer Facing Platforms

---

### Canary Deployment

Recommended for:

* High Traffic Services
* Major Releases

---

# 10.3 Deployment Workflow

```text
Build
↓
Security Scan
↓
Testing
↓
Approval
↓
Deployment
↓
Validation
↓
Monitoring
```

---

# 10.4 Build Validation

Verify:

* Build Success
* Dependency Validation
* Security Scans Complete

---

# 10.5 Security Validation

Verify:

* Vulnerability Scanning
* Secret Scanning
* Dependency Scanning

No critical vulnerabilities may proceed to production.

---

# 10.6 Release Approval Requirements

Required approvals:

| Environment | Approval Required |
| ----------- | ----------------- |
| Development | Team Lead         |
| Staging     | Team Lead         |
| Production  | Team Lead + Owner |

---

# 10.7 Production Deployment Controls

Production deployments require:

* Monitoring Coverage
* Rollback Plan
* Deployment Approval
* Validation Checklist

---

# 11. Production Validation Procedure

Validation confirms successful deployment.

No deployment is considered complete until validation succeeds.

---

# 11.1 Validation Categories

Required validation:

* Infrastructure Validation
* Application Validation
* Security Validation
* Monitoring Validation

---

# 11.2 Infrastructure Validation

Verify:

* Resources Healthy
* Auto Scaling Functional
* Network Connectivity Functional

---

# 11.3 Application Validation

Verify:

* Endpoints Reachable
* Authentication Functional
* Critical Features Functional

---

# 11.4 Security Validation

Verify:

* Security Groups Correct
* IAM Roles Correct
* Encryption Enabled

---

# 11.5 Monitoring Validation

Verify:

* Dashboards Functional
* Alerts Functional
* Logs Available

---

# 11.6 Validation Evidence

Capture:

* Screenshots
* Logs
* Monitoring Results
* Health Check Results

---

# 12. Rollback Procedures

Every deployment must have a rollback strategy.

Rollback plans must be documented before deployment approval.

---

# 12.1 Rollback Objectives

Rollback procedures should:

* Restore Service
* Minimize Downtime
* Minimize Data Loss

---

# 12.2 Rollback Triggers

Rollback may be initiated when:

* Validation Fails
* Service Outage Occurs
* Security Risk Detected
* Performance Degradation Detected

---

# 12.3 Infrastructure Rollback Procedure

Terraform rollback workflow:

```text
Failed Deployment
↓
Stop Further Changes
↓
Identify Failure
↓
Restore Previous State
↓
Validate Recovery
```

---

# 12.4 Application Rollback Procedure

Application rollback workflow:

```text
Failed Release
↓
Previous Version
↓
Deployment
↓
Validation
↓
Monitoring
```

---

# 12.5 Database Rollback Requirements

Database rollbacks require:

* Data Validation
* Backup Availability
* Recovery Plan

Database rollbacks require elevated approval.

---

# 12.6 Rollback Validation

Verify:

* Service Functionality
* Monitoring Health
* User Access
* Security Controls

---

# 13. Emergency Deployment Process

Emergency deployments are reserved for urgent situations.

Examples:

* Production Outage
* Critical Security Vulnerability
* Business-Critical Failure

---

# 13.1 Emergency Deployment Principles

Emergency deployments prioritize:

* Service Restoration
* Risk Reduction

while maintaining auditability.

---

# 13.2 Emergency Workflow

```text
Incident Declared
↓
Emergency Approval
↓
Deployment
↓
Validation
↓
Post Incident Review
```

---

# 13.3 Emergency Approval Authority

Authorized approvers:

* Incident Commander
* Cloud Operations Lead
* CTO

---

# 13.4 Documentation Requirements

Required:

* Incident Reference
* Deployment Details
* Validation Evidence

---

# 13.5 Post Emergency Review

Required within:

```text
5 Business Days
```

after deployment.

---

# 14. Release Management Process

Release management coordinates deployments across environments.

---

# 14.1 Release Objectives

Ensure:

* Controlled Delivery
* Risk Management
* Traceability

---

# 14.2 Release Lifecycle

```text
Planning
↓
Review
↓
Approval
↓
Deployment
↓
Validation
↓
Closure
```

---

# 14.3 Release Planning

Review:

* Scope
* Dependencies
* Risks
* Resources

---

# 14.4 Release Documentation

Required:

* Release Notes
* Deployment Plan
* Rollback Plan

---

# 14.5 Release Approval

Production releases require documented approval.

---

# 14.6 Release Closure

Closure requires:

* Validation Complete
* Documentation Complete
* Stakeholder Notification Complete

```
```

# 15. Production Deployment Requirements

Production deployments represent the highest-risk operational activity performed by InfraGuid.

All production deployments must satisfy the requirements defined in this section.

---

# 15.1 Production Deployment Principles

Production deployments must be:

* Planned
* Reviewed
* Approved
* Auditable
* Recoverable

Emergency deployments are exceptions and must follow the Emergency Deployment Process.

---

# 15.2 Mandatory Preconditions

Before a production deployment begins, verify:

* Change Request Approved
* Rollback Plan Approved
* Validation Complete
* Security Review Complete (if applicable)
* Monitoring Coverage Confirmed

---

# 15.3 Required Documentation

The following documentation must exist:

* Deployment Plan
* Rollback Plan
* Release Notes
* Validation Checklist

Deployments lacking documentation must not proceed.

---

# 15.4 Infrastructure Deployment Controls

Required:

* Terraform Plan Review
* Architecture Review
* Security Validation

for all significant infrastructure changes.

---

# 15.5 Production Freeze Periods

Deployments should be avoided during:

* Major Client Events
* Peak Business Periods
* Active Incident Response Activities
* Declared Change Freeze Windows

---

# 15.6 Production Risk Assessment

Every deployment must include:

| Risk Level | Description                |
| ---------- | -------------------------- |
| Low        | Minimal Impact             |
| Medium     | Moderate Service Impact    |
| High       | Significant Service Impact |
| Critical   | Business Critical Impact   |

---

# 15.7 High-Risk Deployment Requirements

High-risk deployments require:

* Architect Approval
* Security Review
* Rollback Validation
* Enhanced Monitoring

Examples:

* VPC Changes
* Route Table Changes
* IAM Changes
* EKS Cluster Upgrades
* Production Database Modifications

---

# 16. Deployment Checklists

Standardized checklists improve deployment consistency.

---

# 16.1 Pre-Deployment Checklist

Verify:

```text
✓ Change Approved

✓ Rollback Plan Exists

✓ Monitoring Active

✓ Documentation Complete

✓ Validation Complete

✓ Deployment Window Approved

✓ Stakeholders Notified
```

---

# 16.2 Infrastructure Deployment Checklist

Verify:

```text
✓ Terraform Validation Successful

✓ Terraform Plan Reviewed

✓ Security Controls Verified

✓ Resource Naming Standards Followed

✓ Tagging Standards Applied
```

---

# 16.3 Application Deployment Checklist

Verify:

```text
✓ Build Successful

✓ Security Scan Successful

✓ Artifact Approved

✓ Configuration Validated

✓ Monitoring Active
```

---

# 16.4 Kubernetes Deployment Checklist

Verify:

```text
✓ Cluster Healthy

✓ Node Groups Healthy

✓ Ingress Functional

✓ Monitoring Functional

✓ Backup Strategy Validated
```

---

# 16.5 Post-Deployment Checklist

Verify:

```text
✓ Health Checks Passing

✓ Alerts Healthy

✓ Error Rates Normal

✓ Stakeholder Validation Complete

✓ Deployment Documentation Updated
```

---

# 17. Deployment Communication Process

Communication is mandatory throughout the deployment lifecycle.

---

# 17.1 Communication Objectives

Communication should ensure:

* Stakeholder Awareness
* Operational Coordination
* Risk Visibility

---

# 17.2 Required Stakeholders

Depending on deployment scope:

* Platform Engineering
* Cloud Operations
* Security Engineering
* Solutions Architecture
* Client Representatives

---

# 17.3 Pre-Deployment Communication

Notify stakeholders:

```text
24 Hours Before Deployment
```

minimum for production changes.

Notification must include:

* Deployment Scope
* Expected Impact
* Deployment Window
* Rollback Plan

---

# 17.4 Deployment Start Notification

At deployment start:

Communicate:

* Deployment Started
* Scope
* Expected Completion Time

---

# 17.5 Incident Communication

If issues occur:

Immediately communicate:

* Issue Description
* Impact
* Current Status
* Mitigation Actions

---

# 17.6 Deployment Completion Notification

Upon successful completion:

Communicate:

* Deployment Complete
* Validation Successful
* Monitoring Normal

---

# 17.7 Failed Deployment Notification

If rollback occurs:

Communicate:

* Failure Summary
* Rollback Status
* Recovery Status
* Follow-Up Actions

---

# 18. Post Deployment Review Process

Post-deployment reviews improve operational maturity.

---

# 18.1 Review Objectives

Determine:

* What Worked
* What Failed
* Improvement Opportunities

---

# 18.2 Review Triggers

Required for:

* High-Risk Deployments
* Failed Deployments
* Emergency Deployments

---

# 18.3 Review Participants

Required:

* Deployment Engineer
* Team Lead
* Service Owner

Optional:

* Security Engineer
* Solutions Architect

---

# 18.4 Review Topics

Review:

* Deployment Success
* Validation Results
* Monitoring Results
* Operational Issues
* Rollback Effectiveness

---

# 18.5 Lessons Learned

Document:

* Successes
* Failures
* Improvement Opportunities

---

# 18.6 Action Tracking

Every review should produce:

* Corrective Actions
* Preventive Actions
* Owners
* Due Dates

---

# 19. Deployment Metrics and KPIs

InfraGuid measures deployment performance using operational metrics.

---

# 19.1 Deployment Frequency

Measure:

```text
Number of Deployments
Per Environment
Per Month
```

---

# 19.2 Deployment Success Rate

Target:

```text
> 95%
```

---

# 19.3 Change Failure Rate

Target:

```text
< 5%
```

---

# 19.4 Mean Time To Recover (MTTR)

Target:

```text
< 60 Minutes
```

for deployment-related failures.

---

# 19.5 Rollback Rate

Track:

```text
Rollback Events
÷
Total Deployments
```

---

# 19.6 Validation Completion Rate

Target:

```text
100%
```

for production deployments.

---

# 19.7 Documentation Compliance

Target:

```text
100%
```

for deployment records.

---

# 20. Governance Statement

This document defines the official deployment procedures used by InfraGuid Technologies Pvt. Ltd.

All deployment activities performed within client environments and internal infrastructure must follow the standards, controls, approvals, and validation requirements defined within this runbook.

Exceptions require documented approval.

The Platform Engineering team owns and maintains this document.

The objectives of this runbook are to ensure:

* Safe Deployments
* Controlled Changes
* Consistent Processes
* Reliable Recovery
* Operational Excellence

across all client and internal cloud environments.


