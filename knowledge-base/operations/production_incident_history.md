# Production Incident History

Document ID: IG-RCA-001

Version: 1.0

Owner: Arjun Nair (Cloud Operations Lead)

Department: Operations

Classification: Internal Use Only

Review Cycle: Quarterly

Last Updated: June 2026

---

# 1. Purpose

This document serves as the centralized repository of historical production incidents experienced within InfraGuid-managed environments.

The objective of maintaining a centralized incident history is to:

- Preserve organizational knowledge
- Accelerate future troubleshooting
- Improve incident response effectiveness
- Prevent recurrence of known failures
- Support Root Cause Analysis activities
- Improve architecture and operational standards

This document should be consulted whenever:

- Similar symptoms occur
- Major incidents occur
- Architectural changes are proposed
- Post-incident reviews are performed

---

# 2. Scope

This document contains:

- Production Incidents
- Major Service Disruptions
- Security Incidents
- Infrastructure Failures
- Network Failures
- Deployment Failures

Only incidents that resulted in:

- Customer Impact
- Service Degradation
- Security Risk
- Business Impact

should be recorded.

---

# 3. Incident Severity Definitions

## Severity 1

Critical business impact.

Examples:

- Complete service outage
- Production unavailable
- Security breach

---

## Severity 2

Major degradation.

Examples:

- Significant customer impact
- Partial outage

---

## Severity 3

Limited impact.

Examples:

- Non-critical service degradation

---

## Severity 4

Minimal impact.

Examples:

- Internal operational issues

---

# 4. RCA Standard Template

All incidents recorded within this document must follow the structure below.

## Incident Information

Incident ID:

Severity:

Date:

Environment:

Affected Services:

Incident Commander:

---

## Business Impact

Describe:

- Customer Impact
- Operational Impact
- Financial Impact

---

## Timeline

Document:

Detection

Escalation

Investigation

Mitigation

Recovery

Closure

---

## Detection

How was the incident detected?

Examples:

- CloudWatch Alert
- Customer Report
- Security Alert

---

## Root Cause

Document:

Primary Cause

Contributing Factors

---

## Resolution

How was service restored?

---

## Corrective Actions

Immediate improvements.

---

## Preventive Actions

Long-term improvements.

---

## Lessons Learned

Operational and architectural lessons.

---

# RCA-001 — Route Table Misconfiguration Causing Production Application Outage

---

## Incident Information

### Incident ID

RCA-001

---

### Incident Title

Route Table Misconfiguration Causing Production Application Outage

---

### Severity

Sev-1

---

### Date

2025-08-14

---

### Environment

Production

---

### Affected Client

FinTrust Capital Services

---

### AWS Region

ap-south-1

---

### Incident Commander

Arjun Nair

Cloud Operations Lead

---

### Technical Lead

Rahul Varma

Principal Platform Engineer

---

### Services Affected

- Amazon VPC
- Private Subnets
- NAT Gateway
- Application Load Balancer
- EC2 Auto Scaling Group
- Amazon RDS PostgreSQL
- Amazon CloudWatch
- Route53

---

### Duration

1 Hour 47 Minutes

---

### Start Time

09:13 IST

---

### End Time

11:00 IST

---

## Executive Summary

A production outage occurred after a Terraform deployment introduced an incorrect route table association within the production VPC.

The deployment unintentionally associated a private application subnet with a route table intended for isolated database subnets.

As a result:

- Application servers lost outbound internet connectivity
- Systems Manager connectivity failed
- Third-party payment APIs became unreachable
- Authentication requests failed
- Application health checks began failing

Although application servers remained operational, the application was unable to communicate with required external services.

The Application Load Balancer began marking targets as unhealthy, eventually causing customer-facing service degradation and outage conditions.

The issue persisted until the incorrect route table association was identified and corrected.

---

# Business Impact

## Customer Impact

Customers experienced:

- Login Failures
- Payment Processing Failures
- Session Validation Errors
- Dashboard Loading Failures

Approximately:

```text
3,200 Active Users
```

were impacted during the incident.

---

## Operational Impact

Operations teams were unable to:

- Access affected servers through Session Manager
- Execute automated deployment workflows
- Perform routine operational tasks

Engineering teams required emergency troubleshooting procedures.

---

## Financial Impact

Estimated impact:

```text
Approximately ₹4.2 Lakhs
```

in delayed transactions and client SLA penalties.

---

## Reputational Impact

The client reported:

- Increased support tickets
- Customer complaints
- Executive escalation

A formal incident review was requested by client leadership.

---

# Architecture Overview

The affected architecture consisted of:

```text
Internet
    │
CloudFront
    │
Application Load Balancer
    │
Private Application Subnets
    │
EC2 Auto Scaling Group
    │
Amazon RDS PostgreSQL
```

Outbound connectivity for application servers utilized:

```text
Private Subnets
     │
NAT Gateway
     │
Internet Gateway
```

The outage occurred when the private subnet lost its route to the NAT Gateway.

---

# Timeline

## 09:13 IST

Terraform deployment initiated.

Deployment objective:

```text
Introduce new isolated subnet tier
for future analytics workloads.
```

Deployment approved under:

```text
Normal Change Process
```

---

## 09:18 IST

Terraform Apply completed successfully.

No errors reported.

Infrastructure validation not yet started.

---

## 09:20 IST

CloudWatch alarms triggered.

Alerts:

```text
Application Error Rate Increased

Payment API Timeout

Authentication Failures
```

Operations engineer acknowledged alarms.

---

## 09:24 IST

Customer support team reported login failures.

Multiple users unable to authenticate.

---

## 09:28 IST

Incident declared.

Severity:

```text
Sev-2
```

Initial assumption:

```text
Third Party Authentication Provider Failure
```

---

## 09:35 IST

Application logs reviewed.

Errors:

```text
Connection Timeout

Request Timed Out

Unable To Reach Authentication Service
```

---

## 09:41 IST

Additional alerts triggered.

ALB health checks began failing.

Targets progressively marked unhealthy.

---

## 09:45 IST

Severity upgraded:

```text
Sev-1
```

War room initiated.

---

## 09:48 IST

Platform Engineering joined incident.

Investigation focused on:

- ALB
- Application
- Authentication Service

---

## 09:53 IST

Authentication provider verified healthy.

External dependency ruled out.

---

## 10:01 IST

EC2 instances inspected.

Observation:

```text
Instances Healthy

Application Running

Database Reachable
```

Unexpected finding:

```text
Internet Connectivity Failed
```

---

## 10:06 IST

Attempted:

```bash
curl https://google.com
```

from application server.

Result:

```text
Connection Timeout
```

---

## 10:09 IST

Network investigation initiated.

Review:

- Security Groups
- NACLs
- Route Tables

---

## 10:15 IST

Security Groups validated.

No issues found.

---

## 10:21 IST

NACLs validated.

No issues found.

---

## 10:27 IST

Route table review identified anomaly.

Application subnet associated with:

```text
rtb-prod-isolated
```

instead of:

```text
rtb-prod-private
```

---

## 10:31 IST

Terraform state reviewed.

Recent deployment contained:

```hcl
aws_route_table_association
```

modification.

---

## 10:35 IST

Root cause identified.

Incorrect route table association introduced during deployment.

---

## 10:38 IST

Emergency change approved.

---

## 10:41 IST

Correct route table association restored.

---

## 10:44 IST

Outbound connectivity restored.

Verification:

```bash
curl https://google.com
```

successful.

---

## 10:47 IST

Authentication requests successful.

---

## 10:51 IST

Payment processing restored.

---

## 10:55 IST

ALB health checks recovered.

Targets marked healthy.

---

## 11:00 IST

Incident resolved.

Monitoring stabilized.

War room closed.

---

# Detection

## Initial Detection Method

Detected by:

```text
CloudWatch Alarms
```

Specifically:

- Application Error Rate Alarm
- Payment Failure Alarm
- Authentication Failure Alarm

---

## Secondary Detection

Customer reports submitted through support portal.

---

## Monitoring Gaps Identified

Existing monitoring detected symptoms but not root cause.

Missing alerts:

```text
Subnet Route Table Changes

Route Association Drift

NAT Connectivity Validation
```

---

# Technical Investigation

## Phase 1

Application Investigation

Initial assumptions focused on:

- Application failure
- Authentication provider outage

No evidence found.

---

## Phase 2

Load Balancer Investigation

Review findings:

```text
ALB Healthy

Listeners Healthy

Certificates Valid
```

Targets became unhealthy because applications failed dependency checks.

ALB was not root cause.

---

## Phase 3

Infrastructure Investigation

EC2 findings:

```text
CPU Normal

Memory Normal

Disk Normal
```

Applications operational.

---

## Phase 4

Network Investigation

Network path reviewed:

```text
EC2
↓
Route Table
↓
NAT Gateway
↓
Internet Gateway
```

Issue isolated to routing layer.

---

# Root Cause

## Primary Root Cause

Incorrect route table association introduced through Terraform deployment.

Application subnet:

```text
subnet-prod-app-a
```

was associated with:

```text
rtb-prod-isolated
```

instead of:

```text
rtb-prod-private
```

---

## Why This Caused Failure

The isolated route table contained:

```text
Local Route Only
```

and no:

```text
0.0.0.0/0 → NAT Gateway
```

route.

Consequently:

- Internet access failed
- External APIs became unreachable
- Session Manager failed
- Authentication requests failed

---

## Contributing Factor 1

Terraform review focused on resource creation.

Reviewers missed:

```text
Route Table Association Change
```

inside plan output.

---

## Contributing Factor 2

No automated validation existed for:

```text
Subnet Route Table Compliance
```

---

## Contributing Factor 3

No post-deployment connectivity testing.

---

# Resolution

## Immediate Fix

Restored correct route table association.

Terraform updated:

```text
subnet-prod-app-a

↓

rtb-prod-private
```

---

## Validation Performed

Validated:

```text
Outbound Connectivity

Authentication

Payment Processing

Monitoring

ALB Health
```

---

## Service Recovery

Service fully restored.

No data loss occurred.

---

# Corrective Actions

## CA-001

Introduce mandatory route table review checklist.

Owner:

Platform Engineering

Target:

Completed

---

## CA-002

Enhance Terraform PR review process.

Require explicit validation of:

```text
Route Tables

Security Groups

IAM Changes
```

---

## CA-003

Create automated network validation script.

Validate:

```text
Internet Connectivity

DNS Resolution

NAT Access
```

after deployment.

---

# Preventive Actions

## PA-001

AWS Config Rule

Detect:

```text
Unexpected Route Table Associations
```

---

## PA-002

Terraform Policy Validation

Prevent:

```text
Unauthorized Route Table Changes
```

---

## PA-003

CloudWatch Synthetic Monitoring

Validate:

```text
Authentication Endpoint

Payment Endpoint

External Dependencies
```

---

## PA-004

Production Deployment Checklist Update

New validation step:

```text
Outbound Connectivity Test
```

mandatory.

---

## PA-005

Architecture Standards Update

Route table modifications reclassified as:

```text
High Risk Change
```

requiring Architect approval.

---

# Lessons Learned

## Lesson 1

A successful Terraform deployment does not imply a correct deployment.

Infrastructure validation must occur after every deployment.

---

## Lesson 2

Route table modifications represent high operational risk.

Network changes require enhanced review.

---

## Lesson 3

Monitoring should detect root causes, not only symptoms.

Additional network-level monitoring was necessary.

---

## Lesson 4

Post-deployment validation procedures were insufficient.

Connectivity testing must be automated.

---

## Lesson 5

Terraform plan reviews require structured review processes.

Critical networking resources should never rely solely on manual inspection.

---

# Final Outcome

Service Availability Restored:

```text
100%
```

---

Data Loss:

```text
None
```

---

Customer Impact:

```text
Resolved
```

---

Corrective Actions:

```text
Completed
```

---

Preventive Actions:

```text
Implemented
```

---

Incident Status:

```text
Closed
```

# RCA-002 — Application Load Balancer Health Check Failure Following Application Release

---

## Incident Information

### Incident ID

RCA-002

---

### Incident Title

Application Load Balancer Health Check Failure Following Production Application Release

---

### Severity

Sev-1

---

### Date

2025-11-07

---

### Environment

Production

---

### Affected Client

NovaRetail Commerce Platform

---

### AWS Region

ap-south-1

---

### Incident Commander

Arjun Nair

Cloud Operations Lead

---

### Technical Lead

Sneha Iyer

Senior DevOps Engineer

---

### Services Affected

- Application Load Balancer
- EC2 Auto Scaling Group
- Route53
- CloudWatch
- CloudFront
- Payment Service API
- Customer Portal

---

### Duration

58 Minutes

---

### Start Time

14:02 IST

---

### End Time

15:00 IST

---

## Executive Summary

A production outage occurred following deployment of application release version:

```text
v3.18.0
```

The release introduced a new authentication middleware layer that unintentionally modified the behavior of the application health endpoint.

Prior to deployment:

```text
GET /health
```

returned:

```http
HTTP 200 OK
```

without authentication.

Following deployment:

```text
GET /health
```

required JWT authentication.

The Application Load Balancer health checks did not include authentication headers.

As a result:

```text
ALB Health Check

↓

HTTP 401 Unauthorized

↓

Targets Marked Unhealthy

↓

Traffic Stopped
```

Although application servers remained fully operational, the ALB removed all instances from service because health checks failed.

The incident resulted in complete application unavailability until the deployment was rolled back.

---

# Business Impact

## Customer Impact

Customers experienced:

- Login Failures
- Checkout Failures
- Payment Interruptions
- Session Timeouts

---

Approximately:

```text
5,400 Active Users
```

were impacted.

---

## Operational Impact

Operations teams received:

```text
180+
```

support tickets during the incident.

---

## Financial Impact

Estimated:

```text
₹6.8 Lakhs
```

in delayed and abandoned transactions.

---

## SLA Impact

Client SLA violation occurred.

Formal incident review requested.

---

# Architecture Overview

Affected architecture:

```text
Route53
   │
CloudFront
   │
Application Load Balancer
   │
Target Group
   │
EC2 Auto Scaling Group
   │
Application
```

Health check configuration:

```text
Path: /health

Protocol: HTTP

Expected Code: 200
```

---

# Timeline

## 13:45 IST

Deployment window opened.

Release:

```text
v3.18.0
```

approved.

---

## 13:52 IST

Deployment initiated.

Blue-green deployment strategy used.

---

## 13:58 IST

Deployment completed successfully.

Pipeline reported:

```text
Success
```

---

## 14:02 IST

CloudWatch alarms triggered.

Alerts:

```text
Healthy Host Count Decreasing
```

---

## 14:04 IST

Additional alarms triggered.

```text
HTTP 5XX Errors Increasing
```

---

## 14:06 IST

Customer reports received.

Users unable to access portal.

---

## 14:08 IST

Incident declared.

Severity:

```text
Sev-1
```

---

## 14:11 IST

War room initiated.

---

## 14:15 IST

Initial review focused on:

- ALB
- Auto Scaling
- EC2 Health

---

## 14:20 IST

Infrastructure appeared healthy.

Observations:

```text
Instances Running

CPU Normal

Memory Normal
```

---

## 14:23 IST

Target Group review performed.

Finding:

```text
All Targets Unhealthy
```

---

## 14:27 IST

Health check failures identified.

ALB response:

```http
401 Unauthorized
```

---

## 14:30 IST

Application logs reviewed.

Discovery:

```text
Health Endpoint Protected
By Authentication Middleware
```

---

## 14:34 IST

Deployment team engaged.

Recent code changes reviewed.

---

## 14:38 IST

Root cause identified.

Authentication middleware included:

```text
/health
```

endpoint.

---

## 14:41 IST

Rollback approved.

---

## 14:44 IST

Rollback initiated.

---

## 14:50 IST

Rollback completed.

---

## 14:53 IST

Health checks passing.

---

## 14:56 IST

Targets healthy.

---

## 14:58 IST

Customer traffic restored.

---

## 15:00 IST

Incident resolved.

---

# Detection

## Initial Detection

Detected through:

```text
CloudWatch Alarm
```

Alarm:

```text
Healthy Host Count < Threshold
```

---

## Secondary Detection

Customer reports.

---

## Monitoring Gaps

Monitoring detected:

```text
ALB Failure
```

but did not identify:

```text
Health Endpoint Response Change
```

---

# Technical Investigation

## Phase 1

Infrastructure Validation

Reviewed:

```text
EC2

Auto Scaling

Security Groups

Target Groups
```

No infrastructure issues found.

---

## Phase 2

ALB Investigation

Review:

```text
Target Health Status
```

Finding:

```text
Unhealthy
```

for all targets.

---

## Phase 3

Health Check Analysis

ALB health check response:

```http
401 Unauthorized
```

Expected:

```http
200 OK
```

---

## Phase 4

Application Review

Application logs indicated:

```text
Authentication Required
```

for health endpoint.

---

## Phase 5

Code Review

Deployment introduced:

```text
Authentication Middleware Refactor
```

New middleware unintentionally protected:

```text
/health
```

endpoint.

---

# Root Cause

## Primary Root Cause

Application deployment modified health endpoint behavior.

Health endpoint became protected by authentication middleware.

---

## Why This Caused Outage

ALB health checks do not perform authentication.

Therefore:

```text
Health Check

↓

401 Response

↓

Target Unhealthy

↓

Traffic Removed
```

---

## Contributing Factor 1

Health endpoint behavior not documented.

---

## Contributing Factor 2

Release validation did not test:

```text
Unauthenticated Health Endpoint
```

---

## Contributing Factor 3

No deployment guardrails existed for health check paths.

---

## Contributing Factor 4

Blue-green validation focused on business functionality.

Health checks were not independently verified.

---

# Resolution

## Immediate Resolution

Rollback deployment.

Restore previous version.

---

## Validation

Verified:

```text
Health Endpoint

Authentication

Customer Access

Payment Processing
```

---

## Service Recovery

Traffic restored successfully.

No data loss occurred.

---

# Corrective Actions

## CA-001

Create dedicated:

```text
/healthz
```

endpoint.

Always public.

---

## CA-002

Health endpoints excluded from authentication middleware.

---

## CA-003

Application architecture standards updated.

---

## CA-004

Deployment checklist updated.

New validation step:

```text
ALB Health Check Validation
```

---

# Preventive Actions

## PA-001

Automated deployment test.

Validate:

```http
GET /healthz

Expected:
HTTP 200
```

---

## PA-002

Synthetic monitoring.

Validate health endpoint every minute.

---

## PA-003

CI/CD validation rule.

Reject deployments modifying:

```text
Health Check Paths
```

without approval.

---

## PA-004

Architecture review requirement.

Health endpoint changes classified as:

```text
High Risk Change
```

---

## PA-005

ALB monitoring enhancement.

Alert when:

```text
Healthy Host Count
Drops Rapidly
```

---

# Lessons Learned

## Lesson 1

Application health endpoints are critical infrastructure dependencies.

---

## Lesson 2

Successful deployment does not guarantee successful service registration.

---

## Lesson 3

Health check validation should be treated as a production-critical control.

---

## Lesson 4

Middleware changes can have infrastructure impact.

---

## Lesson 5

Blue-green deployments still require comprehensive validation.

---

# Final Outcome

Service Availability:

```text
100% Restored
```

---

Data Loss:

```text
None
```

---

Customer Impact:

```text
Resolved
```

---

Corrective Actions:

```text
Implemented
```

---

Preventive Actions:

```text
Implemented
```

---

Incident Status:

```text
Closed
```

# RCA-003 — Security Group Misconfiguration Blocking Database Connectivity

---

## Incident Information

### Incident ID

RCA-003

---

### Incident Title

Security Group Misconfiguration Blocking Database Connectivity

---

### Severity

Sev-1

---

### Date

2026-01-18

---

### Environment

Production

---

### Affected Client

RetailOne Digital Commerce

---

### AWS Region

ap-south-1

---

### Incident Commander

Arjun Nair

Cloud Operations Lead

---

### Technical Lead

Sneha Iyer

Senior DevOps Engineer

---

### Services Affected

- Amazon RDS PostgreSQL
- EC2 Application Servers
- Application Load Balancer
- CloudWatch
- Customer Portal
- Internal APIs

---

### Duration

1 Hour 22 Minutes

---

## Executive Summary

A production outage occurred after a Terraform deployment modified database security group rules.

The change was intended to remove unused ingress rules and standardize security group configurations.

During deployment, an application security group reference was accidentally removed from the database security group.

As a result:

```text
Application Servers

↓

Database Connection Denied

↓

Application Failure

↓

Customer Impact
```

The database remained healthy throughout the incident.

The outage occurred because application servers could no longer establish TCP connections to PostgreSQL.

---

# Business Impact

## Customer Impact

Customers experienced:

- Login Failures
- Checkout Failures
- Account Access Errors

Approximately:

```text
4,800 Active Users
```

affected.

---

## Operational Impact

Applications became unavailable despite healthy infrastructure.

Operations teams initially suspected database failure.

---

## Financial Impact

Estimated:

```text
₹5.1 Lakhs
```

in delayed transactions.

---

# Timeline

## 10:02 IST

Terraform deployment started.

---

## 10:08 IST

Deployment completed successfully.

---

## 10:11 IST

Application error rates increased.

---

## 10:13 IST

CloudWatch alarms triggered.

---

## 10:18 IST

Customer reports received.

---

## 10:20 IST

Incident declared.

Severity:

```text
Sev-1
```

---

## 10:31 IST

Database reviewed.

Finding:

```text
Healthy
```

---

## 10:39 IST

Application logs reviewed.

Errors:

```text
Connection Refused

Database Timeout

Unable To Connect
```

---

## 10:47 IST

Network investigation initiated.

---

## 10:55 IST

Security group comparison performed.

---

## 11:02 IST

Root cause identified.

Application Security Group reference removed.

---

## 11:08 IST

Emergency change approved.

---

## 11:14 IST

Security group restored.

---

## 11:22 IST

Applications recovered.

---

## 11:30 IST

Incident resolved.

---

# Root Cause

Database security group ingress rule removed during Terraform deployment.

Previous:

```text
Application-SG

↓

Database-SG

TCP 5432
```

After deployment:

```text
Application-SG Access Removed
```

Result:

```text
Database Healthy

↓

Application Cannot Connect
```

---

# Resolution

Restored security group ingress rule.

Validated:

```text
Database Connectivity

Application Health

Customer Transactions
```

---

# Corrective Actions

- Security Group Change Checklist
- Terraform Review Enhancement
- Connectivity Validation Tests

---

# Preventive Actions

- Automated Database Connectivity Tests
- Terraform Policy Controls
- Security Group Drift Detection

---

# Lessons Learned

- Healthy databases can still cause outages through network misconfiguration.
- Security group modifications require enhanced review.
- Connectivity validation must be automated.

---

# Final Outcome

```text
Data Loss: None

Customer Impact: Resolved

Status: Closed
```

---

# RCA-004 — ChromaDB Service Failure Causing AI Assistant Outage

---

## Incident Information

### Incident ID

RCA-004

---

### Severity

Sev-2

---

### Date

2026-03-09

---

### Environment

Production

---

### Affected Service

InfraGuid Knowledge Assistant

---

### Duration

2 Hours 11 Minutes

---

## Executive Summary

The InfraGuid Knowledge Assistant experienced degraded functionality after the ChromaDB service became unavailable.

Users could still access the application interface but AI responses failed because retrieval operations could not complete.

The outage exposed a dependency weakness within the AI platform architecture.

---

# Business Impact

Users experienced:

- Failed AI Responses
- Missing Context Retrieval
- Increased Response Latency

Approximately:

```text
85 Employees
```

affected.

---

# Architecture

```text
User
↓
AI Assistant
↓
Retriever
↓
ChromaDB
↓
Embeddings
```

Failure occurred at:

```text
ChromaDB Layer
```

---

# Timeline

## 09:12 IST

First user reports received.

---

## 09:15 IST

Monitoring alerts triggered.

---

## 09:21 IST

Incident declared.

Severity:

```text
Sev-2
```

---

## 09:34 IST

Application logs reviewed.

---

## 09:49 IST

ChromaDB health endpoint failing.

---

## 10:02 IST

Storage errors identified.

---

## 10:18 IST

Persistent volume corruption suspected.

---

## 10:44 IST

Backup restoration initiated.

---

## 11:07 IST

Service restored.

---

## 11:23 IST

Validation completed.

---

# Detection

Detected through:

```text
Application Errors

Employee Reports

Health Check Alerts
```

---

# Technical Investigation

Review revealed:

```text
Vector Database Process Failure
```

Following node restart:

```text
Index Files Failed Validation
```

---

# Root Cause

Underlying storage corruption caused ChromaDB startup failure.

As a result:

```text
Retriever

↓

No Vector Search

↓

AI Responses Failed
```

---

# Resolution

Actions:

```text
Restore Snapshot

Rebuild Index

Validate Collections
```

---

# Corrective Actions

- Add ChromaDB Health Monitoring
- Backup Verification Process
- Recovery Testing

---

# Preventive Actions

- Daily Snapshot Validation
- Replica Deployment
- Index Integrity Monitoring

---

# Lessons Learned

- AI systems require the same operational rigor as traditional applications.
- Retrieval layer failures should degrade gracefully.
- Backup restoration should be tested regularly.

---

# Final Outcome

```text
Data Loss: None

Service Restored

Status: Closed
```

---

# RCA-005 — IAM Permission Failure Breaking Production Deployments

---

## Incident Information

### Incident ID

RCA-005

---

### Severity

Sev-2

---

### Date

2026-04-17

---

### Environment

Production

---

### Duration

3 Hours 04 Minutes

---

## Executive Summary

Production deployments failed after a newly introduced IAM permission boundary prevented CI/CD roles from performing required deployment actions.

The issue did not impact customer traffic directly but prevented all production releases.

---

# Business Impact

Impact:

```text
Production Deployments Blocked

Emergency Fix Delayed

Release Window Missed
```

---

# Timeline

## 13:04 IST

Permission boundary deployed.

---

## 13:17 IST

Production deployment initiated.

---

## 13:20 IST

Pipeline failed.

---

## 13:28 IST

Retry failed.

---

## 13:41 IST

Incident declared.

---

## 14:05 IST

IAM investigation initiated.

---

## 14:39 IST

Permission boundary identified.

---

## 15:11 IST

Corrected policy deployed.

---

## 16:08 IST

Deployments restored.

---

# Detection

Detected through:

```text
GitHub Actions Failure

Terraform Failure

Deployment Alerts
```

---

# Technical Investigation

Deployment role:

```text
InfraGuid-Prod-Deploy-Role
```

attempted:

```text
iam:PassRole
```

operation.

Denied by:

```text
Permission Boundary
```

introduced during security hardening.

---

# Root Cause

Security team introduced a new permission boundary.

The boundary unintentionally blocked:

```text
iam:PassRole

ecs:UpdateService

eks:DescribeCluster
```

required by deployment workflows.

---

# Resolution

Updated boundary.

Validated:

```text
Terraform Apply

GitHub Actions

Deployment Pipeline
```

---

# Corrective Actions

- IAM Change Review Process
- Deployment Role Testing
- Policy Simulation Validation

---

# Preventive Actions

- Automated IAM Regression Testing
- Permission Boundary Validation
- Pre-Production IAM Testing

---

# Lessons Learned

- Security improvements can create operational failures.
- IAM changes should be treated as high-risk changes.
- Permission simulation should be mandatory before deployment.

---

# Final Outcome

```text
Customer Impact: None

Deployment Capability Restored

Status: Closed
```

# 5. Incident Trend Analysis

This section is updated quarterly by the Operations Team and provides visibility into recurring operational risks observed across InfraGuid-managed environments.

The objective is to identify:

- Recurring Failure Patterns
- High-Risk Services
- Operational Weaknesses
- Security Trends
- Improvement Opportunities

---

## 5.1 Incident Distribution by Category

| Category | Incident Count |
|-----------|-----------|
| Networking | 2 |
| Load Balancing | 1 |
| IAM | 1 |
| AI Platform | 1 |
| Database | 0 |
| Security | 0 |

---

## 5.2 Most Common Failure Domains

### Networking

Observed in:

```text
RCA-001

RCA-003
```

Failures involved:

- Route Tables
- Security Groups

Networking remains the highest operational risk area.

---

### Configuration Changes

Observed in:

```text
RCA-001

RCA-002

RCA-003

RCA-005
```

Over 80% of incidents originated from configuration changes.

---

### Deployment Related Failures

Observed in:

```text
RCA-001

RCA-002

RCA-003

RCA-005
```

Most incidents occurred within:

```text
30 Minutes
```

of deployment activities.

---

## 5.3 Root Cause Trends

### Category 1

Infrastructure Misconfiguration

Examples:

```text
Route Tables

Security Groups

IAM Policies
```

---

### Category 2

Validation Gaps

Examples:

```text
Health Checks

Connectivity Testing

Permission Testing
```

---

### Category 3

Insufficient Guardrails

Examples:

```text
Terraform Validation

Policy Validation

Monitoring Coverage
```

---

## 5.4 Lessons Repeated Across Multiple Incidents

Recurring lessons identified:

### Lesson 1

Successful deployment does not guarantee successful operation.

---

### Lesson 2

Infrastructure validation must occur after every deployment.

---

### Lesson 3

Critical networking changes require enhanced review.

---

### Lesson 4

Monitoring should identify root causes, not only symptoms.

---

### Lesson 5

Automated validation is more reliable than manual validation.

---

# 6. Standard Corrective Action Library

The following actions have proven effective across multiple incidents.

Engineers should consider these controls when designing new environments.

---

## Network Changes

Required:

```text
Connectivity Validation

Route Validation

Security Group Validation
```

---

## Load Balancer Changes

Required:

```text
Health Check Validation

Target Group Validation

Synthetic Monitoring
```

---

## IAM Changes

Required:

```text
Policy Simulation

Permission Testing

Pipeline Validation
```

---

## AI Platform Changes

Required:

```text
Backup Validation

Recovery Testing

Dependency Monitoring
```

---

# 7. Organizational Recommendations

Based on historical incident data, InfraGuid recommends the following operational improvements.

---

## Recommendation 1

Expand automated validation coverage.

---

## Recommendation 2

Increase deployment guardrails.

---

## Recommendation 3

Treat networking changes as high-risk changes.

---

## Recommendation 4

Implement broader synthetic monitoring.

---

## Recommendation 5

Conduct quarterly incident review workshops.

---

# 8. Document Maintenance Process

The Operations Team owns this document.

Updates must occur:

```text
After Every Sev-1 Incident

After Every Sev-2 Incident

Quarterly Review Cycle
```

---

## Required Updates

For every new incident:

```text
Add RCA

Update Trends

Update Lessons Learned

Update Recommendations
```

---

# 9. Governance Statement

This document serves as the official historical incident repository for InfraGuid Technologies Pvt. Ltd.

Its purpose is to preserve organizational memory and accelerate future incident resolution.

All Sev-1 and Sev-2 incidents must be documented in this repository.

All Root Cause Analyses must follow the approved RCA structure defined in this document.

The Operations Team is responsible for maintaining the accuracy and completeness of this repository.

Engineers are expected to consult this document when:

```text
Investigating Incidents

Performing Architecture Reviews

Designing New Platforms

Implementing Corrective Actions

Planning Operational Improvements
```

This document represents the authoritative source of historical production incident knowledge across all InfraGuid-managed environments.

---

# Cross-Incident Pattern Analysis

## Pattern 1: Change Validation Gaps

Several incidents were triggered by infrastructure changes that passed basic checks but failed operational validation. Route table changes, security group dependencies, CloudFront invalidation failures, and DNS migration issues all show that a successful plan or API call is not enough. Production changes require post-change validation tied to the real user path. For network changes, validation includes egress tests from private subnets, route table inspection, NAT Gateway health, VPC Flow Log sampling, and application dependency checks. For CDN changes, validation includes invalidation status, cache behavior inspection, asset version checks, and error-rate monitoring.

Corrective action across these incidents is to make validation explicit in deployment pipelines. Terraform plans must be reviewed for high-risk resource classes such as route tables, security groups, IAM policies, DNS records, and load balancer target groups. After apply, pipelines must run service-specific smoke tests. If a smoke test fails, the pipeline must stop promotion and notify the owning team. Manual validation steps are acceptable only when they are documented, assigned, and captured as evidence.

The operations team maintains a high-risk change checklist. The checklist requires confirmation of rollback method, blast radius, monitoring dashboard, expected metric movement, and emergency contact. High-risk changes should be scheduled during approved deployment windows unless they are incident mitigations. The incident commander may approve emergency exceptions, but those exceptions must be reviewed in the post-incident process.

## Pattern 2: Missing Quota and Capacity Guardrails

The ChromaDB disk-full incident and Bedrock throttling incident exposed missing quota controls. Capacity issues rarely fail gracefully when they affect core dependencies. Vector storage, model invocation limits, database connection pools, CloudFront invalidation quotas, and runner capacity must be monitored before they hit hard limits. Engineering teams must treat quota as part of architecture, not as an afterthought.

Preventive controls include service quota dashboards, budget alerts, storage utilization alerts, request-rate alerts, and load-test environment isolation. Bedrock workloads must use request throttling, retry with backoff, and environment-specific quotas. Load tests must never target production without written approval, a defined traffic envelope, and a rollback or stop procedure. Test plans must identify all managed service quotas that may be consumed.

Capacity reviews are required monthly for managed services clients. The review checks growth trends, saturation risks, quota utilization, pending migrations, and upcoming load events. Findings are converted into backlog items with owners and due dates. Critical capacity findings are escalated through the same path as reliability risks.

## Pattern 3: Dependency Readiness and Race Conditions

The EFS mount race condition demonstrates that infrastructure dependencies may exist in Terraform state before they are ready for application use. Similar issues can occur with DNS propagation, ACM certificate validation, ALB target registration, RDS failover, ECS service stabilization, and CloudFront deployment propagation. Readiness checks must verify operational availability, not only resource creation.

User data scripts and bootstrap automation must include dependency retries with clear timeouts. An EC2 instance should not fail permanently because an EFS mount target needed additional time to become reachable. Bootstrap scripts should log each dependency check, retry with backoff, and surface failure in CloudWatch logs. Auto Scaling replacement policies must account for stabilization time to avoid repeated churn.

Terraform modules should expose readiness-relevant outputs such as DNS names, security group IDs, target group ARNs, and health check paths. Deployment pipelines should wait for service-specific stabilization signals. For example, CloudFront distributions must reach deployed status, ECS services must reach steady state, and ALB target groups must report healthy targets before promotion is considered complete.

## Pattern 4: IAM and Secret Access Fragility

The missing Lambda permission incident shows the need for contract tests around IAM access. IAM policies may look correct during review but still fail at runtime because ARN patterns, conditions, KMS permissions, or secret naming conventions do not match the application behavior. Permission changes must be tested with the workload identity that will run in production.

Approved IAM modules should include least-privilege examples for Secrets Manager, KMS, CloudWatch Logs, S3, DynamoDB, RDS IAM authentication, Bedrock, and EventBridge. Teams must avoid broad wildcard permissions to bypass testing. If wildcard permissions are used temporarily during incident mitigation, they must have an expiry action and follow-up review.

Secret access validation includes reading the expected secret version, decrypting with the configured KMS key, verifying rotation configuration, and confirming application startup with the production role. Failed secret access should produce actionable logs that include secret identifier pattern, role name, and missing permission category without exposing secret values.

## Pattern 5: State and Drift Management

The Terraform state lock incident and circular dependency incident demonstrate how infrastructure state can become an operational dependency during outages. State locks, partial applies, provider errors, and drift can block urgent remediation. Teams must know how to inspect state safely, release stale locks with approval, and reconcile partial configuration without deleting production resources unintentionally.

State lock release requires evidence that no active apply is running. The approving engineer checks pipeline status, runner activity, DynamoDB lock metadata, and team communication channels. The lock is released only after the change owner and platform lead agree. The release command is recorded in the incident timeline and follow-up action verifies that the next plan is clean.

Drift detection runs on a scheduled basis for managed environments. Drift findings are categorized as expected external change, emergency change requiring reconciliation, unmanaged resource, or unauthorized modification. Unauthorized modifications are escalated to security and operations leadership. Reconciliation must prefer importing or updating Terraform code over manual correction when possible.

# Standard Corrective Action Backlog Themes

## Validation Automation

All service teams must convert repeated manual checks into automated validation. Deployment validation should include health endpoint checks, dependency checks, synthetic transactions, log error scans, and dashboard review. Validation scripts are stored with the service repository and run from CI/CD. The script output becomes deployment evidence.

## Runbook Precision

Runbooks must include commands, expected outputs, rollback triggers, and escalation thresholds. A runbook that says "check CloudWatch" is not sufficient. It should identify the dashboard, metric, namespace, time range, alarm, and interpretation. During incidents, vague runbooks increase cognitive load and slow restoration.

## Ownership Clarity

Each corrective action needs a named owner and due date. Ownership cannot be assigned to a generic team mailbox. The owner is accountable for progress, evidence, and closure. Managers review overdue corrective actions weekly. Repeated overdue actions from the same category are escalated as operational risk.

## Environment Isolation

Load tests, chaos tests, and migration rehearsals should run in isolated environments unless production testing is explicitly required. Production tests must have a defined start time, end time, maximum traffic, stop condition, communication plan, and monitoring owner. Test traffic should be identifiable through headers, source IPs, tags, or logs.

## Observability Improvements

Incident reviews must identify whether the issue was detected by monitoring, user report, deployment validation, or manual inspection. If users detected the issue first, monitoring coverage is incomplete. New alerts should be actionable and routed to the right team. Alert thresholds must avoid noise while still detecting meaningful service risk.

# Incident Review Metrics

InfraGuid tracks mean time to detect, mean time to acknowledge, mean time to mitigate, mean time to resolve, corrective action closure rate, repeat incident count, and customer-impact minutes. These metrics are reviewed monthly by operations leadership. The purpose is not to rank individuals but to identify systemic weaknesses in architecture, automation, monitoring, and process.

Repeat incidents receive additional scrutiny. If the same failure mode recurs after a corrective action was marked complete, the action was either insufficient, not implemented correctly, or not applied broadly enough. The review must determine whether the failure was local to one service or represents a company-wide control gap.

Incident data also influences architecture standards. If a recurring incident category appears in multiple clients or platforms, the platform team updates modules, CI/CD templates, runbooks, and review checklists. Standards are strongest when they are shaped by real operational evidence.
