# Service Catalog

**Document ID:** IG-SVC-001
**Version:** 1.0
**Owner:** Divya Rajan (Solutions Architect)
**Department:** Solutions Architecture
**Classification:** Internal Use Only
**Review Cycle:** Every 6 Months
**Last Updated:** June 2026

---

# 1. Purpose

This document defines the official service offerings provided by InfraGuid Technologies Pvt. Ltd.

The purpose of this catalog is to:

* Standardize service offerings
* Define delivery scope
* Clarify ownership
* Establish delivery expectations
* Support project planning
* Assist employee onboarding

All client-facing services must align with the definitions provided in this document.

---

# 2. Scope

This catalog applies to:

* Sales Teams
* Solutions Architects
* Platform Engineers
* Cloud Operations Teams
* Security Engineers
* Project Coordinators

The services described in this document represent the approved service portfolio of InfraGuid.

---

# 3. Service Portfolio Overview

InfraGuid provides services across five primary domains.

```text id="svcportfolio"
Cloud Architecture
↓
Infrastructure Automation
↓
DevOps Engineering
↓
Cloud Security
↓
Managed Cloud Operations
```

---

# 4. Service Delivery Principles

All services are delivered according to the following principles.

---

## 4.1 Automation First

Solutions should prioritize automation over manual operations.

Examples:

* Terraform
* CI/CD Pipelines
* Automated Monitoring

---

## 4.2 Security by Default

Security controls must be integrated into all service offerings.

Examples:

* IAM Controls
* Encryption
* Monitoring
* Audit Logging

---

## 4.3 Infrastructure as Code

All infrastructure implementations should be delivered through Infrastructure as Code.

Preferred tooling:

```text id="iacstandard"
Terraform
```

---

## 4.4 Documentation Driven Delivery

Every project must include documentation deliverables.

Minimum documentation:

* Architecture Documentation
* Operational Documentation
* Deployment Documentation

---

# 5. Service Category 1

# Cloud Architecture Services

Cloud Architecture Services focus on designing scalable, secure, and resilient cloud platforms.

---

## Service Owner

```text id="owner1"
Divya Rajan
Solutions Architect
```

---

## Objectives

* Design AWS Environments
* Improve Scalability
* Improve Reliability
* Improve Security

---

## Typical Deliverables

* High Level Architecture Diagram
* Detailed Architecture Diagram
* AWS Account Strategy
* Network Design
* Security Design
* Cost Estimation

---

## Technologies

* AWS
* VPC
* Route53
* CloudFront
* ALB
* Transit Gateway

---

## Typical Engagement Duration

```text id="duration1"
1 - 4 Weeks
```

---

## Included Activities

* Discovery Workshops
* Architecture Design
* Design Reviews
* Technical Recommendations

---

## Excluded Activities

* Application Development
* Managed Operations
* End User Support

---

# 6. Service Category 2

# AWS Landing Zone Implementation

This service provides secure AWS foundations for clients.

---

## Service Owner

```text id="owner2"
Rahul Varma
Principal Platform Engineer
```

---

## Objectives

Establish a secure multi-account AWS environment.

---

## Deliverables

* AWS Organizations Setup
* Account Structure
* IAM Baseline
* Logging Configuration
* Security Baseline

---

## Technologies

* AWS Organizations
* IAM Identity Center
* CloudTrail
* AWS Config
* Security Hub

---

## Typical Engagement Duration

```text id="duration2"
2 - 6 Weeks
```

---

## Included Activities

* Multi-Account Design
* Security Baseline Configuration
* Governance Controls
* Documentation

---

## Success Criteria

Client receives a production-ready AWS foundation.

---

# 7. Service Category 3

# Infrastructure as Code Implementation

This service focuses on infrastructure automation and standardization.

---

## Service Owner

```text id="owner3"
Rahul Varma
Principal Platform Engineer
```

---

## Objectives

Eliminate manual infrastructure management.

---

## Deliverables

* Terraform Modules
* Terraform Standards
* Environment Automation
* State Management Strategy

---

## Technologies

* Terraform
* Terragrunt
* GitHub Actions

---

## Typical Engagement Duration

```text id="duration3"
2 - 8 Weeks
```

---

## Included Activities

* Terraform Development
* Module Design
* State Strategy Design
* Automation Setup

---

## Excluded Activities

* Application Refactoring
* Business Process Consulting

---

# 8. Service Category 4

# DevOps Engineering Services

This service enables automated software delivery and operational efficiency.

---

## Service Owner

```text id="owner4"
Sneha Iyer
Senior DevOps Engineer
```

---

## Objectives

Improve software delivery speed and reliability.

---

## Deliverables

* CI/CD Pipelines
* Deployment Automation
* Release Procedures
* Build Automation

---

## Technologies

* GitHub Actions
* Jenkins
* Docker
* Kubernetes

---

## Typical Engagement Duration

```text id="duration4"
2 - 10 Weeks
```

---

## Included Activities

* Pipeline Design
* Pipeline Implementation
* Deployment Automation
* Release Process Design

---

## Success Criteria

Client can perform automated deployments with minimal manual intervention.

# 9. Service Category 5

# Kubernetes & Amazon EKS Services

This service helps clients design, deploy, secure, and operate containerized platforms using Kubernetes.

---

## Service Owner

```text
Vishal Reddy
Platform Engineer
```

---

## Objectives

* Modernize application platforms
* Improve scalability
* Standardize container operations
* Enable cloud-native adoption

---

## Deliverables

* EKS Cluster Design
* EKS Deployment
* Kubernetes Governance Standards
* Ingress Configuration
* Monitoring Configuration
* Operational Runbooks

---

## Technologies

* Kubernetes
* Amazon EKS
* Docker
* Helm
* ALB Controller
* ExternalDNS

---

## Typical Engagement Duration

```text
3 - 12 Weeks
```

---

## Included Activities

* Cluster Design
* Cluster Deployment
* Security Configuration
* Monitoring Setup
* Operational Handover

---

## Excluded Activities

* Application Refactoring
* Software Development
* Long-Term Platform Operations

---

## Success Criteria

Client receives a production-ready Kubernetes platform with operational documentation and monitoring.

---

# 10. Service Category 6

# Cloud Security Services

Cloud Security Services help clients improve security posture, governance, and compliance readiness.

---

## Service Owner

```text
Nikhil Sharma
Cloud Security Engineer
```

---

## Objectives

* Reduce Security Risk
* Improve Compliance Readiness
* Strengthen Cloud Governance
* Improve Identity Security

---

## Deliverables

* Security Assessment Report
* IAM Review Report
* Security Architecture Review
* Risk Register
* Remediation Recommendations

---

## Technologies

* IAM
* KMS
* Secrets Manager
* Security Hub
* GuardDuty
* CloudTrail

---

## Typical Engagement Duration

```text
1 - 6 Weeks
```

---

## Included Activities

* IAM Assessment
* Security Reviews
* Architecture Reviews
* Compliance Gap Analysis

---

## Excluded Activities

* Penetration Testing
* Managed Security Operations
* Application Security Testing

---

## Success Criteria

Client receives documented findings, remediation plans, and security recommendations.

---

# 11. Service Category 7

# Managed Cloud Operations

Managed Cloud Operations provides ongoing operational support for client cloud environments.

---

## Service Owner

```text
Meera Krishnan
Cloud Operations Lead
```

---

## Objectives

* Improve Reliability
* Reduce Downtime
* Improve Operational Maturity
* Provide Incident Support

---

## Deliverables

* Monitoring Coverage
* Incident Management
* Operational Reviews
* Monthly Reports
* Cost Review Reports

---

## Technologies

* AWS CloudWatch
* Prometheus
* Grafana
* AWS Systems Manager

---

## Typical Engagement Duration

```text
Ongoing Service
```

---

## Included Activities

* Monitoring
* Incident Response
* Alert Management
* Patch Management
* Operational Reviews

---

## Excluded Activities

* Application Development
* Product Feature Support
* Business Process Support

---

## Service Levels

### Standard Support

Coverage:

```text
Business Hours
```

---

### Enhanced Support

Coverage:

```text
24x7 Monitoring
```

---

## Success Criteria

Client infrastructure remains operational, monitored, and supported according to agreed service levels.

---

# 12. Service Category 8

# Cloud Cost Optimization Services

This service helps clients reduce unnecessary cloud spending while maintaining performance and reliability.

---

## Service Owner

```text
Rahul Varma
Principal Platform Engineer
```

---

## Objectives

* Reduce Waste
* Improve Resource Utilization
* Optimize Cloud Spending

---

## Deliverables

* Cost Assessment Report
* Optimization Recommendations
* Savings Forecast
* Resource Inventory

---

## Technologies

* AWS Cost Explorer
* AWS Trusted Advisor
* AWS Compute Optimizer

---

## Typical Engagement Duration

```text
1 - 3 Weeks
```

---

## Included Activities

* Cost Analysis
* Resource Review
* Rightsizing Recommendations
* Savings Identification

---

## Excluded Activities

* Financial Planning
* Accounting Activities

---

## Success Criteria

Client receives actionable recommendations that can reduce cloud expenditure.

---

# 13. Service Category 9

# Cloud Migration Services

Cloud Migration Services help organizations migrate workloads into AWS.

---

## Service Owner

```text
Divya Rajan
Solutions Architect
```

---

## Objectives

* Reduce Migration Risk
* Modernize Infrastructure
* Improve Scalability

---

## Deliverables

* Migration Strategy
* Migration Plan
* Target Architecture
* Risk Assessment
* Cutover Plan

---

## Technologies

* AWS Application Migration Service
* AWS DMS
* AWS Storage Services

---

## Typical Engagement Duration

```text
2 - 16 Weeks
```

---

## Included Activities

* Discovery
* Assessment
* Planning
* Migration Execution
* Validation

---

## Excluded Activities

* Application Re-Architecture
* Software Development

---

## Migration Approaches Supported

* Rehost
* Replatform
* Refactor
* Repurchase
* Retire
* Retain

---

## Success Criteria

Workloads successfully migrated and validated within agreed timelines.

---

# 14. Service Ownership Matrix

| Service                  | Primary Owner  |
| ------------------------ | -------------- |
| Cloud Architecture       | Divya Rajan    |
| AWS Landing Zone         | Rahul Varma    |
| Infrastructure as Code   | Rahul Varma    |
| DevOps Engineering       | Sneha Iyer     |
| Kubernetes & EKS         | Vishal Reddy   |
| Cloud Security           | Nikhil Sharma  |
| Managed Cloud Operations | Meera Krishnan |
| Cost Optimization        | Rahul Varma    |
| Cloud Migration          | Divya Rajan    |

---

# 15. Engagement Delivery Model

InfraGuid follows a standardized delivery model for all service engagements.

```text
Discovery
↓
Assessment
↓
Solution Design
↓
Implementation
↓
Validation
↓
Knowledge Transfer
↓
Project Closure
```

---

## Discovery

Understand client requirements.

---

## Assessment

Evaluate current environment.

---

## Solution Design

Produce architecture and implementation plans.

---

## Implementation

Execute approved work.

---

## Validation

Verify solution functionality.

---

## Knowledge Transfer

Deliver documentation and training.

---

## Project Closure

Formal sign-off and handover.

---

# 16. Governance Statement

This document defines the approved service portfolio offered by InfraGuid Technologies Pvt. Ltd.

No employee may propose, estimate, or deliver services outside the scope of this catalog without approval from the Solutions Architecture team.

The Service Catalog serves as the authoritative reference for:

* Sales Activities
* Solution Design
* Project Planning
* Delivery Governance
* Employee Onboarding

The Solutions Architecture team is responsible for maintaining and updating this document.

---

# 17. Service Qualification Criteria

Every proposed service engagement must be qualified before estimation. Qualification confirms the client objective, business driver, target environments, compliance obligations, migration timeline, required integrations, operational ownership, and success criteria. Sales teams may discuss the catalog at a high level, but solution architects must validate technical feasibility before a delivery commitment is made.

Qualification also determines whether the service is advisory, implementation, or managed operations. Advisory work produces assessments, designs, roadmaps, and decision support. Implementation work produces deployed infrastructure, automation, documentation, and handover artifacts. Managed operations work includes monitoring, incident response, change execution, optimization, and reporting. A statement of work may combine these categories, but each category must have separate deliverables and acceptance criteria.

InfraGuid does not accept engagements that require bypassing security controls, sharing personal credentials, disabling audit logging, storing secrets in source control, or deploying unmanaged production infrastructure. If a client requests a risky pattern, the solution architect documents the risk, proposes a compliant alternative, and escalates if commercial pressure conflicts with engineering standards.

# 18. Discovery Deliverables by Service

Cloud foundation engagements require a current-state inventory, account or subscription model, identity integration requirements, network connectivity plan, tagging taxonomy, logging requirements, backup requirements, and environment promotion model. The discovery output must identify dependencies that can block implementation, such as missing domain ownership, unavailable CIDR ranges, incomplete IAM approvals, or unconfirmed compliance constraints.

Terraform engagements require module inventory, state backend design, provider version strategy, environment layout, CI/CD integration, drift management process, and module ownership. The delivery team must confirm whether existing resources will be imported, recreated, or left unmanaged. Import-heavy engagements include additional planning for state mapping, naming drift, dependency ordering, and rollback.

Managed services onboarding requires an operational readiness review. Required inputs include architecture diagrams, service inventory, monitoring access, incident contacts, change calendar, backup evidence, deployment runbooks, escalation matrix, maintenance windows, and known risks. If these inputs are incomplete, onboarding proceeds through a stabilization phase before normal managed service commitments begin.

# 19. Estimation Standards

Estimates are based on scope, complexity, dependencies, client readiness, review cycles, and operational risk. Engineers estimate implementation effort separately from discovery, documentation, testing, security review, and handover. Terraform module development includes time for input validation, examples, tests, README updates, security scanning, and peer review. Migration estimates include rehearsal, data validation, cutover, rollback planning, and hypercare.

Assumptions must be explicit. Common assumptions include access availability, client stakeholder response time, environment parity, toolchain approval, DNS control, certificate ownership, source repository access, and AWS service quota availability. Any estimate that depends on a client-provided artifact must state the artifact and the date by which it is required.

High-risk items require contingency. Examples include production database migration, IAM redesign, CIDR renumbering, multi-account landing zone remediation, legacy application dependency discovery, and incident-prone workloads. Contingency is not a buffer for poor planning; it is a transparent allowance for known uncertainty.

# 20. Delivery Acceptance Evidence

Acceptance evidence must be objective. For infrastructure services, evidence includes Terraform plan and apply records, resource inventory, tagging validation, encryption validation, security scan results, monitoring dashboard links, backup configuration, and successful health checks. For CI/CD services, evidence includes workflow runs, branch protection settings, artifact retention settings, environment approvals, and rollback demonstration.

For advisory services, acceptance evidence includes completed assessment documents, reviewed architecture diagrams, decision logs, prioritized recommendations, and stakeholder sign-off. Recommendations must identify owner, priority, estimated effort, risk reduced, and dependency. Advisory outputs should be directly usable for implementation planning.

For managed services onboarding, acceptance evidence includes operational handover, alert routing validation, access validation, runbook walkthrough, escalation test, and the first reporting baseline. The baseline establishes the starting point for availability, cost, security, and operational maturity improvements.

# 21. Service Boundaries and Exclusions

The service catalog defines what InfraGuid delivers, but each statement of work defines exact boundaries. Common exclusions include application feature development, business data ownership, client internal approval delays, third-party vendor outages, unmanaged manual changes, and remediation of pre-existing defects outside agreed scope. Exclusions must be discussed during discovery to avoid operational ambiguity.

InfraGuid may support application teams during platform incidents, but application code defects remain the application owner's responsibility unless application support is explicitly included. Platform teams provide infrastructure telemetry, deployment evidence, and dependency health data so application teams can diagnose their services quickly.

Security service boundaries are also explicit. InfraGuid can design controls, implement approved policies, monitor findings, and recommend remediation. The client remains accountable for business risk acceptance unless the managed security agreement assigns that authority differently. No engineer may accept compliance risk on behalf of a client without written authorization from the authorized client stakeholder.

# 22. Service Improvement Loop

Every completed engagement feeds improvements back into the catalog. Delivery teams submit lessons learned, reusable automation, common blockers, revised estimates, and updated acceptance criteria. The Solutions Architecture team reviews these inputs monthly and updates service descriptions, prerequisites, and delivery checklists.

Managed services reports include improvement recommendations. Recommendations are categorized as reliability, security, cost, performance, automation, or documentation. Each recommendation includes expected benefit, estimated effort, priority, and risk of deferral. Accepted recommendations become backlog items and are tracked through completion.

The catalog is reviewed every quarter for obsolete services, new AWS capabilities, internal module changes, pricing shifts, and security policy updates. Services that are no longer aligned with company standards are retired or redesigned before they are sold again.
