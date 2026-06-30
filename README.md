# InfraGuid

InfraGuid is a DevOps assistant I built around AWS Bedrock. The idea is simple:
you ask it questions about your infrastructure / deployments in plain English, and
it answers using a RAG knowledge base instead of making things up. On top of that
there's a small Kubernetes "log intelligence" agent that watches pod logs and pings
you on SNS when something actually breaks (OOMKills, crash loops, image pull errors,
that sort of thing).

It started as a side project to stop me digging through CloudWatch at 2am, so a lot
of the design choices lean towards "notify me, don't touch my cluster".

## What's in here

```
services/            the FastAPI microservices
  chat-service/      the API the frontend talks to (auth, chat, docs)
  agent-service/     the LangGraph agent + tools
  rag-service/       retrieval over the knowledge base
  ingestion-service/ chunk + embed docs into the vector store
  log-intel-lambda/  the K8s log watcher (runs as a Lambda)
shared/              common code shared by the services (config, http, cache)
frontend/            plain nginx + SPA, nothing fancy
terraform/           all the AWS bits (EKS, ECR, S3, IRSA, SNS, Lambda)
argocd-apps/         GitOps manifests + Helm charts
knowledge-base/      the source docs that get ingested
```

## Running it locally

You'll need Docker and a `.env`. Copy the example and fill in your own AWS /
Bedrock / Cognito values (the example file has comments explaining each one):

```bash
cp .env.example .env
docker compose up --build
```

Frontend comes up on http://localhost:3000 and the chat API on http://localhost:8000.

Heads up: `.env` is gitignored on purpose — don't commit real credentials.

## Deploying

The full EKS walkthrough lives in [DEPLOYMENT.md](DEPLOYMENT.md). GitOps layout is
described under `argocd-apps/`. `main` is treated as prod, so anything merged there
goes out through the pipeline.

## A note on the log agent

The log intelligence agent is notify-only by design. It summarises the incident
with Bedrock Claude, gives it a rough P1–P4 severity, and sends you an SNS alert.
It will *not* restart pods or roll anything back for you — I wanted a second pair of
eyes, not an autopilot.

## Status

Still a work in progress and probably always will be. PRs and ideas welcome.
