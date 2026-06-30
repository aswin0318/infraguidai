# Cost Optimization Guide

Document ID: IG-COST-001

Version: 1.0

Owner: Rahul Menon

Owner Role: Solutions Architect

Department: Platform Engineering

Classification: Internal Use Only

Status: Approved

Review Cycle: Quarterly

Last Updated: June 2026

---

# 1. Purpose

This document defines the official cost optimization standards, governance controls, FinOps practices, and cloud cost management strategies used by InfraGuid Technologies Pvt. Ltd.

The objective of cost optimization is not simply to reduce spending.

The objective is to:

```text
Maximize Business Value

Maintain Reliability

Control Cloud Spend

Improve Resource Efficiency
```

while ensuring platform stability and security.

This document serves as the authoritative guide for cloud cost management across all InfraGuid-managed environments.

---

# 2. Scope

This guide applies to:

```text
AWS Accounts

Production Environments

Staging Environments

Development Environments

Internal Platforms

Client Platforms
```

---

## Covered Services

Including:

```text
EC2

EBS

EFS

RDS

CloudFront

S3

EKS

Lambda

Bedrock

Route53

NAT Gateway
```

---

# 3. FinOps Principles

InfraGuid follows FinOps principles for cloud financial management.

---

## 3.1 Business Value First

Cost optimization must never compromise:

```text
Security

Availability

Compliance

Business Requirements
```

---

## 3.2 Data Driven Decisions

Optimization decisions should be based on:

```text
CloudWatch Metrics

Cost Explorer

CUR Reports

Trusted Advisor
```

not assumptions.

---

## 3.3 Continuous Optimization

Cost optimization is an ongoing process.

Not:

```text
One Time Activity
```

---

## 3.4 Shared Responsibility

Cloud cost management is owned by:

```text
Platform Engineering

Service Owners

Finance

Leadership
```

---

# 4. Cost Governance

Cost governance ensures accountability.

---

## 4.1 Ownership Requirement

Every resource must have:

```text
Owner

Cost Center

Project

Environment
```

through tags.

---

## 4.2 Cost Accountability

Service owners are responsible for:

```text
Resource Usage

Optimization Opportunities

Cost Reviews
```

---

## 4.3 Budget Ownership

Every environment must have:

```text
Budget

Forecast

Cost Owner
```

defined.

---

## 4.4 Cost Review Frequency

Production:

```text
Monthly
```

minimum.

---

# 5. Tagging Requirements

Cost optimization depends on tagging.

---

## Mandatory Cost Tags

```text
Environment

Owner

Project

CostCenter

ManagedBy

Criticality
```

---

## Purpose

Enables:

```text
Chargeback

Showback

Cost Allocation

Reporting
```

---

# 6. Cost Allocation Standards

Cloud costs must be traceable.

---

## Allocation Dimensions

Track spend by:

```text
Team

Project

Environment

Service
```

---

## Shared Services

Shared services should have:

```text
Shared Cost Center
```

defined.

---

## Cost Visibility

Every service owner should know:

```text
Monthly Cost

Top Cost Drivers

Optimization Opportunities
```

---

# 7. Budget Management

Budgets provide spending controls.

---

## Budget Categories

### Production

### Staging

### Development

### Shared Services

---

## Alert Thresholds

Configure:

```text
50%

75%

90%

100%
```

alerts.

---

## Escalation

100% budget utilization requires:

```text
Management Review
```

---

# 8. Cost Monitoring

Cost monitoring should be proactive.

---

## Required Tools

```text
AWS Cost Explorer

AWS Budgets

Trusted Advisor

CUR Reports
```

---

## Review Metrics

Track:

```text
Monthly Spend

Daily Spend

Service Spend

Growth Rate
```

---

## Cost Anomaly Detection

Required:

```text
AWS Cost Anomaly Detection
```

for production accounts.

# 9. EC2 Optimization

Amazon EC2 is one of the largest cost contributors in most AWS environments.

The objective is to provide required compute capacity at the lowest sustainable cost.

---

## 9.1 EC2 Cost Optimization Principles

Prioritize:

```text
Rightsizing

Autoscaling

Reserved Capacity

Workload Efficiency
```

---

Avoid:

```text
Overprovisioning

Idle Instances

Unnecessary High-End Instance Types
```

---

## 9.2 Instance Rightsizing

Review:

```text
CPU Utilization

Memory Utilization

Network Utilization
```

monthly.

---

### Rightsizing Thresholds

Investigate if:

```text
CPU < 20%

Memory < 30%
```

for 30 consecutive days.

---

### Example

Current:

```text
m6i.2xlarge
```

Recommended:

```text
m6i.large
```

when utilization supports it.

---

## 9.3 Auto Scaling Requirements

Production workloads should use:

```text
Auto Scaling Groups
```

whenever possible.

---

Benefits:

```text
Reduce Idle Capacity

Improve Availability

Lower Costs
```

---

## 9.4 Scheduling Non-Production Instances

Development environments should be automatically stopped during non-business hours.

Example:

```text
Shutdown:
8 PM

Startup:
8 AM
```

---

Expected Savings:

```text
40-60%
```

---

## 9.5 Instance Family Selection

Preferred:

```text
Graviton Instances
```

where compatible.

Examples:

```text
t4g

m7g

c7g

r7g
```

---

Potential savings:

```text
15-30%
```

compared to x86.

---

## 9.6 Spot Instances

Suitable for:

```text
CI/CD

Batch Jobs

Testing

Data Processing
```

---

Not suitable for:

```text
Critical Stateful Workloads
```

---

Potential savings:

```text
70-90%
```

---

## 9.7 Reserved Capacity Strategy

Stable workloads should use:

```text
Savings Plans
```

or:

```text
Reserved Instances
```

---

Review every:

```text
Quarter
```

---

## 9.8 EC2 Monitoring Requirements

Track:

```text
Idle Instances

Low Utilization

Stopped Instances

Orphaned Resources
```

---

## 9.9 EC2 Governance

Every production instance must justify:

```text
Size

Availability Requirement

Expected Utilization
```

---

# 10. EBS Optimization

EBS costs often increase due to unused volumes and excessive provisioning.

---

## 10.1 EBS Optimization Principles

Focus on:

```text
Volume Utilization

Volume Type

Lifecycle Management
```

---

## 10.2 Volume Type Selection

Use:

```text
gp3
```

as default.

---

Avoid:

```text
gp2
```

for new deployments.

---

Benefits:

```text
Lower Cost

Independent IOPS Configuration
```

---

## 10.3 Unattached Volume Detection

Review:

```text
Available Volumes
```

weekly.

---

Unused volumes should be:

```text
Archived

Deleted
```

after approval.

---

## 10.4 Snapshot Management

Snapshots should follow:

```text
Retention Policy
```

---

Recommended:

```text
Daily

Weekly

Monthly
```

rotation.

---

## 10.5 Provisioned IOPS Review

Review:

```text
io1

io2
```

volumes quarterly.

---

Validate:

```text
Actual IOPS Usage
```

matches provisioned capacity.

---

## 10.6 Storage Rightsizing

Review:

```text
Used Capacity

Allocated Capacity
```

---

Investigate:

```text
< 40% Utilization
```

---

## 10.7 EBS Governance

Unused EBS resources should not remain in production environments without documented justification.

---

# 11. EFS Optimization

EFS can become expensive when storage growth is unmanaged.

---

## 11.1 EFS Optimization Principles

Focus on:

```text
Storage Lifecycle

Throughput Selection

Data Retention
```

---

## 11.2 Lifecycle Management

Enable:

```text
EFS Lifecycle Policies
```

---

Move inactive files to:

```text
EFS Infrequent Access
```

---

Potential savings:

```text
Up to 90%
```

for inactive data.

---

## 11.3 Throughput Mode Selection

Default:

```text
Elastic Throughput
```

---

Provisioned throughput should only be used when justified by workload requirements.

---

## 11.4 Data Retention Reviews

Review:

```text
Inactive Files

Archived Data

Legacy Application Data
```

quarterly.

---

## 11.5 Shared Storage Governance

Shared EFS file systems require:

```text
Owner

Retention Policy

Usage Monitoring
```

---

# 12. RDS Optimization

RDS often represents one of the highest recurring cloud expenses.

---

## 12.1 Optimization Objectives

Focus on:

```text
Rightsizing

Storage Optimization

Reserved Capacity

Query Optimization
```

---

## 12.2 Instance Rightsizing

Review:

```text
CPU

Memory

Connections

IOPS
```

monthly.

---

Investigate:

```text
CPU < 20%
```

sustained usage.

---

## 12.3 Multi-AZ Usage

Production:

```text
Required
```

---

Development:

```text
Generally Not Required
```

unless specifically justified.

---

## 12.4 Storage Optimization

Enable:

```text
Storage Autoscaling
```

where appropriate.

---

Review:

```text
Unused Allocated Storage
```

quarterly.

---

## 12.5 Backup Optimization

Backup retention should align with:

```text
Business Requirements

Compliance Requirements
```

---

Avoid excessive retention periods.

---

## 12.6 Reserved Capacity

Stable production databases should use:

```text
Reserved Instances
```

or:

```text
Savings Plans
```

where appropriate.

---

## 12.7 Query Optimization

Application teams should review:

```text
Slow Queries

High Latency Queries

Expensive Queries
```

regularly.

---

## 12.8 RDS Governance

Database sizing decisions must be supported by utilization metrics.

---

# 13. CloudFront Optimization

CloudFront improves performance while reducing origin costs.

---

## 13.1 Optimization Objectives

Goals:

```text
Increase Cache Hit Ratio

Reduce Origin Requests

Reduce Data Transfer Costs
```

---

## 13.2 Cache Hit Ratio Targets

Target:

```text
> 90%
```

for static content.

---

Investigate:

```text
< 80%
```

cache hit rates.

---

## 13.3 Cache Policy Optimization

Optimize:

```text
Headers

Cookies

Query Strings
```

to maximize caching efficiency.

---

## 13.4 Origin Cost Reduction

Higher cache hit ratios reduce:

```text
ALB Costs

EC2 Costs

Data Transfer Costs
```

---

## 13.5 Compression

Enable:

```text
Brotli

Gzip
```

where supported.

---

Benefits:

```text
Reduced Bandwidth

Improved Performance
```

---

## 13.6 Geographic Analysis

Review:

```text
Top Regions

Traffic Distribution

Origin Load
```

quarterly.

---

## 13.7 CloudFront Governance

All public web applications should evaluate CloudFront usage before direct internet exposure.

---

# 14. S3 Optimization

S3 costs are frequently driven by storage growth and inefficient storage classes.

---

## 14.1 Optimization Principles

Focus on:

```text
Storage Class Selection

Lifecycle Policies

Data Retention
```

---

## 14.2 Storage Class Standards

Use:

### Frequent Access

```text
S3 Standard
```

---

### Infrequent Access

```text
S3 Standard-IA
```

---

### Archive

```text
S3 Glacier

S3 Glacier Deep Archive
```

---

## 14.3 Lifecycle Policies

All production buckets should implement lifecycle policies where appropriate.

---

Example:

```text
30 Days
↓
Standard-IA

90 Days
↓
Glacier

365 Days
↓
Deep Archive
```

---

## 14.4 Versioning Reviews

Versioning is required for critical buckets.

However:

```text
Old Versions
```

should be managed through lifecycle policies.

---

## 14.5 Incomplete Multipart Uploads

Automatically remove:

```text
Incomplete Uploads
```

after:

```text
7 Days
```

---

## 14.6 Storage Growth Monitoring

Monitor:

```text
Bucket Growth

Object Count

Storage Class Distribution
```

monthly.

---

## 14.7 S3 Governance

Every bucket must have:

```text
Owner

Retention Policy

Lifecycle Policy
```

defined and documented.

# 15. EKS Optimization

Amazon EKS can become one of the most expensive services in AWS environments if cluster resources are not actively managed.

The primary optimization objective is:

```text
Maximize Pod Utilization

Minimize Node Waste

Reduce Operational Overhead
```

while maintaining reliability and scalability.

---

## 15.1 EKS Cost Optimization Principles

Focus on:

```text
Node Utilization

Pod Density

Autoscaling

Storage Efficiency
```

---

Avoid:

```text
Overprovisioned Nodes

Idle Clusters

Unused Persistent Volumes
```

---

## 15.2 Cluster Utilization Targets

Production clusters should target:

```text
CPU Utilization:
50% - 70%

Memory Utilization:
50% - 75%
```

---

Investigate:

```text
CPU < 30%

Memory < 30%
```

sustained utilization.

---

## 15.3 Node Group Optimization

Separate node groups for:

```text
System Workloads

Application Workloads

AI Workloads

Batch Workloads
```

---

Benefits:

```text
Better Scaling

Lower Cost

Improved Resource Allocation
```

---

## 15.4 Cluster Autoscaler

Production clusters should use:

```text
Cluster Autoscaler
```

or:

```text
Karpenter
```

---

Purpose:

```text
Automatically Add Nodes

Automatically Remove Nodes
```

based on demand.

---

## 15.5 Spot Instances

Suitable for:

```text
CI/CD

Batch Processing

AI Training

Background Jobs
```

---

Potential savings:

```text
70% - 90%
```

---

## 15.6 Pod Resource Optimization

Every workload must define:

```yaml
requests:
limits:
```

---

Review:

```text
CPU Requests

Memory Requests

Actual Usage
```

monthly.

---

## 15.7 Rightsizing Workloads

Common waste pattern:

```text
CPU Request:
2 vCPU

Actual Usage:
0.2 vCPU
```

---

Such workloads should be resized.

---

## 15.8 Persistent Volume Management

Review:

```text
Unused PVCs

Orphaned Volumes

Storage Utilization
```

monthly.

---

## 15.9 Cluster Consolidation

Multiple small clusters should be reviewed.

Consolidation opportunities:

```text
Development Clusters

Testing Clusters

Internal Tooling Clusters
```

---

## 15.10 EKS Governance

Every cluster must maintain:

```text
Capacity Dashboard

Cost Dashboard

Resource Utilization Review
```

---

# 16. Lambda Optimization

AWS Lambda provides excellent cost efficiency when properly designed.

However, poor implementations can create unnecessary spending.

---

## 16.1 Optimization Objectives

Focus on:

```text
Execution Duration

Memory Allocation

Invocation Volume
```

---

## 16.2 Memory Optimization

Review:

```text
Configured Memory

Actual Usage
```

---

Example:

```text
Configured:
2048 MB

Actual:
300 MB
```

---

Potential optimization opportunity exists.

---

## 16.3 Execution Duration

Monitor:

```text
Average Duration

P95 Duration

P99 Duration
```

---

Reduce:

```text
Cold Starts

Unnecessary Processing

External Dependencies
```

---

## 16.4 Provisioned Concurrency

Use only when justified.

Suitable for:

```text
Critical APIs

Latency Sensitive Workloads
```

---

Avoid for:

```text
Low Traffic Functions
```

---

## 16.5 Lambda Architecture

Preferred:

```text
ARM64
```

when supported.

---

Benefits:

```text
Lower Cost

Improved Efficiency
```

---

## 16.6 Event Filtering

Filter events before invocation whenever possible.

Examples:

```text
SQS Filtering

EventBridge Rules

SNS Filtering
```

---

Benefits:

```text
Lower Invocation Count

Lower Cost
```

---

## 16.7 Lambda Governance

Review:

```text
Invocation Volume

Execution Duration

Memory Utilization
```

quarterly.

---

# 17. Bedrock Cost Management

Bedrock usage can scale rapidly if governance controls are not implemented.

Because Bedrock pricing is usage-based, uncontrolled adoption can create significant spend.

---

## 17.1 Cost Management Objectives

Focus on:

```text
Model Efficiency

Token Efficiency

Prompt Optimization

Caching
```

---

## 17.2 Model Selection Strategy

Use the smallest model capable of solving the task.

---

Example hierarchy:

```text
Small Model
↓
Medium Model
↓
Large Model
```

---

Avoid:

```text
Always Using Largest Model
```

---

## 17.3 Prompt Optimization

Reduce:

```text
Prompt Length

Context Size

Redundant Instructions
```

---

Benefits:

```text
Lower Token Usage

Faster Responses

Lower Cost
```

---

## 17.4 Context Management

RAG systems should retrieve:

```text
Relevant Documents Only
```

---

Avoid:

```text
Large Unfiltered Context
```

---

## 17.5 Response Length Controls

Limit:

```text
Maximum Tokens
```

based on business requirements.

---

## 17.6 Embedding Optimization

Avoid unnecessary embedding generation.

Generate embeddings only when:

```text
Content Changes

New Content Added
```

---

## 17.7 Caching Strategy

Cache:

```text
Frequently Asked Questions

Common Queries

Static Responses
```

---

Benefits:

```text
Reduced Model Calls

Reduced Token Consumption
```

---

## 17.8 Usage Monitoring

Track:

```text
Model Usage

Token Usage

Cost Per User

Cost Per Request
```

---

## 17.9 Bedrock Governance

Every AI platform must maintain:

```text
Usage Dashboard

Monthly Cost Review

Cost Alerting
```

---

# 18. Data Transfer Optimization

Data transfer costs are often overlooked but can become significant.

---

## 18.1 Optimization Objectives

Reduce:

```text
Internet Egress

Cross AZ Traffic

Cross Region Traffic
```

---

## 18.2 CloudFront Usage

Public applications should use:

```text
CloudFront
```

to reduce:

```text
Origin Traffic

Bandwidth Costs
```

---

## 18.3 Cross-AZ Traffic

Review:

```text
Application Design

Database Design

Storage Access Patterns
```

---

Excessive cross-AZ communication increases costs.

---

## 18.4 Cross-Region Traffic

Cross-region traffic should be:

```text
Documented

Justified

Monitored
```

---

## 18.5 NAT Gateway Costs

Monitor:

```text
Data Processed

Data Transfer
```

---

Large NAT Gateway costs often indicate architectural inefficiencies.

---

## 18.6 VPC Endpoints

Use:

```text
Gateway Endpoints

Interface Endpoints
```

where cost effective.

---

Benefits:

```text
Reduce NAT Traffic

Improve Security
```

---

## 18.7 Data Transfer Governance

Monthly review required for:

```text
NAT Costs

Cross AZ Costs

Cross Region Costs
```

---

# 19. Savings Plans Strategy

Savings Plans are the preferred commitment model for InfraGuid.

---

## 19.1 Strategy Objectives

Reduce compute costs while maintaining flexibility.

---

## 19.2 Applicable Services

Savings Plans apply to:

```text
EC2

Lambda

Fargate
```

---

## 19.3 Eligible Workloads

Use Savings Plans for:

```text
Stable Production Workloads

Long Running Services

Predictable Compute Usage
```

---

## 19.4 Commitment Planning

Analyze:

```text
6 Months Usage

12 Months Usage
```

before purchase.

---

## 19.5 Coverage Targets

Target:

```text
70% - 90%
```

coverage for stable workloads.

---

## 19.6 Review Frequency

Review:

```text
Quarterly
```

---

## 19.7 Governance

Savings Plan purchases require:

```text
Architecture Review

Cost Review

Management Approval
```

---

# 20. Reserved Instances Strategy

Reserved Instances remain useful for predictable workloads.

---

## 20.1 Applicable Services

Examples:

```text
RDS

ElastiCache

Redshift
```

---

## 20.2 Candidate Identification

Suitable workloads:

```text
Steady State

Long Running

Predictable Usage
```

---

## 20.3 Commitment Evaluation

Review:

```text
Historical Usage

Growth Forecast

Migration Plans
```

before purchase.

---

## 20.4 Utilization Targets

Target:

```text
> 90% Utilization
```

for purchased reservations.

---

## 20.5 Risk Considerations

Avoid overcommitting.

Changes in:

```text
Architecture

Instance Types

Regions
```

may reduce value.

---

## 20.6 RI Review Process

Review:

```text
Coverage

Utilization

Savings Achieved
```

quarterly.

---

## 20.7 Governance

Reserved Instance purchases require:

```text
Cost Analysis

Approval

Documentation
```

prior to commitment.

# 21. Rightsizing Process

Rightsizing is the process of aligning cloud resource capacity with actual workload requirements.

The objective is:

```text
Eliminate Waste
↓
Maintain Performance
↓
Reduce Cost
```

without negatively impacting availability or user experience.

---

## 21.1 Rightsizing Objectives

Rightsizing aims to:

```text
Reduce Overprovisioning

Improve Resource Utilization

Lower Cloud Spend

Improve Operational Efficiency
```

---

## 21.2 Rightsizing Scope

Applicable resources:

```text
EC2

EBS

RDS

EKS Nodes

Lambda

ECS

ElastiCache
```

---

## 21.3 Rightsizing Workflow

Standard process:

```text
Collect Metrics
↓
Analyze Utilization
↓
Identify Waste
↓
Recommend Changes
↓
Validate Impact
↓
Implement
↓
Monitor
```

---

## 21.4 Rightsizing Review Frequency

### Production

Monthly

---

### Shared Services

Monthly

---

### Development

Quarterly

---

## 21.5 Rightsizing Criteria

Review resources with:

```text
CPU < 20%

Memory < 30%

Storage < 40%
```

for extended periods.

---

## 21.6 Validation Requirements

Before rightsizing:

Validate:

```text
Peak Usage

Growth Trends

Seasonal Demand

Business Events
```

---

## 21.7 Post-Implementation Validation

Verify:

```text
Performance

Availability

Latency

Error Rates
```

for at least:

```text
7 Days
```

after changes.

---

## 21.8 Rightsizing Governance

Rightsizing recommendations should be documented and tracked until implemented or formally rejected.

---

# 22. Idle Resource Detection

Idle resources represent one of the most common sources of cloud waste.

The objective is to identify and remove unused infrastructure.

---

## 22.1 Idle Resource Categories

Common examples:

```text
Unused EC2 Instances

Unattached EBS Volumes

Unused Load Balancers

Unused Elastic IPs

Unused Snapshots

Unused NAT Gateways

Unused EKS Clusters
```

---

## 22.2 Detection Frequency

Review:

```text
Weekly
```

for production accounts.

---

## 22.3 EC2 Idle Detection

Investigate:

```text
CPU < 5%

Network Near Zero

Disk Activity Near Zero
```

for:

```text
30 Days
```

---

## 22.4 EBS Idle Detection

Review:

```text
Available Volumes

Orphaned Volumes
```

---

## 22.5 Load Balancer Detection

Review:

```text
Request Count

Target Traffic

Health Status
```

---

Unused ALBs should be evaluated for removal.

---

## 22.6 Elastic IP Detection

Review:

```text
Unassociated Elastic IPs
```

monthly.

---

## 22.7 Snapshot Review

Review:

```text
Snapshot Age

Retention Compliance

Recovery Requirements
```

---

## 22.8 Idle Resource Governance

No resource should remain idle without:

```text
Business Justification

Owner

Review Date
```

---

# 23. Monthly Cost Review Process

Monthly reviews ensure cloud spending remains controlled and aligned with business goals.

---

## 23.1 Review Objectives

Evaluate:

```text
Spending Trends

Optimization Opportunities

Forecast Accuracy

Budget Compliance
```

---

## 23.2 Review Participants

Required:

```text
Platform Engineering

Service Owners

Solutions Architect
```

---

Optional:

```text
Finance

Leadership
```

---

## 23.3 Review Inputs

Review:

```text
AWS Cost Explorer

CUR Reports

Budgets

Anomaly Reports

Trusted Advisor
```

---

## 23.4 Review Areas

### Infrastructure

Review:

```text
EC2

RDS

EKS

Storage
```

---

### Networking

Review:

```text
CloudFront

NAT Gateway

Data Transfer
```

---

### AI Platform

Review:

```text
Bedrock

Embeddings

Vector Databases
```

---

## 23.5 Review Outputs

Deliver:

```text
Cost Summary

Optimization Opportunities

Savings Forecast

Action Items
```

---

## 23.6 Escalation Criteria

Escalate when:

```text
Budget Exceeded

Unexpected Growth

Anomaly Detection Triggered
```

---

## 23.7 Monthly Review Governance

Monthly cost reviews are mandatory for all production environments.

---

# 24. FinOps Responsibilities

Cloud financial management is a shared responsibility.

---

## 24.1 Platform Engineering Responsibilities

Responsible for:

```text
Infrastructure Optimization

Rightsizing

Automation

Resource Governance
```

---

## 24.2 Service Owner Responsibilities

Responsible for:

```text
Application Efficiency

Resource Justification

Cost Visibility
```

---

## 24.3 Solutions Architect Responsibilities

Responsible for:

```text
Architecture Reviews

Optimization Recommendations

Commitment Planning
```

---

## 24.4 Operations Responsibilities

Responsible for:

```text
Monitoring

Cost Alerting

Resource Discovery
```

---

## 24.5 Leadership Responsibilities

Responsible for:

```text
Budget Approval

Investment Decisions

Optimization Prioritization
```

---

## 24.6 FinOps Accountability Model

Every cloud resource must have:

```text
Owner

Budget

Business Purpose
```

defined.

---

# 25. Cost Optimization KPIs

KPIs measure optimization effectiveness.

---

## 25.1 Budget Variance

Measure:

```text
Actual Spend

vs

Forecast Spend
```

---

Target:

```text
±10%
```

---

## 25.2 Resource Utilization

Track:

```text
CPU Utilization

Memory Utilization

Storage Utilization
```

---

## 25.3 Idle Resource Count

Target:

```text
Continuous Reduction
```

---

## 25.4 Savings Plan Coverage

Target:

```text
70% - 90%
```

for eligible workloads.

---

## 25.5 Reserved Capacity Utilization

Target:

```text
> 90%
```

---

## 25.6 Cost Per Service

Track:

```text
Monthly Cost

Growth Trend

Optimization Savings
```

---

## 25.7 Cost Per User

Track:

```text
Platform Cost

÷

Active Users
```

where applicable.

---

## 25.8 Optimization Savings

Track:

```text
Identified Savings

Implemented Savings

Realized Savings
```

---

## 25.9 Cost Anomalies

Target:

```text
100%
```

investigation of detected anomalies.

---

## 25.10 FinOps Maturity

Evaluate:

```text
Visibility

Optimization

Governance

Automation
```

annually.

---

# 26. Governance Statement

This document defines the official cloud cost optimization and FinOps standards used by InfraGuid Technologies Pvt. Ltd.

All employees responsible for designing, deploying, operating, or maintaining cloud environments must follow the principles and controls defined within this guide.

The objectives of this document are:

```text
Control Cloud Spend

Improve Resource Efficiency

Increase Cost Visibility

Enable Sustainable Growth

Support Business Objectives
```

The Platform Engineering Team owns and maintains this document.

The Solutions Architecture Team is responsible for optimization strategy and governance.

Service owners are responsible for the efficient use of resources under their ownership.

Exceptions to these standards require approval from:

```text
Solutions Architect

Platform Engineering Lead

CTO
```

This document represents the authoritative cost optimization standard for all InfraGuid-managed cloud environments.