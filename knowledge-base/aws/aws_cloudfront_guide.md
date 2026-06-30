# AWS CloudFront Guide

Document ID: IG-AWS-CF-001

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

This document provides the official CloudFront reference guide used by InfraGuid Technologies Pvt. Ltd.

The purpose of this guide is to help engineers understand, design, deploy, secure, optimize, and troubleshoot Amazon CloudFront distributions.

This guide combines:

```text
AWS CloudFront Concepts

InfraGuid Standards

Production Architecture Patterns

Terraform Examples

Operational Troubleshooting
```

to provide a practical CDN reference for engineering teams.

---

# 2. What Is CloudFront?

Amazon CloudFront is AWS's global Content Delivery Network (CDN).

It accelerates content delivery by serving content from edge locations closer to users.

---

## Problem Without CloudFront

User:

```text
London
```

Application:

```text
Mumbai Region
```

Request Path:

```text
London

↓

Mumbai

↓

London
```

---

Result:

```text
Higher Latency

Higher Origin Load

Higher Cost
```

---

## With CloudFront

```text
London User

↓

London Edge Location

↓

Response
```

---

Benefits:

```text
Lower Latency

Higher Performance

Lower Origin Cost
```

---

# 3. CloudFront Core Components

CloudFront consists of several components.

---

## Distribution

Primary CloudFront resource.

Represents:

```text
Global CDN Configuration
```

---

## Edge Locations

AWS global caching locations.

Purpose:

```text
Cache Content Near Users
```

---

## Origin

Source of content.

Examples:

```text
S3

ALB

EC2

API Gateway
```

---

## Cache Behavior

Defines:

```text
Caching Rules

Routing Rules

Request Handling
```

---

## Viewer

End User.

---

# 4. CloudFront Request Flow

Standard request path:

```text
User

↓

CloudFront Edge

↓

Cache Hit?
```

---

If Yes:

```text
Return Cached Content
```

---

If No:

```text
Fetch From Origin

Cache Response

Return To User
```

---

# 5. Origins

Origins provide content to CloudFront.

---

## 5.1 S3 Origin

Used for:

```text
Static Websites

Images

CSS

JavaScript

Downloads
```

---

Architecture:

```text
User

↓

CloudFront

↓

S3
```

---

## 5.2 ALB Origin

Used for:

```text
Web Applications

APIs

Dynamic Content
```

---

Architecture:

```text
User

↓

CloudFront

↓

ALB

↓

Application
```

---

## 5.3 API Gateway Origin

Used for:

```text
Serverless APIs
```

---

## 5.4 Multi-Origin Design

CloudFront can route requests:

```text
/static/*

↓

S3
```

---

```text
/api/*

↓

ALB
```

---

## InfraGuid Standard

Preferred architecture:

```text
CloudFront

↓

ALB

↓

Application
```

for internet-facing applications.

---

# 6. Caching Fundamentals

Caching is the primary reason CloudFront exists.

---

## What Is Cached?

Examples:

```text
Images

CSS

JavaScript

Videos

API Responses
```

---

## Cache Hit

CloudFront already has content.

---

Result:

```text
Fast Response

No Origin Request
```

---

## Cache Miss

Content not present.

---

Result:

```text
Origin Request Required
```

---

## Why Cache Hits Matter

Benefits:

```text
Reduced Latency

Reduced Cost

Reduced Backend Load
```

---

# 7. TTL Settings

TTL determines how long content remains cached.

---

## Minimum TTL

Lowest cache duration.

---

## Default TTL

Standard cache duration.

---

## Maximum TTL

Longest cache duration.

---

## Example

```text
Default TTL

↓

86400 Seconds

↓

24 Hours
```

---

## InfraGuid Recommendation

Static Assets:

```text
30 Days
```

or longer.

---

Dynamic APIs:

```text
Short TTL

Or No Cache
```

---

# 8. Cache Policies

Cache policies determine:

```text
What Creates Cache Variations
```

---

Examples:

```text
Headers

Cookies

Query Strings
```

---

## Bad Example

Forward:

```text
All Headers
```

---

Result:

```text
Low Cache Hit Ratio
```

---

## Good Example

Forward:

```text
Required Headers Only
```

---

Benefits:

```text
Higher Cache Efficiency
```

---

# 9. Cache Hit Ratio

One of the most important CloudFront metrics.

---

## Formula

```text
Cache Hits

÷

Total Requests
```

---

## Example

```text
900 Hits

100 Misses
```

---

Result:

```text
90%
```

Cache Hit Ratio

---

## InfraGuid Targets

Static Content:

```text
>90%
```

---

Investigate:

```text
<80%
```

---

## Common Causes Of Low Cache Hit Ratio

```text
Short TTL

Excessive Headers

Query Strings

Cookies
```

---

# 10. Origin Access Control (OAC)

OAC is the modern mechanism for securing S3 origins.

---

## Problem

Without OAC:

```text
Users May Access S3 Directly
```

---

## Architecture

```text
User

↓

CloudFront

↓

S3
```

---

Direct S3 access blocked.

---

## Benefits

```text
Improved Security

AWS Recommended

Simplified Management
```

---

## InfraGuid Standard

All new S3 origins must use:

```text
Origin Access Control (OAC)
```

---

Avoid:

```text
Public S3 Buckets
```

---

# 11. Origin Access Identity (OAI)

Legacy predecessor to OAC.

---

## Status

Supported but older.

---

## InfraGuid Recommendation

Preferred:

```text
OAC
```

---

Use OAI only when:

```text
Legacy Compatibility Required
```

---

# 12. Compression

CloudFront supports:

```text
Gzip

Brotli
```

---

Benefits:

```text
Reduced Bandwidth

Improved Performance
```

---

## InfraGuid Standard

Enable:

```text
Brotli

Gzip
```

for all web workloads.

---

# 13. CloudFront + AWS WAF

CloudFront is frequently the first security control protecting internet-facing applications.

AWS WAF integrates directly with CloudFront to inspect and filter incoming traffic before requests reach the origin.

---

## 13.1 Why WAF Matters

Without WAF:

```text
Internet

↓

Application
```

---

With WAF:

```text
Internet

↓

WAF

↓

CloudFront

↓

Origin
```

---

Benefits:

```text
Attack Mitigation

Bot Protection

Rate Limiting

Traffic Filtering
```

---

## 13.2 Common Threats Blocked

Examples:

```text
SQL Injection

Cross Site Scripting

Bad Bots

Credential Stuffing

Layer 7 DDoS
```

---

## 13.3 Managed Rules

AWS provides:

```text
Managed Rule Groups
```

---

Examples:

```text
AWS Common Rule Set

Known Bad Inputs

Amazon IP Reputation

Anonymous IP List
```

---

## 13.4 Rate Limiting

Useful against:

```text
Brute Force Attacks

API Abuse

Credential Stuffing
```

---

Example:

```text
Block

More Than 1000 Requests

Per 5 Minutes
```

---

## 13.5 InfraGuid Standard

Internet-facing applications must implement:

```text
CloudFront

+

AWS WAF
```

---

# 14. Signed URLs

Signed URLs provide temporary access to protected content.

---

## Problem

Content should not be publicly accessible.

Examples:

```text
Paid Downloads

Private Documents

Training Videos
```

---

Without Signed URLs:

```text
Anyone With URL

Can Access Content
```

---

## Solution

Generate:

```text
Temporary URL
```

---

Example:

```text
Valid For:

15 Minutes
```

---

After expiration:

```text
Access Denied
```

---

## Architecture

```text
Application

↓

Generate Signed URL

↓

User

↓

CloudFront

↓

Content
```

---

## Common Use Cases

```text
Private Videos

Premium Content

Customer Documents

Reports
```

---

## Security Benefits

```text
Time Limited Access

Reduced Exposure

No Public Content
```

---

# 15. Signed Cookies

Signed Cookies provide controlled access to multiple protected objects.

---

## Difference From Signed URLs

Signed URL:

```text
One File
```

---

Signed Cookie:

```text
Multiple Files
```

---

## Example

Video Platform:

```text
video1.mp4

video2.mp4

video3.mp4
```

---

Instead of generating:

```text
3 Signed URLs
```

Use:

```text
1 Signed Cookie
```

---

## Benefits

```text
Simplified Access

Better User Experience

Reduced Complexity
```

---

## Common Use Cases

```text
Video Libraries

Premium Portals

Training Platforms
```

---

# 16. Geographic Restrictions

CloudFront can restrict content access by country.

---

## Why Restrict Access

Examples:

```text
Licensing Restrictions

Compliance Requirements

Fraud Prevention
```

---

## Allow List Model

Only specific countries allowed.

Example:

```text
India

Singapore

United States
```

---

## Block List Model

Specific countries blocked.

Example:

```text
Restricted Regions
```

---

## Architecture

```text
User Country

↓

CloudFront Check

↓

Allow / Block
```

---

## InfraGuid Standard

Use geographic restrictions only when:

```text
Business Requirement Exists
```

---

Avoid unnecessary restrictions.

---

# 17. Security Headers

Security headers improve browser-side security.

CloudFront can inject security headers through:

```text
Response Headers Policies
```

---

## Recommended Headers

### HSTS

```text
Strict-Transport-Security
```

---

Purpose:

```text
Force HTTPS
```

---

### X-Content-Type-Options

```text
nosniff
```

---

Purpose:

```text
Prevent MIME Attacks
```

---

### X-Frame-Options

```text
DENY
```

---

Purpose:

```text
Prevent Clickjacking
```

---

### Referrer-Policy

Controls:

```text
Referrer Information
```

---

### Content Security Policy

Controls:

```text
Allowed Browser Resources
```

---

## InfraGuid Standard

Internet-facing applications should use:

```text
Security Headers Policy
```

through CloudFront.

---

# 18. CloudFront Logging

CloudFront logs are critical for:

```text
Troubleshooting

Security Investigations

Performance Analysis

Traffic Auditing
```

---

## Standard Logs

Provide:

```text
Requests

IPs

URLs

Response Codes
```

---

## Real-Time Logs

Provide:

```text
Near Real-Time Visibility
```

---

Useful for:

```text
Security Events

Production Incidents
```

---

## Storage Destinations

Recommended:

```text
S3

CloudWatch
```

---

## Retention Standards

Production:

```text
90 Days Minimum
```

---

Security Investigations:

```text
1 Year
```

recommended.

---

## InfraGuid Standard

All production distributions must enable:

```text
CloudFront Logging
```

---

# 19. Monitoring

CloudFront monitoring ensures performance and availability.

---

## Key Metrics

Monitor:

```text
Requests

Error Rates

Cache Hit Ratio

Latency

Bandwidth
```

---

## Error Monitoring

Track:

```text
4xx Errors

5xx Errors
```

---

Investigate:

```text
Sudden Increases
```

immediately.

---

## Performance Metrics

Review:

```text
Origin Latency

Viewer Latency

Cache Efficiency
```

---

## Dashboard Requirements

Production distributions should have dashboards showing:

```text
Traffic

Errors

Latency

Cache Performance
```

---

## Alerting Standards

Create alerts for:

```text
High 5xx Errors

Origin Failures

Traffic Spikes

Low Cache Hit Ratio
```

---

# 20. CloudFront Cost Optimization

CloudFront can significantly reduce infrastructure costs when configured correctly.

---

## 20.1 Cost Drivers

Major CloudFront costs:

```text
Data Transfer Out

Requests

Origin Fetches

Functions
```

---

## 20.2 Improve Cache Hit Ratio

Higher cache hit ratio means:

```text
Lower Origin Cost

Lower Compute Cost

Lower Bandwidth Cost
```

---

Target:

```text
>90%
```

for static workloads.

---

## 20.3 Optimize Cache Policies

Avoid forwarding:

```text
All Headers

All Cookies

All Query Strings
```

unless required.

---

Reason:

```text
Reduced Cache Efficiency
```

---

## 20.4 Compression

Enable:

```text
Brotli

Gzip
```

---

Benefits:

```text
Reduced Transfer Cost

Improved Performance
```

---

## 20.5 CloudFront vs Direct Origin

Preferred:

```text
CloudFront

↓

Origin
```

---

Instead of:

```text
User

↓

Origin
```

---

Benefits:

```text
Lower Origin Load

Lower EC2 Cost

Lower ALB Cost
```

---

## 20.6 Cost Monitoring

Review monthly:

```text
Bandwidth

Requests

Origin Traffic

Cache Hit Ratio
```

---

## 20.7 InfraGuid Cost Optimization Standard

Every production distribution must maintain:

```text
Cost Dashboard

Cache Dashboard

Optimization Review
```

---

## 20.8 Common Waste Patterns

Examples:

```text
TTL Too Low

No Compression

Poor Cache Policy

Excessive Origin Requests
```

---

Review these areas first when CloudFront costs increase unexpectedly.

# 21. CloudFront Functions

CloudFront Functions provide lightweight code execution at AWS edge locations.

They execute before requests reach the origin.

---

## 21.1 What Are CloudFront Functions?

CloudFront Functions are:

```text
Lightweight

Low Latency

High Scale
```

edge compute services.

---

They are designed for:

```text
Request Manipulation

Response Manipulation

Header Processing

URL Rewriting
```

---

## 21.2 Execution Location

Functions execute at:

```text
CloudFront Edge Locations
```

before origin communication.

---

Architecture:

```text
User

↓

CloudFront Function

↓

Cache

↓

Origin
```

---

## 21.3 Common Use Cases

### URL Rewrites

Example:

```text
/about

↓

/about.html
```

---

### Header Injection

Add:

```text
Security Headers

Custom Headers
```

---

### Redirects

Example:

```text
HTTP

↓

HTTPS
```

---

### Basic Authentication

Simple edge authentication.

---

## 21.4 Benefits

```text
Extremely Fast

Low Cost

Global Scale

No Origin Load
```

---

## 21.5 Limitations

Not suitable for:

```text
Database Access

External API Calls

Complex Processing
```

---

## 21.6 CloudFront Functions vs Lambda@Edge

Use Functions for:

```text
Simple Logic

Header Manipulation

Redirects
```

---

## 21.7 InfraGuid Standard

Prefer:

```text
CloudFront Functions
```

before:

```text
Lambda@Edge
```

when functionality is sufficient.

---

# 22. Lambda@Edge

Lambda@Edge extends CloudFront with full Lambda execution capabilities.

---

## 22.1 What Is Lambda@Edge?

Lambda@Edge allows code execution at CloudFront edge locations.

Unlike CloudFront Functions, it supports:

```text
Complex Logic

External Calls

Advanced Processing
```

---

## 22.2 Execution Events

Can execute during:

```text
Viewer Request

Viewer Response

Origin Request

Origin Response
```

---

## 22.3 Common Use Cases

### JWT Validation

```text
Validate Token

↓

Allow Access
```

---

### Advanced Authentication

```text
User Authentication

Authorization
```

---

### Dynamic Content Generation

Generate responses without reaching origin.

---

### Bot Filtering

Advanced request inspection.

---

## 22.4 Advantages

```text
Full Lambda Runtime

More Features

Advanced Logic
```

---

## 22.5 Disadvantages

```text
Higher Cost

Higher Latency

Operational Complexity
```

---

## 22.6 InfraGuid Recommendation

Use Lambda@Edge only when:

```text
CloudFront Functions
```

cannot satisfy requirements.

---

# 23. Terraform Examples

This section provides approved Terraform implementation patterns.

---

# 23.1 Basic CloudFront Distribution

```hcl
resource "aws_cloudfront_distribution" "main" {

  enabled = true

  origin {

    domain_name =
      aws_s3_bucket.static.bucket_regional_domain_name

    origin_id = "static-site"
  }

  default_cache_behavior {

    allowed_methods = [
      "GET",
      "HEAD"
    ]

    cached_methods = [
      "GET",
      "HEAD"
    ]

    target_origin_id = "static-site"

    viewer_protocol_policy =
      "redirect-to-https"
  }

  viewer_certificate {

    cloudfront_default_certificate = true
  }
}
```

---

## Purpose

Creates:

```text
Basic CDN

HTTPS

Caching
```

---

# 23.2 Origin Access Control

```hcl
resource "aws_cloudfront_origin_access_control" "oac" {

  name = "main-oac"

  origin_access_control_origin_type = "s3"

  signing_behavior = "always"

  signing_protocol = "sigv4"
}
```

---

## Purpose

Provides:

```text
Private S3 Access
```

through CloudFront.

---

# 23.3 WAF Association

```hcl
resource "aws_cloudfront_distribution" "main" {

  web_acl_id =
    aws_wafv2_web_acl.main.arn
}
```

---

## Purpose

Protect distribution using:

```text
AWS WAF
```

---

# 23.4 Response Headers Policy

```hcl
resource "aws_cloudfront_response_headers_policy" "security" {

  name = "security-policy"
}
```

---

Purpose:

```text
Security Headers

Browser Protection
```

---

# 23.5 Logging Configuration

```hcl
logging_config {

  bucket =
    aws_s3_bucket.logs.bucket_domain_name

  include_cookies = false
}
```

---

Purpose:

```text
Access Logging
```

---

# 23.6 Compression

```hcl
compress = true
```

---

Benefits:

```text
Reduced Bandwidth

Improved Performance
```

---

# 24. Common Troubleshooting Scenarios

This section documents common CloudFront incidents encountered by InfraGuid engineering teams.

---

# Scenario 1

CloudFront Serving Old Content

---

## Symptoms

```text
Updated File

↓

Users Still See Old Version
```

---

## Investigation Checklist

Verify:

```text
TTL

Cache Policy

Invalidation Status

Browser Cache
```

---

## Common Root Causes

### Long TTL

Content remains cached.

---

### Missing Invalidation

CloudFront unaware of changes.

---

### Browser Cache

User browser still serving old content.

---

## Resolution

```text
CloudFront Invalidation

Versioned File Names

Review TTL
```

---

# Scenario 2

Low Cache Hit Ratio

---

## Symptoms

```text
High Origin Load

High CloudFront Cost

Increased Latency
```

---

## Investigation Checklist

Verify:

```text
Headers

Cookies

Query Strings

TTL Values
```

---

## Common Root Causes

```text
Forwarding All Headers

Forwarding All Cookies

Very Short TTL
```

---

## Resolution

Optimize:

```text
Cache Policy
```

---

# Scenario 3

CloudFront Returning 403

---

## Symptoms

```text
Access Denied
```

---

## Investigation Checklist

Verify:

```text
OAC

Bucket Policy

Signed URL

Signed Cookie
```

---

## Common Root Causes

```text
Bucket Policy Error

OAC Misconfiguration

Expired Signed URL
```

---

# Scenario 4

CloudFront Returning 502

---

## Symptoms

```text
Bad Gateway
```

---

## Investigation Checklist

Verify:

```text
Origin Health

SSL Certificates

ALB

Origin DNS
```

---

## Common Root Causes

```text
Origin Unreachable

Certificate Error

Backend Failure
```

---

# Scenario 5

CloudFront Returning 504

---

## Symptoms

```text
Gateway Timeout
```

---

## Investigation Checklist

Verify:

```text
Application Response Time

Origin Capacity

Database Latency
```

---

## Common Root Causes

```text
Slow Backend

Database Bottleneck

Origin Saturation
```

---

# Scenario 6

WAF Not Blocking Requests

---

## Symptoms

```text
Malicious Traffic

↓

Still Reaches Origin
```

---

## Investigation Checklist

Verify:

```text
WAF Association

Rule Priority

Rule Actions

Scope
```

---

## Common Root Causes

```text
Wrong Web ACL

Count Mode

Rule Ordering
```

---

# Scenario 7

High CloudFront Costs

---

## Investigation Checklist

Verify:

```text
Cache Hit Ratio

Bandwidth

Request Volume

Origin Fetches
```

---

## Common Root Causes

```text
Poor Caching

Large Objects

Excessive Requests
```

---

# 25. Best Practices

The following practices apply to all InfraGuid-managed CloudFront deployments.

---

## Security

Always use:

```text
HTTPS Only
```

---

Enable:

```text
TLS 1.2+

AWS WAF
```

---

## Origins

Preferred:

```text
Private Origins
```

---

Avoid:

```text
Public S3 Buckets
```

---

Use:

```text
Origin Access Control (OAC)
```

---

## Caching

Target:

```text
>90%
```

cache hit ratio for static workloads.

---

Use:

```text
Long TTL

Versioned Assets
```

---

## Monitoring

Enable:

```text
CloudFront Logs

CloudWatch Metrics

Alarms
```

---

## Cost Optimization

Enable:

```text
Compression

Efficient Cache Policies
```

---

Review monthly:

```text
Traffic

Bandwidth

Origin Requests

Cache Performance
```

---

## Edge Compute

Use:

```text
CloudFront Functions
```

for lightweight logic.

---

Use:

```text
Lambda@Edge
```

only when necessary.

---

## Security Headers

Implement:

```text
HSTS

CSP

X-Frame-Options

X-Content-Type-Options
```

---

# 26. Governance Statement

This document defines the official CloudFront architecture, implementation standards, operational guidance, and troubleshooting procedures used by InfraGuid Technologies Pvt. Ltd.

All CloudFront distributions, CDN architectures, edge security controls, caching configurations, and internet-facing content delivery platforms must align with the standards defined in this guide.

The objectives of this document are:

```text
Secure Content Delivery

High Performance

Operational Consistency

Cost Efficiency

Global Scalability
```

The Architecture Team owns and maintains this document.

Platform Engineering is responsible for implementation and operational compliance.

Security Engineering is responsible for WAF integration, security controls, and internet-facing risk management.

Exceptions require approval from:

```text
Solutions Architect

Platform Engineering Lead

Security Engineering Lead
```

This document serves as the authoritative CloudFront reference for all InfraGuid-managed cloud environments.