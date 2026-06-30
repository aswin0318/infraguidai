# InfraGuidAI — ArgoCD GitOps

GitOps source of truth for the InfraGuidAI EKS deployment. ArgoCD watches this
directory and reconciles the cluster to match `main`.

## Structure

```
argocd-apps/
├── app-of-apps.yaml      # root Application -> syncs apps/ and infra/
├── values.yaml           # global reference values (registry, domain, ARNs)
├── projects/
│   └── infraguid.yaml     # ArgoCD AppProject
├── apps/                 # one Application per microservice
│   ├── chat-service.yaml  agent-service.yaml  rag-service.yaml
│   ├── ingestion-service.yaml  frontend.yaml
├── infra/                # one Application per cluster add-on
│   ├── aws-load-balancer-controller.yaml  metrics-server.yaml
│   ├── fluent-bit.yaml  redis.yaml  ingress.yaml
├── infrastructure/
│   ├── bootstrap/        # namespace, app service account, log-intel RBAC
│   ├── redis/            # in-cluster Redis manifests
│   └── ingress/          # ALB Ingress manifest
└── microservices/        # Helm charts (incl. frontend)
    ├── chat-service/  agent-service/  rag-service/
    ├── ingestion-service/  frontend/
```

The CS-02 **Log Intelligence Agent is a Lambda** (Terraform), not a chart here.
`infra/fluent-bit.yaml` is its trigger source (pod logs -> CloudWatch -> Lambda).

## Values to fill in (search for `CHANGE_ME`)

After `terraform apply`, take these outputs and substitute them:

| Placeholder | Source |
|---|---|
| repo URL `github.com/CHANGE_ME/infraguid` | your GitHub repo |
| `ecrRegistry` / image `repository` prefix | `terraform output ecr_registry_url` |
| app SA role ARN | `terraform output irsa_app_role_arn` |
| ALB controller role ARN | `terraform output irsa_alb_controller_role_arn` |
| fluent-bit role ARN | `terraform output irsa_fluent_bit_role_arn` |
| `vpcId` (alb controller) | `terraform output vpc_id` |
| ingress `certificate-arn` | `terraform output acm_certificate_arn` |
| frontend Cognito ids | `terraform output cognito_user_pool_id` / `cognito_app_client_id` |
| ingestion `knowledgeBaseBucket` | `terraform output knowledge_base_bucket_name` |
| domain / host | your domain |

Quick repo-URL substitution:

```bash
grep -rl 'CHANGE_ME/infraguid' argocd-apps | xargs sed -i 's#github.com/CHANGE_ME/infraguid#github.com/<owner>/infraguid#g'
```

## Bootstrap (one-time)

See [infrastructure/bootstrap/README.md](infrastructure/bootstrap/README.md).
