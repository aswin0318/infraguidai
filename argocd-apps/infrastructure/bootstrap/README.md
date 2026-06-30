# Bootstrap (one-time)

Run after `terraform apply` has created the EKS cluster, and after substituting
all `CHANGE_ME` placeholders (see [../../README.md](../../README.md)).

```bash
# 1. Point kubectl at the cluster
aws eks update-kubeconfig --name infraguidai-prod --region us-east-1

# 2. Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd rollout status deploy/argocd-server

# 3. App namespace, IRSA service account, log-intel RBAC
kubectl apply -f argocd-apps/infrastructure/bootstrap/namespace.yaml
kubectl apply -f argocd-apps/infrastructure/bootstrap/serviceaccount.yaml
kubectl apply -f argocd-apps/infrastructure/bootstrap/rbac-log-intel.yaml

# 4. AppProject, then the root app-of-apps (ArgoCD reconciles everything else)
kubectl apply -f argocd-apps/projects/infraguid.yaml
kubectl apply -f argocd-apps/app-of-apps.yaml

# 5. ArgoCD admin password (UI/CLI login)
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d; echo
```

ArgoCD then syncs `infra/` (ALB controller, metrics-server, fluent-bit, redis,
ingress) and `apps/` (the five microservices). Confirm with:

```bash
kubectl get applications -n argocd
kubectl get ingress -n infraguid   # note the ALB address
```

Finally, point your Route53 record at the ALB hostname (or add an alias record),
then browse to https://<your-domain>.
