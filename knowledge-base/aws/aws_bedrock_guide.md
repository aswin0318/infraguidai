# AWS Bedrock Guide

Document ID: IG-AWS-BEDROCK-001

Version: 1.0

Owner: Rahul Varma

Owner Role: Solutions Architect

Department: Architecture

Classification: Internal Use Only

Status: Approved

Review Cycle: 6 Months

Last Updated: June 2026

---

# 1. Purpose

This document provides the official AWS Bedrock reference guide used by InfraGuid Technologies Pvt. Ltd.

The purpose of this guide is to help engineers understand, design, deploy, secure, optimize, and troubleshoot AI applications built on Amazon Bedrock.

This guide combines:

```text
AWS Bedrock Concepts

Generative AI Principles

RAG Architecture Patterns

Cost Optimization

Production Standards

Troubleshooting Guidance
```

to provide a practical AI engineering reference for engineering teams.

---

# 2. What Is Amazon Bedrock?

Amazon Bedrock is AWS's managed Generative AI platform.

It provides access to foundation models through a fully managed API.

---

## Traditional Approach

Before Bedrock:

```text
Choose Model

Deploy Infrastructure

Manage GPUs

Scale Inference

Monitor Usage
```

---

## Bedrock Approach

```text
Application

↓

Bedrock API

↓

Foundation Model

↓

Response
```

---

AWS manages:

```text
Infrastructure

Scaling

Availability

Model Hosting
```

---

## Benefits

```text
No GPU Management

Managed Scaling

Enterprise Security

AWS Integration
```

---

# 3. Bedrock Core Components

Bedrock consists of several major components.

---

## Foundation Models

Large language models available through Bedrock.

---

## Embedding Models

Convert text into vectors.

---

## Knowledge Bases

Managed RAG solution.

---

## Agents

Tool-using AI systems.

---

## Guardrails

Safety and policy enforcement.

---

## Inference APIs

Model invocation endpoints.

---

# 4. Foundation Models

Foundation Models (FMs) are pre-trained AI models.

They generate:

```text
Text

Code

Summaries

Explanations

Structured Data
```

---

## Examples

Available models may include:

```text
Claude

Llama

Nova

Titan

Mistral
```

---

## Selection Principle

Choose:

```text
Smallest Model

That Solves The Problem
```

---

Avoid:

```text
Largest Model By Default
```

---

## InfraGuid Standard

Model selection should consider:

```text
Accuracy

Latency

Cost

Context Window
```

---

# 5. Bedrock Inference

Inference means:

```text
Sending Prompt

↓

Receiving Response
```

---

## Request Flow

```text
Application

↓

Prompt

↓

Bedrock

↓

Model

↓

Response
```

---

## Components

Request contains:

```text
System Prompt

User Prompt

Parameters
```

---

Response contains:

```text
Generated Output
```

---

# 6. Prompt Engineering

Prompt engineering significantly impacts:

```text
Accuracy

Cost

Latency
```

---

## Prompt Structure

Recommended:

```text
Role

Task

Context

Instructions

Output Format
```

---

## Example

```text
You are a DevOps expert.

Explain NAT Gateway.

Use simple language.

Provide examples.
```

---

## Common Mistakes

```text
Ambiguous Instructions

Excessive Context

Missing Constraints
```

---

## InfraGuid Standard

Prompts should be:

```text
Clear

Structured

Deterministic
```

---

# 7. Model Parameters

Model behavior is influenced by parameters.

---

## Temperature

Controls randomness.

---

Low:

```text
More Deterministic
```

---

High:

```text
More Creative
```

---

## Top P

Controls token selection probability.

---

## Max Tokens

Limits output size.

---

## InfraGuid Recommendation

Knowledge systems:

```text
Low Temperature
```

---

Creative systems:

```text
Higher Temperature
```

---

# 8. Embedding Models

Embedding models convert text into vectors.

---

## Why Embeddings Exist

LLMs process:

```text
Language
```

---

Vector databases process:

```text
Numbers
```

---

Embeddings bridge the gap.

---

## Example

Text:

```text
NAT Gateway allows outbound internet access.
```

---

Embedding:

```text
[0.234, -0.891, 0.112, ...]
```

---

## Purpose

Enable:

```text
Similarity Search

Semantic Search

RAG Retrieval
```

---

## InfraGuid Standard

Use embeddings whenever:

```text
Knowledge Retrieval

Document Search

Semantic Search
```

is required.

---

# 9. Embedding Workflow

Standard workflow:

```text
Document

↓

Chunking

↓

Embedding

↓

Vector Database

↓

Retrieval
```

---

At query time:

```text
Question

↓

Embedding

↓

Similarity Search

↓

Relevant Chunks
```

---

Returned to model as context.

---

# 10. Vector Databases

Vector databases store embeddings.

---

## Purpose

Enable:

```text
Semantic Retrieval
```

---

## Examples

```text
ChromaDB

OpenSearch

Pinecone

Weaviate
```

---

## Query Example

Question:

```text
Why do we use NAT Gateway?
```

---

Returns:

```text
Semantically Similar Documents
```

even if wording differs.

---

## InfraGuid Standard

Preferred:

```text
ChromaDB
```

for internal AI assistants.

---

# 11. Retrieval-Augmented Generation (RAG)

RAG is the primary AI architecture used by InfraGuid.

---

## Problem Without RAG

Model answers using:

```text
Training Data
```

only.

---

Problems:

```text
Hallucinations

Outdated Information

No Company Knowledge
```

---

## Solution

Retrieve:

```text
Relevant Documents
```

before generation.

---

## Architecture

```text
User Question

↓

Embedding

↓

Vector Search

↓

Retrieve Chunks

↓

LLM

↓

Answer
```

---

## Benefits

```text
Current Information

Company Knowledge

Reduced Hallucination
```

---

## InfraGuid Standard

Internal assistants should use:

```text
RAG First
```

before relying on model knowledge.

# 12. Chunking Strategies

Chunking is the process of splitting large documents into smaller sections before generating embeddings.

Chunking is one of the most important components in a RAG system.

Poor chunking often causes:

```text
Poor Retrieval

Incomplete Answers

Hallucinations

Irrelevant Context
```

even when the LLM itself is excellent.

---

## 12.1 Why Chunking Exists

Embedding models have limits.

Entire documents should not be embedded as a single vector.

Example:

```text
500 Page PDF

↓

Single Embedding
```

Result:

```text
Poor Retrieval Accuracy
```

---

Instead:

```text
Document

↓

Chunks

↓

Embeddings

↓

Vector Store
```

---

## 12.2 Fixed Size Chunking

Documents split by:

```text
Character Count

Token Count
```

---

Example:

```text
500 Tokens

↓

500 Tokens

↓

500 Tokens
```

---

Advantages:

```text
Simple

Fast

Easy To Implement
```

---

Disadvantages:

```text
May Break Context

May Split Sentences

May Split Concepts
```

---

## 12.3 Recursive Chunking

Most common production strategy.

---

Process:

```text
Document

↓

Sections

↓

Paragraphs

↓

Sentences
```

until target size reached.

---

Advantages:

```text
Preserves Meaning

Maintains Context

Improved Retrieval
```

---

## 12.4 Semantic Chunking

Uses AI to determine:

```text
Meaning Boundaries
```

instead of character boundaries.

---

Example:

```text
NAT Gateway Section

↓

One Chunk

IAM Section

↓

Another Chunk
```

---

Advantages:

```text
Highest Quality Retrieval
```

---

Disadvantages:

```text
Higher Cost

More Processing
```

---

## 12.5 Parent Child Chunking

Store:

```text
Small Chunks

+

Large Parent Context
```

---

Retrieval:

```text
Retrieve Child

↓

Expand To Parent
```

---

Benefits:

```text
Better Precision

Better Context
```

---

## 12.6 Chunk Overlap

Overlap preserves context between chunks.

---

Example:

```text
Chunk A

Tokens 1-500
```

---

```text
Chunk B

Tokens 450-950
```

---

Overlap:

```text
50 Tokens
```

---

Benefits:

```text
Improved Continuity

Reduced Context Loss
```

---

## 12.7 InfraGuid Standard

Default recommendation:

```text
Recursive Chunking

500-1000 Tokens

10-20% Overlap
```

---

Use Semantic Chunking for:

```text
Critical Knowledge Systems
```

---

# 13. Bedrock Knowledge Bases

Knowledge Bases provide a managed RAG implementation inside Bedrock.

---

## 13.1 What Is A Knowledge Base?

Knowledge Base automates:

```text
Ingestion

Chunking

Embedding

Storage

Retrieval
```

---

Instead of building RAG manually.

---

## Traditional RAG

```text
Documents

↓

Chunking

↓

Embedding

↓

Vector Store

↓

Retriever

↓

LLM
```

---

## Bedrock Knowledge Base

```text
Documents

↓

Knowledge Base

↓

LLM
```

---

AWS manages:

```text
Chunking

Embeddings

Retrieval
```

---

## 13.2 Supported Data Sources

Examples:

```text
S3

Confluence

SharePoint

Web Sources
```

(depending on AWS capabilities at deployment time)

---

## 13.3 Retrieval Flow

```text
User Question

↓

Knowledge Base

↓

Retrieve Chunks

↓

Model

↓

Response
```

---

## 13.4 Advantages

```text
Reduced Engineering Effort

Managed Service

AWS Integration
```

---

## 13.5 Limitations

Less control over:

```text
Chunking

Retrieval Logic

Ranking
```

compared to custom RAG.

---

## 13.6 InfraGuid Standard

For enterprise AI assistants:

```text
Custom RAG
```

preferred when:

```text
Advanced Retrieval

Custom Ranking

Observability

Multi-Agent Systems
```

are required.

---

# 14. Agents

Agents are AI systems capable of:

```text
Reasoning

Planning

Tool Usage

Multi-Step Execution
```

---

## 14.1 Traditional LLM

```text
Question

↓

Answer
```

---

## Agent

```text
Question

↓

Reason

↓

Choose Tool

↓

Execute Tool

↓

Analyze Results

↓

Answer
```

---

## Example

Question:

```text
Show production EC2 instances
```

---

Agent:

```text
Determine Intent

↓

Call AWS API

↓

Collect Data

↓

Generate Answer
```

---

## 14.2 Agent Components

Typically:

```text
LLM

Tools

Memory

Instructions

Planning Logic
```

---

## 14.3 Common Tools

Examples:

```text
AWS APIs

Terraform Repositories

Monitoring Systems

Knowledge Bases

Ticketing Systems
```

---

## 14.4 Agent Benefits

```text
Automation

Operational Assistance

Complex Workflows
```

---

## 14.5 Agent Risks

```text
Incorrect Actions

Tool Abuse

Excessive Permissions
```

---

## 14.6 InfraGuid Standard

Agents should:

```text
Read By Default

Write By Exception
```

for production systems.

---

# 15. Guardrails

Guardrails provide safety controls for AI applications.

---

## 15.1 Why Guardrails Exist

Without guardrails:

```text
Unsafe Responses

Policy Violations

Data Leakage
```

may occur.

---

## 15.2 Guardrail Functions

Can enforce:

```text
Content Policies

Topic Restrictions

PII Protection

Response Filtering
```

---

## Example

User asks:

```text
Reveal Production Passwords
```

---

Guardrail:

```text
Blocks Response
```

---

## 15.3 Common Controls

### Sensitive Information

```text
Credit Cards

Passwords

Secrets
```

---

### Restricted Topics

```text
Internal Security Data

Confidential Information
```

---

### Toxic Content

```text
Harassment

Hate Speech

Abusive Content
```

---

## 15.4 InfraGuid Standard

All external-facing AI applications must implement:

```text
Guardrails

PII Protection

Prompt Filtering
```

---

# 16. AI Security

AI systems introduce new attack surfaces.

Security controls are mandatory.

---

## 16.1 Security Objectives

Protect:

```text
Models

Prompts

Data

Users
```

---

## 16.2 Prompt Injection

Example:

```text
Ignore Previous Instructions
```

---

Risk:

```text
Bypass Intended Behavior
```

---

Mitigation:

```text
Prompt Isolation

Context Validation

Guardrails
```

---

## 16.3 Data Leakage

Risk:

```text
Sensitive Data

↓

Model Output
```

---

Mitigation:

```text
Data Classification

Access Controls

Output Filtering
```

---

## 16.4 Tool Abuse

Agent receives:

```text
Dangerous Request
```

---

Tool execution must enforce:

```text
Authorization

Approval

Auditability
```

---

## 16.5 Secrets Protection

Never place:

```text
Passwords

API Keys

Tokens
```

inside prompts.

---

## 16.6 InfraGuid Standard

AI systems must follow:

```text
Least Privilege

Guardrails

Prompt Security

Audit Logging
```

---

# 17. AI Architecture Patterns

InfraGuid uses multiple AI architecture patterns.

---

## 17.1 Direct LLM

Architecture:

```text
User

↓

LLM

↓

Answer
```

---

Suitable for:

```text
General Assistance
```

---

## 17.2 RAG

Architecture:

```text
User

↓

Retriever

↓

Documents

↓

LLM
```

---

Suitable for:

```text
Knowledge Systems
```

---

## 17.3 Agentic RAG

Architecture:

```text
User

↓

Agent

↓

Retriever

↓

Tools

↓

LLM
```

---

Suitable for:

```text
Enterprise Assistants

Operations Platforms
```

---

## 17.4 Multi-Agent Systems

Architecture:

```text
Coordinator Agent

↓

Specialized Agents

↓

Answer
```

---

Examples:

```text
Networking Agent

IAM Agent

Terraform Agent

Security Agent
```

---

## 17.5 InfraGuid Standard

Preferred architecture:

```text
RAG

↓

Agent Layer

↓

Tool Layer
```

for internal engineering assistants.

---

# 18. Prompt Management

Prompts should be treated as production assets.

---

## 18.1 Why Prompt Management Matters

Prompt changes can impact:

```text
Accuracy

Latency

Cost

Safety
```

---

## 18.2 Prompt Versioning

Prompts should be:

```text
Version Controlled
```

similar to application code.

---

## 18.3 Prompt Structure Standard

Recommended:

```text
System Instructions

Role Definition

Constraints

Context

Output Format
```

---

## 18.4 Prompt Testing

Validate:

```text
Accuracy

Safety

Consistency
```

before production deployment.

---

## 18.5 Prompt Observability

Track:

```text
Prompt Version

Latency

Cost

User Feedback
```

---

## 18.6 Prompt Governance

Production prompts require:

```text
Review

Version Control

Testing
```

before release.

---

## 18.7 InfraGuid Standard

Prompt engineering should be managed through:

```text
Git Repository

Pull Requests

Change Reviews
```

rather than manual editing in production.

# 19. Model Selection Framework

Model selection is one of the most important architectural decisions in an AI system.

Incorrect model selection can result in:

```text
Excessive Cost

Poor Accuracy

High Latency

Operational Complexity
```

---

## 19.1 Model Selection Objectives

The objective is:

```text
Choose The Smallest

Lowest Cost

Fastest Model

That Meets Business Requirements
```

---

## 19.2 Evaluation Criteria

Every model should be evaluated against:

```text
Accuracy

Latency

Cost

Context Window

Tool Usage

Reasoning Capability
```

---

## 19.3 Decision Framework

### Step 1

Determine task type.

Examples:

```text
Summarization

Question Answering

Code Generation

Agentic Workflows

Classification
```

---

### Step 2

Determine quality requirements.

Examples:

```text
Basic

Moderate

Advanced
```

---

### Step 3

Determine latency requirements.

Examples:

```text
Interactive

Near Real-Time

Batch Processing
```

---

### Step 4

Determine cost sensitivity.

Examples:

```text
Low Volume

High Volume

Enterprise Scale
```

---

## 19.4 Model Selection Matrix

| Requirement | Preferred Model Class |
|------------|----------------------|
| FAQ Bot | Small |
| Knowledge Assistant | Medium |
| Agent System | Medium-Large |
| Deep Reasoning | Large |
| Code Generation | Medium-Large |

---

## 19.5 Escalation Strategy

Preferred:

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
Largest Model By Default
```

---

## 19.6 InfraGuid Standard

Production systems must document:

```text
Selected Model

Reason For Selection

Expected Cost

Expected Latency
```

---

# 20. Token Optimization

Token usage directly impacts:

```text
Cost

Latency

Scalability
```

---

## 20.1 Why Token Optimization Matters

Every request consumes:

```text
Input Tokens

Output Tokens
```

---

Larger prompts:

```text
Higher Cost

Longer Latency
```

---

## 20.2 Common Waste Patterns

Examples:

```text
Repeated Instructions

Large Irrelevant Context

Duplicate Documents

Excessive Output Length
```

---

## 20.3 Prompt Reduction

Reduce:

```text
Redundant Instructions

Unnecessary Examples

Repeated Context
```

---

## 20.4 Context Optimization

Retrieve:

```text
Relevant Chunks Only
```

---

Avoid:

```text
Entire Documents
```

when only a small section is needed.

---

## 20.5 Output Control

Use:

```text
Max Tokens
```

appropriately.

---

Example:

Bad:

```text
4000 Output Tokens
```

---

Good:

```text
500 Output Tokens
```

for short answers.

---

## 20.6 RAG Optimization

Retrieve:

```text
Top 3-5 Chunks
```

instead of:

```text
Top 20 Chunks
```

unless justified.

---

## 20.7 InfraGuid Standard

Every AI platform should monitor:

```text
Average Input Tokens

Average Output Tokens

Cost Per Request
```

---

# 21. Bedrock Cost Optimization

Bedrock costs scale with usage.

Without governance, costs can increase rapidly.

---

## 21.1 Cost Drivers

Primary cost drivers:

```text
Input Tokens

Output Tokens

Embedding Generation

Knowledge Base Usage

Agent Invocations
```

---

## 21.2 Model Selection

Largest models are not always required.

Review:

```text
Model Performance

Cost

Latency
```

regularly.

---

## 21.3 Embedding Optimization

Generate embeddings only when:

```text
Documents Change

New Documents Added
```

---

Avoid:

```text
Re-Embedding Entire Corpus
```

unnecessarily.

---

## 21.4 Context Optimization

Reduce:

```text
Chunk Count

Chunk Size

Prompt Size
```

where possible.

---

## 21.5 Response Optimization

Limit:

```text
Output Length
```

based on business requirements.

---

## 21.6 Caching

Cache:

```text
Frequently Asked Questions

Static Answers

Repeated Queries
```

---

Benefits:

```text
Reduced Model Usage

Reduced Cost

Reduced Latency
```

---

## 21.7 Cost Monitoring

Track:

```text
Cost Per Request

Cost Per User

Cost Per Team

Monthly Spend
```

---

## 21.8 InfraGuid Standard

All Bedrock workloads must maintain:

```text
Cost Dashboard

Usage Dashboard

Monthly Cost Review
```

---

# 22. Monitoring & Observability

AI systems require observability similar to traditional software systems.

---

## 22.1 Objectives

Monitor:

```text
Accuracy

Latency

Cost

Reliability
```

---

## 22.2 Request Metrics

Track:

```text
Request Count

Success Rate

Failure Rate
```

---

## 22.3 Latency Metrics

Track:

```text
P50

P95

P99
```

latency.

---

## 22.4 Token Metrics

Track:

```text
Input Tokens

Output Tokens

Total Tokens
```

---

## 22.5 Retrieval Metrics

For RAG systems monitor:

```text
Chunks Retrieved

Retrieval Latency

Chunk Relevance
```

---

## 22.6 Agent Metrics

Track:

```text
Tool Calls

Tool Failures

Execution Time

Agent Success Rate
```

---

## 22.7 Quality Metrics

Monitor:

```text
User Feedback

Hallucination Rate

Escalation Rate
```

---

## 22.8 Observability Dashboard

Production AI systems should expose:

```text
Latency

Cost

Usage

Quality Metrics
```

---

# 23. Terraform Examples

This section provides approved Bedrock implementation patterns.

---

# 23.1 Bedrock IAM Policy

```hcl
resource "aws_iam_policy" "bedrock_invoke" {

  name = "bedrock-invoke"

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {
        Effect = "Allow"

        Action = [
          "bedrock:InvokeModel"
        ]

        Resource = "*"
      }
    ]
  })
}
```

---

## Purpose

Allow:

```text
Model Invocation
```

---

# 23.2 Bedrock Runtime Endpoint Access

```hcl
resource "aws_vpc_endpoint" "bedrock" {

  vpc_id = aws_vpc.main.id

  service_name =
    "com.amazonaws.ap-south-1.bedrock-runtime"

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

## Purpose

Provide:

```text
Private Bedrock Access
```

without internet traffic.

---

# 23.3 Knowledge Base Access Role

```hcl
resource "aws_iam_role" "knowledge_base" {

  name = "bedrock-kb-role"

  assume_role_policy =
    data.aws_iam_policy_document.kb_trust.json
}
```

---

## Purpose

Allow:

```text
Knowledge Base Access
```

to data sources.

---

# 23.4 Logging Permissions

```hcl
{
  "Effect": "Allow",

  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],

  "Resource": "*"
}
```

---

Purpose:

```text
AI Platform Observability
```

---

# 24. Common Troubleshooting Scenarios

This section documents common Bedrock and RAG incidents.

---

# Scenario 1

Hallucinated Answers

---

## Symptoms

```text
Confident

But Incorrect Answers
```

---

## Investigation Checklist

Verify:

```text
Retrieved Context

Prompt Design

Chunk Quality

Model Selection
```

---

## Common Causes

```text
No RAG

Poor Retrieval

Insufficient Context
```

---

# Scenario 2

Relevant Documents Not Retrieved

---

## Symptoms

```text
Correct Document Exists

Not Returned
```

---

## Investigation Checklist

Verify:

```text
Chunking Strategy

Embedding Quality

Similarity Search

Metadata Filters
```

---

## Common Causes

```text
Bad Chunking

Wrong Embeddings

Low Recall Retrieval
```

---

# Scenario 3

High Bedrock Costs

---

## Symptoms

```text
Unexpected Spend Increase
```

---

## Investigation Checklist

Verify:

```text
Model Usage

Prompt Size

Output Size

Request Volume
```

---

## Common Causes

```text
Large Context

Large Output

Wrong Model Selection
```

---

# Scenario 4

Agent Produces Incorrect Actions

---

## Symptoms

```text
Wrong Tool Invoked

Incorrect Workflow
```

---

## Investigation Checklist

Verify:

```text
Agent Instructions

Tool Definitions

Prompt Design
```

---

## Common Causes

```text
Ambiguous Instructions

Poor Tool Selection Logic
```

---

# Scenario 5

Knowledge Base Returns Poor Results

---

## Investigation Checklist

Verify:

```text
Chunking

Embeddings

Source Documents

Ingestion Status
```

---

## Common Causes

```text
Poor Documents

Poor Chunking

Outdated Data
```

---

# Scenario 6

High Latency

---

## Symptoms

```text
Slow Responses
```

---

## Investigation Checklist

Verify:

```text
Model Size

Prompt Length

Retrieval Latency

Agent Workflow
```

---

## Common Causes

```text
Large Models

Large Context

Multiple Tool Calls
```

---

# 25. Best Practices

The following practices apply to all InfraGuid-managed AI systems.

---

## Architecture

Preferred:

```text
RAG

↓

Agent Layer

↓

Tool Layer
```

---

## Retrieval

Use:

```text
Recursive Chunking

Chunk Overlap

Metadata Filtering
```

---

## Security

Implement:

```text
Guardrails

Access Control

Prompt Security
```

---

## Cost

Monitor:

```text
Tokens

Usage

Model Selection
```

---

## Observability

Track:

```text
Latency

Accuracy

Cost

Quality
```

---

## Agents

Default:

```text
Read Access
```

---

Require approval for:

```text
Write Operations
```

---

## Governance

Version control:

```text
Prompts

Agent Definitions

Retrieval Logic
```

---

# 26. Governance Statement

This document defines the official AI engineering, Bedrock implementation, RAG architecture, and generative AI standards used by InfraGuid Technologies Pvt. Ltd.

All AI platforms, Bedrock integrations, retrieval systems, agent architectures, and enterprise AI assistants must align with the principles and controls defined within this guide.

The objectives of this document are:

```text
Reliable AI Systems

Secure AI Systems

Cost Efficient AI Systems

Observable AI Systems

Enterprise-Ready AI Platforms
```

The Architecture Team owns and maintains this document.

Platform Engineering is responsible for implementation and operational compliance.

Security Engineering is responsible for AI security controls, access management, and data protection.

Exceptions require approval from:

```text
Solutions Architect

Platform Engineering Lead

Security Engineering Lead
```

This document serves as the authoritative Bedrock and AI engineering reference for all InfraGuid-managed AI platforms.
