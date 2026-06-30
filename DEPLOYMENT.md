# InfraGuidAI — EKS Deployment Guide

End-to-end deploy of InfraGuidAI to **EKS (2 nodes)** with GitOps (ArgoCD), ECR,
the CS-02 Log Intelligence Lambda, and GitHub-flow CI/CD (main = production).

## Architecture

```
                      ┌──────────── GitHub (main) ────────────┐
                      │  CI/CD: build → ECR → bump Helm tag    │
                      └───────────────────┬────────────────────┘
                                          │ ArgoCD syncs argocd-apps/
 Route53 → ACM/ALB Ingress ──────────────▼───────────────────────────────
   /      → frontend (nginx pod)                          EKS (2x t3.large)
   /api   → chat-service ─→ agent-service ─→ rag-service ─→ (Bedrock)
                         └─→ ingestion-service          └─→ RDS pgvector
   chat-service ─→ redis (in-cluster)                       (Secrets Manager via IRSA)

 Pods → Fluent Bit → CloudWatch Logs ──(anomaly filter)──► log-intel Lambda
                                                            → Bedrock Claude → SNS → admin
```

## 0. Manual prerequisites

1. **Bedrock model access** (region `us-east-1`): enable Claude (default
   `us.anthropic.claude-3-5-sonnet-20241022-v2:0`), Llama 3.1, Titan Embeddings.
2. **Terraform backend** exists: S3 `infraguidai-tfstate-901607650789` +
   DynamoDB `infraguidai-tfstate-lock` (or edit the backend block in
   `terraform/main.tf`).
3. **Route53 hosted zone** for your domain; set `domain_name` + `hosted_zone_id`.
4. **SNS email**: set `alert_email`; confirm the subscription email after apply.
5. **GitHub repo variables** (Settings → Secrets and variables → Actions →
   *Variables*): `AWS_DEPLOY_ROLE_ARN`, `AWS_REGION`, `ALERTS_TOPIC_ARN`,
   `LAMBDA_ARTIFACTS_BUCKET`. **Secret:** `SNYK_TOKEN`. (Create a GitHub OIDC
   provider + deploy role in IAM and trust this repo.)
6. Local CLIs: `awscli`, `kubectl`, `helm`, `argocd`.

## 1. Provision infrastructure (Terraform)

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # fill in your values
terraform init
terraform apply
```

Creates: VPC (EKS-tagged subnets), EKS + 2-node group, ECR repos
(`infragui/*`), new S3 buckets, IRSA roles, SNS topic, Fluent Bit log group +
anomaly subscription filter, and the log-intel Lambda. Note the outputs — you'll
substitute several into the GitOps files (`terraform output`).

## 2. Build & push the first images

Either let CI publish on first merge to `main`, or one-time manually:

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ecr_registry_url>
for s in chat-service agent-service rag-service ingestion-service; do
  docker build -f services/$s/Dockerfile -t <ecr_registry_url>/infragui/$s:main-bootstrap .
  docker push <ecr_registry_url>/infragui/$s:main-bootstrap
done
docker build -f frontend/Dockerfile -t <ecr_registry_url>/infragui/frontend:main-bootstrap .
docker push <ecr_registry_url>/infragui/frontend:main-bootstrap
```

Set the matching `image.tag` in each `argocd-apps/microservices/*/values.yaml`.

**Seed the knowledge base** (the ingestion pod syncs this bucket on startup):

```bash
aws s3 sync knowledge-base/ s3://<knowledge_base_bucket_name>/
```

After the app is up, trigger ingestion once: `POST /api/admin/ingest` (admin auth).

## 3. Fill GitOps placeholders

Substitute every `CHANGE_ME` (see `argocd-apps/README.md`) from Terraform
outputs: repo URL, `ecr_registry_url`, `irsa_*_role_arn`, `vpc_id`,
`acm_certificate_arn`, Cognito ids, `knowledge_base_bucket_name`, your domain.

## 4. Bootstrap the cluster (one-time)

Follow `argocd-apps/infrastructure/bootstrap/README.md`:
install ArgoCD → apply namespace/SA/RBAC → apply AppProject → apply
`app-of-apps.yaml`. ArgoCD then reconciles `infra/` then `apps/`.

## 5. DNS

```bash
kubectl get ingress -n infraguid     # copy the ALB hostname
```

Point your Route53 record (alias A) at the ALB.

## 6. Verify

| Check | Command / action | Expect |
|---|---|---|
| Nodes | `kubectl get nodes` | 2 Ready |
| ArgoCD | `kubectl get applications -n argocd` | all Synced/Healthy |
| API | `curl https://<domain>/api/health` | `200` |
| App | open `https://<domain>` | frontend loads, chat works |
| **Log agent** | see below | SNS email with P-severity summary |

**Induce a crash to test CS-02:**

```bash
kubectl run boom --image=busybox -n infraguid --restart=Always -- /bin/sh -c "echo CrashLoopBackOff; exit 1"
# Fluent Bit ships the line → CloudWatch anomaly filter → Lambda → Bedrock → SNS.
# Check the function ran:
aws logs tail /aws/lambda/infraguidai-prod-log-intel --since 5m
kubectl delete pod boom -n infraguid
```

You should receive an SNS email subjected `[Px] CrashLoopBackOff in boom` with a
root-cause hypothesis and suggested fix.

## CI/CD recap (GitHub flow, production only)

- **PR → main:** lint → SCA (Snyk) → docker build + Trivy → quality gate;
  SNS notify on critical findings.
- **push → main:** build/push image to ECR (`main-<sha>`) → bump Helm tag → ArgoCD deploys.
- **GitHub Release:** publish image (`<release-tag>`) → bump Helm tag → deploy.
- **`terraform/**`:** fmt/validate/plan on PR, apply on push to main.
- **`services/log-intel-lambda/**`:** zip → upload → `update-function-code`.
