# AWS VPC Guide

Document ID: IG-AWS-VPC-001

Version: 1.0

Owner: Rahul Varma

Owner Role: Solutions Architect

Department: Architecture

Classification: Internal Use Only

Status: Approved

Review Cycle: 12 Months

Last Updated: June 2026

---

# 1. Purpose

This document provides the official networking reference guide used by InfraGuid Technologies Pvt. Ltd.

The purpose of this guide is to help engineers understand, design, deploy, troubleshoot, and maintain Amazon Virtual Private Cloud (VPC) environments.

This guide combines:

```text
AWS Networking Concepts

InfraGuid Standards

Production Architecture Patterns

Terraform Examples

Operational Troubleshooting
```

to provide a practical networking reference for engineering teams.

---

# 2. What Is A VPC?

A Virtual Private Cloud (VPC) is a logically isolated virtual network within AWS.

It allows organizations to control:

```text
IP Addressing

Routing

Internet Access

Private Connectivity

Security Controls
```

for AWS resources.

---

## Real World Analogy

Think of AWS as a city.

A VPC is:

```text
Your Private Office Building
```

inside that city.

Within the building you decide:

```text
Rooms

Doors

Hallways

Visitors

Security Guards
```

---

AWS provides the city.

You design the building.

---

## Why We Need A VPC

Without a VPC:

```text
No Network Isolation

No Routing Control

No Security Boundaries
```

---

A VPC provides:

```text
Private Network Space

Traffic Control

Security Boundaries

Connectivity Control
```

---

# 3. VPC Components Overview

A VPC consists of multiple networking components working together.

---

## Core Components

```text
VPC
│
├── Subnets
├── Route Tables
├── Internet Gateway
├── NAT Gateway
├── Security Groups
├── Network ACLs
├── VPC Endpoints
├── Flow Logs
└── DNS Services
```

---

## Component Responsibilities

| Component | Purpose |
|------------|----------|
| VPC | Network Boundary |
| Subnet | Network Segmentation |
| Route Table | Traffic Routing |
| Internet Gateway | Public Internet Access |
| NAT Gateway | Outbound Internet Access |
| Security Group | Instance Firewall |
| NACL | Subnet Firewall |
| Endpoint | Private AWS Access |
| Flow Logs | Traffic Monitoring |

---

# 4. CIDR Fundamentals

CIDR defines the IP range available inside a VPC.

---

## Example

```text
10.0.0.0/16
```

---

Meaning:

```text
Network:
10.0.0.0

Mask:
/16
```

---

Available Addresses:

```text
65,536
```

---

## Common CIDR Sizes

| CIDR | Addresses |
|--------|------------|
| /24 | 256 |
| /20 | 4096 |
| /16 | 65536 |

---

## InfraGuid Standard

Production VPCs should use:

```text
/16
```

unless there is a justified reason to use smaller ranges.

---

Reason:

```text
Future Growth

Additional Subnets

Peering

Transit Gateway Expansion
```

---

## CIDR Planning Rules

Avoid:

```text
Overlapping CIDRs
```

because they break:

```text
VPC Peering

Transit Gateway

Hybrid Connectivity
```

---

## Approved Production Range

Examples:

```text
10.0.0.0/16

10.1.0.0/16

10.2.0.0/16
```

---

# 5. Subnets

A subnet represents a smaller network segment inside a VPC.

---

## Purpose

Subnets provide:

```text
Isolation

Traffic Control

Availability Design
```

---

## Types

### Public Subnet

Contains resources requiring internet access.

Examples:

```text
ALB

NAT Gateway

Bastion Hosts
```

---

### Private Subnet

Contains resources that should not be directly accessible from the internet.

Examples:

```text
EC2

EKS Nodes

RDS

EFS
```

---

## Public Subnet Architecture

```text
Internet
    │
    ▼
Internet Gateway
    │
    ▼
Public Subnet
    │
    ▼
ALB
```

---

## Private Subnet Architecture

```text
Private Subnet
      │
      ▼
NAT Gateway
      │
      ▼
Internet Gateway
      │
      ▼
Internet
```

---

## InfraGuid Production Standard

Production environments must contain:

```text
Minimum 2 Public Subnets

Minimum 2 Private Subnets

Across Multiple AZs
```

---

## Example

```text
ap-south-1a

Public-A
Private-A

ap-south-1b

Public-B
Private-B
```

---

# 6. Route Tables

Route tables determine:

```text
Where Traffic Goes
```

inside a VPC.

---

## Concept

Every packet leaving a resource consults:

```text
Route Table
```

before being forwarded.

---

## Example Route

```text
Destination:
0.0.0.0/0

Target:
Internet Gateway
```

Meaning:

```text
Send Internet Traffic
To Internet Gateway
```

---

## Public Route Table

```text
Destination      Target

10.0.0.0/16      local
0.0.0.0/0        igw
```

---

## Private Route Table

```text
Destination      Target

10.0.0.0/16      local
0.0.0.0/0        nat
```

---

## InfraGuid Standard

Every subnet must have:

```text
Explicit Route Association
```

---

Avoid:

```text
Default Route Table Usage
```

in production.

---

## Common Failure Pattern

Observed in RCA-001:

```text
Missing Route Association

↓

Traffic Failure

↓

Application Outage
```

---

# 7. Internet Gateway (IGW)

An Internet Gateway enables internet connectivity for public resources.

---

## Responsibilities

Provides:

```text
Inbound Internet Access

Outbound Internet Access
```

for public subnets.

---

## Traffic Flow

```text
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Public Subnet
```

---

## Requirements

For internet access:

```text
Internet Gateway

Public IP

Route Table Entry
```

must all exist.

---

## Common Misconception

Having an Internet Gateway alone does NOT provide internet access.

Required:

```text
IGW

Route

Public IP
```

together.

---

## InfraGuid Standard

One Internet Gateway per VPC.

---

# 8. NAT Gateway

A NAT Gateway allows private resources to initiate outbound internet connections.

It does NOT allow inbound internet access.

---

## Why NAT Exists

Private resources need access to:

```text
Software Updates

Package Repositories

AWS APIs

Container Images
```

without becoming publicly accessible.

---

## Traffic Flow

```text
Private EC2
     │
     ▼
NAT Gateway
     │
     ▼
Internet Gateway
     │
     ▼
Internet
```

---

## Key Characteristic

Allowed:

```text
Outbound Connections
```

Blocked:

```text
Inbound Connections
```

---

## InfraGuid Production Standard

Production VPCs must deploy:

```text
One NAT Gateway Per AZ
```

---

Reason:

```text
High Availability

Fault Tolerance

Reduced Cross-AZ Dependency
```

---

## Common Failure Scenario

```text
Private EC2

↓

Cannot Download Packages
```

Checklist:

```text
NAT Gateway

Route Table

Internet Gateway

DNS
```

must be verified.

# 9. Security Groups

Security Groups are virtual firewalls attached to AWS resources.

They control:

```text
Inbound Traffic

Outbound Traffic
```

at the resource level.

Security Groups are one of the most important security controls within AWS.

---

## 9.1 Security Group Fundamentals

Security Groups operate at:

```text
Network Interface Level
```

Examples:

```text
EC2

ALB

RDS

EKS Nodes

Lambda ENIs
```

---

## 9.2 Stateful Firewall

Security Groups are:

```text
Stateful
```

Meaning:

If inbound traffic is allowed:

```text
Request
↓
Response
```

the response is automatically allowed.

---

No explicit return rule is required.

---

## Example

```text
Allow:

TCP 443

Source:
0.0.0.0/0
```

Client sends:

```text
HTTPS Request
```

Response automatically returns.

---

## 9.3 Inbound Rules

Control:

```text
Incoming Traffic
```

---

Example:

```text
Port:
443

Source:
0.0.0.0/0
```

Meaning:

```text
Allow HTTPS
From Internet
```

---

## 9.4 Outbound Rules

Control:

```text
Outgoing Traffic
```

---

Default AWS behavior:

```text
Allow All Outbound
```

---

Production environments should restrict outbound traffic when practical.

---

## 9.5 Security Group Referencing

Preferred InfraGuid approach:

```text
Security Group
To
Security Group
```

communication.

---

Example:

```text
ALB-SG

↓

APP-SG

↓

DB-SG
```

---

RDS Example:

Allow:

```text
Source:
APP-SG

Port:
5432
```

---

Avoid:

```text
10.0.0.0/16
```

when SG references are possible.

---

## 9.6 Production Architecture Example

```text
Internet
    │
    ▼
ALB-SG
    │
    ▼
APP-SG
    │
    ▼
DB-SG
```

---

Benefits:

```text
Least Privilege

Improved Security

Reduced Exposure
```

---

## 9.7 Common Failure Scenario

Observed in:

```text
RCA-003
```

Issue:

```text
Application SG Removed
```

Result:

```text
Application

↓

Database Connection Failure
```

---

Checklist:

```text
Ingress Rules

Egress Rules

SG References

Port Numbers
```

---

## 9.8 InfraGuid Standards

Production Security Groups must:

```text
Be Named

Be Tagged

Use SG References

Follow Least Privilege
```

---

Avoid:

```text
0.0.0.0/0

All Ports

All Protocols
```

unless formally approved.

---

# 10. Network ACLs (NACLs)

Network ACLs provide subnet-level traffic filtering.

---

## 10.1 What Is A NACL?

A NACL acts as:

```text
Subnet Firewall
```

---

Unlike Security Groups:

```text
Security Group
=
Resource Level

NACL
=
Subnet Level
```

---

## 10.2 Stateless Firewall

NACLs are:

```text
Stateless
```

---

Meaning:

Both directions must be explicitly allowed.

---

Example:

Allowed:

```text
Inbound TCP 443
```

Must also allow:

```text
Outbound Ephemeral Ports
```

---

Otherwise communication fails.

---

## 10.3 Rule Processing

Rules processed:

```text
Lowest Number First
```

Example:

```text
100 Allow HTTPS

200 Deny All
```

---

## 10.4 Common Use Cases

Useful for:

```text
Additional Security Layer

Compliance Requirements

Network Segmentation
```

---

## 10.5 InfraGuid Recommendation

Keep NACLs:

```text
Simple
```

---

Complex NACLs often create:

```text
Troubleshooting Difficulty

Unexpected Connectivity Failures
```

---

## 10.6 Common Troubleshooting Scenario

Symptoms:

```text
Security Groups Correct

Still No Connectivity
```

Investigate:

```text
NACL Rules

Ephemeral Ports

Subnet Association
```

---

## 10.7 InfraGuid Standard

Default recommendation:

```text
Allow Internal Traffic

Control Access Through Security Groups
```

---

# 11. Elastic IPs

Elastic IPs provide static public IPv4 addresses.

---

## 11.1 Purpose

Normally:

```text
Public IPs Change
```

during resource replacement.

---

Elastic IPs provide:

```text
Persistent Public Address
```

---

## 11.2 Common Uses

Examples:

```text
NAT Gateway

Bastion Host

Legacy Integrations
```

---

## 11.3 NAT Gateway Dependency

Every NAT Gateway requires:

```text
Elastic IP
```

---

Reason:

NAT Gateway requires:

```text
Stable Public Identity
```

for internet communication.

---

## 11.4 Cost Considerations

Unused Elastic IPs incur charges.

---

Review monthly:

```text
Unassociated EIPs
```

---

## 11.5 InfraGuid Standard

Elastic IPs should only exist when:

```text
Business Need Exists
```

---

# 12. VPC Endpoints

VPC Endpoints allow private communication with AWS services.

---

## Why They Exist

Without endpoints:

```text
Private EC2
     │
     ▼
NAT Gateway
     │
     ▼
Internet
     │
     ▼
AWS Service
```

---

With endpoints:

```text
Private EC2
     │
     ▼
VPC Endpoint
     │
     ▼
AWS Service
```

---

Benefits:

```text
Private Connectivity

Improved Security

Reduced NAT Cost
```

---

## Endpoint Types

AWS supports:

```text
Gateway Endpoints

Interface Endpoints
```

---

# 13. Gateway Endpoints

Gateway Endpoints support:

```text
S3

DynamoDB
```

only.

---

## Architecture

```text
Private EC2
      │
      ▼
Route Table
      │
      ▼
Gateway Endpoint
      │
      ▼
S3
```

---

## Benefits

```text
No NAT Required

Private Connectivity

Reduced Cost
```

---

## Common Use Case

Private instance accessing:

```text
S3
```

without internet access.

---

## Terraform Example

```hcl
resource "aws_vpc_endpoint" "s3" {

  vpc_id = aws_vpc.main.id

  service_name = "com.amazonaws.ap-south-1.s3"

  vpc_endpoint_type = "Gateway"

  route_table_ids = [
    aws_route_table.private.id
  ]
}
```

---

## InfraGuid Standard

Production VPCs should use:

```text
S3 Gateway Endpoint
```

when significant S3 access exists.

---

# 14. Interface Endpoints

Interface Endpoints provide private access to AWS services using ENIs.

---

## Supported Services

Examples:

```text
Secrets Manager

SSM

CloudWatch

Bedrock

ECR

SNS

SQS
```

---

## Architecture

```text
Private EC2
     │
     ▼
Private ENI
     │
     ▼
AWS Service
```

---

## DNS Behavior

AWS automatically changes:

```text
Public Service Name

↓

Private Endpoint Address
```

inside the VPC.

---

Example:

```text
secretsmanager.ap-south-1.amazonaws.com

↓

Private IP
```

---

## Benefits

```text
Private Connectivity

Improved Security

Reduced NAT Traffic
```

---

## Common Use Cases

```text
Secrets Manager

Bedrock

CloudWatch

SSM
```

---

## InfraGuid Standard

Production workloads should use:

```text
Interface Endpoints
```

for frequently accessed AWS services.

---

# 15. AWS PrivateLink

PrivateLink allows secure private connectivity between VPCs and services.

---

## Problem It Solves

Without PrivateLink:

```text
Public Internet

VPC Peering

Transit Gateway
```

often required.

---

PrivateLink enables:

```text
Private Service Consumption
```

without exposing services publicly.

---

## Architecture

Provider:

```text
Service VPC
```

Consumer:

```text
Client VPC
```

---

Connection:

```text
Interface Endpoint

↓

Endpoint Service

↓

Provider Service
```

---

## Common Use Cases

### SaaS Platforms

```text
Customer VPC

↓

PrivateLink

↓

Vendor Service
```

---

### Internal Shared Services

```text
Shared Security Platform

↓

PrivateLink

↓

Application Accounts
```

---

### Centralized AI Platform

```text
AI Service VPC

↓

PrivateLink

↓

Client Workloads
```

---

## Benefits

```text
Private Connectivity

Reduced Attack Surface

No Public Exposure

Simplified Architecture
```

---

## PrivateLink vs Peering

| Feature | PrivateLink | VPC Peering |
|----------|------------|------------|
| Network Access | Service Level | Full Network |
| CIDR Overlap | Supported | Not Supported |
| Security Isolation | Strong | Moderate |
| Complexity | Lower | Higher |

---

## InfraGuid Standard

Use PrivateLink when:

```text
Single Service Exposure Needed
```

Use Peering or Transit Gateway when:

```text
Full Network Connectivity Needed
```

# 16. Transit Gateway

As organizations grow, managing connectivity between multiple VPCs becomes increasingly complex.

Transit Gateway (TGW) acts as a centralized networking hub.

---

## 16.1 What Is Transit Gateway?

Transit Gateway is a regional AWS networking service that allows multiple VPCs and on-premises networks to connect through a central routing hub.

Think of it as:

```text
Network Router For AWS
```

---

Without Transit Gateway:

```text
VPC A
 ↔
VPC B

VPC A
 ↔
VPC C

VPC B
 ↔
VPC C
```

Multiple connections become difficult to manage.

---

With Transit Gateway:

```text
          TGW
        /  |  \
       /   |   \
      /    |    \
   VPC-A VPC-B VPC-C
```

---

## 16.2 Why We Use Transit Gateway

Benefits:

```text
Simplified Routing

Centralized Management

Scalability

Hybrid Connectivity
```

---

## 16.3 Common Use Cases

### Multi-Account Architecture

```text
Shared Services VPC

Production VPC

Security VPC

Monitoring VPC
```

---

### Hybrid Connectivity

```text
On-Premises

↓

VPN

↓

Transit Gateway

↓

AWS VPCs
```

---

### Centralized Security

```text
Security Inspection VPC

↓

Transit Gateway

↓

All Traffic Inspection
```

---

## 16.4 Route Tables In TGW

Transit Gateway maintains its own route tables.

Important:

```text
VPC Route Tables

AND

TGW Route Tables
```

must both be correct.

---

## 16.5 Common Failure Scenario

Symptoms:

```text
VPC A Cannot Reach VPC B
```

Common Causes:

```text
Missing TGW Route

Missing Attachment

Wrong Route Propagation
```

---

## 16.6 InfraGuid Standard

Transit Gateway should be used when:

```text
More Than 3 VPCs Require Connectivity
```

---

Avoid building large peering meshes.

---

# 17. VPC Peering

VPC Peering creates direct network connectivity between two VPCs.

---

## 17.1 What Is VPC Peering?

VPC Peering establishes:

```text
Private Network Connection
```

between two VPCs.

---

Example:

```text
VPC-A

↓

Peering

↓

VPC-B
```

---

Traffic remains:

```text
Private

Within AWS Network
```

---

## 17.2 Peering Characteristics

Benefits:

```text
Low Latency

Simple Setup

Private Communication
```

---

Limitations:

```text
No Transitive Routing

CIDR Overlap Not Allowed
```

---

## 17.3 No Transitive Routing

Example:

```text
A ↔ B

B ↔ C
```

Does NOT mean:

```text
A ↔ C
```

---

This is one of the most common misunderstandings.

---

## 17.4 Routing Requirements

Peering alone is not enough.

Both VPCs require:

```text
Route Updates
```

---

Example:

```text
Destination:
10.1.0.0/16

Target:
Peering Connection
```

---

## 17.5 Common Failure Scenario

Symptoms:

```text
Peering Active

No Connectivity
```

Checklist:

```text
Route Tables

Security Groups

NACLs

CIDRs
```

---

## 17.6 InfraGuid Standard

Use VPC Peering for:

```text
Small Architectures

Temporary Connectivity

Limited VPC Counts
```

---

Use Transit Gateway for:

```text
Enterprise Networking
```

---

# 18. DNS In VPC

DNS is one of the most overlooked networking components.

Many connectivity issues are actually DNS issues.

---

## 18.1 AWS DNS Service

Every VPC includes:

```text
AmazonProvidedDNS
```

---

Example:

```text
10.0.0.2
```

inside:

```text
10.0.0.0/16
```

---

## 18.2 DNS Hostnames

Production VPCs should enable:

```text
enable_dns_support

enable_dns_hostnames
```

---

Required for:

```text
Private DNS

Interface Endpoints

EKS

Service Discovery
```

---

## 18.3 Public DNS

Resources with public IPs receive:

```text
Public DNS Names
```

Example:

```text
ec2-13-233-xx-xx.ap-south-1.compute.amazonaws.com
```

---

## 18.4 Private DNS

Resources communicate using:

```text
Private IPs

Private Hostnames
```

inside VPCs.

---

## 18.5 Route53 Private Hosted Zones

Useful for:

```text
Internal Services

Databases

Shared Platforms
```

---

Example:

```text
db.internal.infraguid.local
```

---

## 18.6 Common DNS Failure Scenario

Symptoms:

```text
Ping By IP Works

Ping By Name Fails
```

Root Cause Usually:

```text
DNS Configuration
```

---

Checklist:

```text
DNS Support

Hosted Zones

Resolver Rules

Endpoint Configuration
```

---

## 18.7 InfraGuid Standard

All production VPCs must enable:

```text
DNS Support

DNS Hostnames
```

---

# 19. VPC Flow Logs

Flow Logs provide network visibility.

They help answer:

```text
What Traffic Is Flowing?

What Traffic Is Being Blocked?
```

---

## 19.1 What Are Flow Logs?

Flow Logs capture:

```text
Source IP

Destination IP

Port

Protocol

Action
```

for network traffic.

---

## Example Record

```text
10.0.1.25

↓

10.0.5.10

↓

TCP 5432

↓

ACCEPT
```

---

## 19.2 Why Flow Logs Matter

Useful for:

```text
Troubleshooting

Security Investigation

Compliance

Traffic Analysis
```

---

## 19.3 Flow Log Levels

Can be enabled for:

```text
VPC

Subnet

Network Interface
```

---

## 19.4 Storage Destinations

Recommended:

```text
CloudWatch Logs

S3
```

---

## 19.5 Common Troubleshooting Example

Issue:

```text
Application Cannot Reach Database
```

Flow Logs reveal:

```text
REJECT
```

---

Possible Causes:

```text
Security Group

NACL

Routing
```

---

## 19.6 InfraGuid Standard

Production environments must enable:

```text
VPC Flow Logs
```

---

Retention:

```text
90 Days Minimum
```

---

# 20. Multi-AZ Networking

High availability requires networking across multiple Availability Zones.

---

## 20.1 Why Multi-AZ Matters

Single AZ architectures create:

```text
Single Point Of Failure
```

---

Example Failure:

```text
AZ Failure

↓

Application Outage
```

---

## 20.2 Multi-AZ Design

Recommended:

```text
AZ-A

Public-A
Private-A

AZ-B

Public-B
Private-B
```

---

## 20.3 ALB Design

Application Load Balancers should span:

```text
Minimum Two AZs
```

---

## 20.4 NAT Gateway Design

InfraGuid Standard:

```text
One NAT Gateway Per AZ
```

---

Avoid:

```text
Single NAT Gateway
```

for production workloads.

---

## 20.5 Database Design

Production databases:

```text
Multi-AZ Required
```

---

## 20.6 Kubernetes Design

EKS node groups should span:

```text
Multiple AZs
```

---

## 20.7 Multi-AZ Benefits

Provides:

```text
Fault Tolerance

Improved Availability

Reduced Risk
```

---

# 21. Production Networking Architecture

This section defines the standard networking architecture used by InfraGuid.

---

## 21.1 Standard Architecture

```text
                     Internet
                         │
                         ▼
                 Internet Gateway
                         │
                         ▼
                Application Load Balancer
                   /               \
                  /                 \
                 ▼                   ▼

      Public Subnet A        Public Subnet B
              │                     │
              ▼                     ▼

      NAT Gateway A        NAT Gateway B
              │                     │
              ▼                     ▼

      Private Subnet A      Private Subnet B
              │                     │
              ▼                     ▼

         EKS Nodes          EKS Nodes
              │                     │
              └────────┬────────────┘
                       │
                       ▼

                    RDS
```

---

## 21.2 Security Layers

Layer 1:

```text
Security Groups
```

---

Layer 2:

```text
NACLs
```

---

Layer 3:

```text
IAM
```

---

Layer 4:

```text
WAF
```

---

## 21.3 AWS Service Connectivity

Preferred:

```text
Private Endpoints
```

for:

```text
Secrets Manager

SSM

CloudWatch

Bedrock
```

---

## 21.4 Logging Requirements

Required:

```text
CloudTrail

Flow Logs

ALB Logs
```

---

## 21.5 Monitoring Requirements

Required:

```text
CloudWatch

Network Dashboards

Alerting
```

---

## 21.6 Architecture Governance

Production networking changes require:

```text
Architecture Review

Security Review

Change Approval
```

before implementation.

# 22. Terraform Examples

This section provides Terraform examples aligned with InfraGuid standards.

The purpose is to provide reusable implementation patterns for common networking components.

---

# 22.1 VPC Creation

```hcl
resource "aws_vpc" "main" {

  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "infraguid-prod-vpc"
    Environment = "prod"
    ManagedBy   = "Terraform"
  }
}
```

---

## Explanation

Creates:

```text
10.0.0.0/16 VPC

DNS Support Enabled

DNS Hostnames Enabled
```

---

# 22.2 Public Subnet

```hcl
resource "aws_subnet" "public_a" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.1.0/24"

  availability_zone = "ap-south-1a"

  map_public_ip_on_launch = true

  tags = {
    Name = "public-a"
  }
}
```

---

## Purpose

Hosts:

```text
ALB

NAT Gateway

Bastion Hosts
```

---

# 22.3 Private Subnet

```hcl
resource "aws_subnet" "private_a" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.11.0/24"

  availability_zone = "ap-south-1a"

  tags = {
    Name = "private-a"
  }
}
```

---

## Purpose

Hosts:

```text
EC2

EKS

RDS

EFS
```

---

# 22.4 Internet Gateway

```hcl
resource "aws_internet_gateway" "igw" {

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}
```

---

# 22.5 Public Route Table

```hcl
resource "aws_route_table" "public" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.igw.id
  }
}
```

---

## Purpose

Allows:

```text
Internet Access
```

for public resources.

---

# 22.6 NAT Gateway

```hcl
resource "aws_eip" "nat" {

  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {

  allocation_id = aws_eip.nat.id

  subnet_id = aws_subnet.public_a.id

  depends_on = [
    aws_internet_gateway.igw
  ]
}
```

---

## Why Elastic IP?

NAT Gateway requires:

```text
Static Public Address
```

to communicate with the internet.

---

# 22.7 Private Route Table

```hcl
resource "aws_route_table" "private" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    nat_gateway_id = aws_nat_gateway.nat.id
  }
}
```

---

## Purpose

Allows:

```text
Outbound Internet Access
```

for private resources.

---

# 22.8 Security Group

```hcl
resource "aws_security_group" "web" {

  name = "web-sg"

  vpc_id = aws_vpc.main.id

  ingress {

    from_port = 443

    to_port = 443

    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

# 22.9 Database Security Group Reference

```hcl
resource "aws_security_group_rule" "db" {

  type = "ingress"

  from_port = 5432

  to_port = 5432

  protocol = "tcp"

  source_security_group_id =
    aws_security_group.app.id

  security_group_id =
    aws_security_group.db.id
}
```

---

## InfraGuid Standard

Preferred:

```text
Security Group References
```

instead of:

```text
CIDR Based Access
```

---

# 22.10 S3 Gateway Endpoint

```hcl
resource "aws_vpc_endpoint" "s3" {

  vpc_id = aws_vpc.main.id

  service_name =
    "com.amazonaws.ap-south-1.s3"

  vpc_endpoint_type = "Gateway"

  route_table_ids = [
    aws_route_table.private.id
  ]
}
```

---

## Benefit

```text
Private S3 Access

No NAT Cost
```

---

# 22.11 Secrets Manager Endpoint

```hcl
resource "aws_vpc_endpoint" "secrets" {

  vpc_id = aws_vpc.main.id

  service_name =
    "com.amazonaws.ap-south-1.secretsmanager"

  vpc_endpoint_type = "Interface"

  subnet_ids = [
    aws_subnet.private_a.id
  ]

  security_group_ids = [
    aws_security_group.endpoint.id
  ]
}
```

---

## Benefit

```text
Private Secrets Access
```

without internet connectivity.

---

# 23. Common Troubleshooting Scenarios

This section documents common networking failures encountered within InfraGuid-managed environments.

---

# Scenario 1

Private EC2 Cannot Reach Internet

---

## Symptoms

```text
yum update fails

apt update fails

Docker pull fails
```

---

## Investigation Checklist

Verify:

```text
NAT Gateway Exists

NAT Healthy

Internet Gateway Exists

Route Table Correct

DNS Enabled
```

---

## Common Root Causes

### Missing NAT Route

```text
0.0.0.0/0 Missing
```

---

### NAT Gateway Failure

```text
NAT Deleted

NAT Misconfigured
```

---

### Wrong Route Association

Private subnet associated with wrong route table.

---

# Scenario 2

EC2 Cannot Reach RDS

---

## Symptoms

```text
Database Connection Timeout

Application Failure
```

---

## Investigation Checklist

Verify:

```text
Security Groups

Port Numbers

Route Tables

NACLs

DNS
```

---

## Common Root Causes

### Missing Security Group Rule

Observed in:

```text
RCA-003
```

---

### Incorrect Database Port

Examples:

```text
5432

3306
```

---

### NACL Blocking Traffic

Stateless rule issue.

---

# Scenario 3

ALB Returns 503 Errors

---

## Symptoms

```text
503 Service Unavailable
```

---

## Investigation Checklist

Verify:

```text
Target Health

Security Groups

Health Checks

Application Status
```

---

## Common Root Causes

```text
Failed Health Checks

Application Crash

Security Group Restrictions
```

---

# Scenario 4

S3 Access Fails From Private Subnet

---

## Symptoms

```text
Access Timeout

Slow Downloads
```

---

## Investigation Checklist

Verify:

```text
Gateway Endpoint

IAM Role

Bucket Policy

Route Tables
```

---

## Common Root Causes

```text
Missing Endpoint

Missing IAM Permission

Bucket Policy Deny
```

---

# Scenario 5

VPC Peering Connectivity Failure

---

## Symptoms

```text
Ping Fails

TCP Connection Fails
```

---

## Investigation Checklist

Verify:

```text
Peering Status

Route Tables

Security Groups

CIDR Overlap
```

---

## Common Root Causes

```text
Missing Route

Overlapping CIDRs

Blocked Security Groups
```

---

# Scenario 6

Interface Endpoint Not Working

---

## Symptoms

```text
Secrets Manager Unreachable

CloudWatch Unreachable
```

---

## Investigation Checklist

Verify:

```text
Private DNS

Endpoint Status

Security Group

Subnet Placement
```

---

## Common Root Causes

```text
Private DNS Disabled

Endpoint Security Group Issue
```

---

# 24. Best Practices

The following best practices apply to all InfraGuid-managed networking environments.

---

## Architecture

Always deploy:

```text
Multi-AZ
```

for production.

---

## Security

Use:

```text
Security Group References
```

whenever possible.

---

Avoid:

```text
0.0.0.0/0
```

unless required.

---

## Routing

Avoid:

```text
Default Route Tables
```

in production.

---

Use:

```text
Explicit Route Associations
```

---

## NAT Gateway

Production standard:

```text
One NAT Gateway Per AZ
```

---

## Endpoints

Use:

```text
Gateway Endpoints

Interface Endpoints
```

to reduce:

```text
NAT Cost

Security Risk
```

---

## Monitoring

Enable:

```text
Flow Logs

CloudTrail

CloudWatch Monitoring
```

---

## CIDR Planning

Design for:

```text
Growth

Peering

Transit Gateway
```

from day one.

---

## Documentation

Document:

```text
CIDRs

Routes

Security Groups

Connectivity Paths
```

for all production environments.

---

# 25. Governance Statement

This document defines the official AWS networking standards and implementation guidance used by InfraGuid Technologies Pvt. Ltd.

All VPC architectures, networking implementations, Terraform deployments, and connectivity designs must align with the principles and standards defined in this guide.

The objectives of this document are:

```text
Secure Networking

Reliable Connectivity

Operational Consistency

Scalable Architecture

Efficient Troubleshooting
```

The Architecture Team owns and maintains this document.

Platform Engineering is responsible for implementation and operational compliance.

Security Engineering is responsible for reviewing networking controls and validating security requirements.

Exceptions to these standards require approval from:

```text
Solutions Architect

Platform Engineering Lead

Security Team
```

This document serves as the authoritative networking reference for all InfraGuid-managed cloud environments.