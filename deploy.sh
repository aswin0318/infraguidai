#!/usr/bin/env bash
# =====================================================================
# InfraGuidAI — end-to-end deploy (post-terraform).
# Builds & pushes images, installs cluster add-ons (AWS LBC with Gateway
# API), bootstraps the app, deploys microservices, wires Route53, and
# verifies https://nutritrack360.in.
#
# Prereqs: terraform applied, docker running, aws/kubectl/helm on PATH.
# Run from the repo root:  bash deploy.sh
# =====================================================================
set -euo pipefail

REGION="us-east-1"
NAMESPACE="infraguid"
DOMAIN="nutritrack360.in"
TF="terraform -chdir=terraform"
LBC_CHART_VERSION="3.4.0"    # AWS LBC v3.4.0 (Gateway API GA, ALB L7)
GWAPI_VERSION="v1.2.1"

say() { echo -e "\n\033[1;36m==> $*\033[0m"; }

# ---------------------------------------------------------------------
say "Reading terraform outputs"
ECR_REGISTRY=$($TF output -raw ecr_registry_url)
EKS_CLUSTER=$($TF output -raw eks_cluster_name)
ACM_ARN=$($TF output -raw acm_certificate_arn)
VPC_ID=$($TF output -raw vpc_id)
ALB_IRSA=$($TF output -raw irsa_alb_controller_role_arn)
APP_IRSA=$($TF output -raw irsa_app_role_arn)
FLUENT_IRSA=$($TF output -raw irsa_fluent_bit_role_arn)
USER_POOL_ID=$($TF output -raw cognito_user_pool_id)
APP_CLIENT_ID=$($TF output -raw cognito_app_client_id)
KB_BUCKET=$($TF output -raw knowledge_base_bucket_name)
ZONE_ID=$(aws route53 list-hosted-zones-by-name --dns-name "$DOMAIN" \
  --query "HostedZones[0].Id" --output text | cut -d'/' -f3)
echo "registry=$ECR_REGISTRY cluster=$EKS_CLUSTER zone=$ZONE_ID"

# ---------------------------------------------------------------------
say "Phase 2: build & push images to ECR"
aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"

build_push() {
  local svc="$1" dockerfile="$2"
  echo "--- $svc"
  docker build -q -t "$ECR_REGISTRY/infragui/$svc:latest" -f "$dockerfile" . >/dev/null
  docker push -q "$ECR_REGISTRY/infragui/$svc:latest"
}
build_push chat-service      services/chat-service/Dockerfile
build_push agent-service     services/agent-service/Dockerfile
build_push rag-service       services/rag-service/Dockerfile
build_push ingestion-service services/ingestion-service/Dockerfile
build_push frontend          frontend/Dockerfile

# ---------------------------------------------------------------------
say "Phase 3: kubeconfig + Gateway API CRDs + bootstrap"
aws eks update-kubeconfig --name "$EKS_CLUSTER" --region "$REGION"

kubectl apply -f "https://github.com/kubernetes-sigs/gateway-api/releases/download/${GWAPI_VERSION}/standard-install.yaml"

kubectl apply -f argocd-apps/infrastructure/bootstrap/namespace.yaml
sed "s|CHANGE_ME_irsa_app_role_arn|$APP_IRSA|" \
  argocd-apps/infrastructure/bootstrap/serviceaccount.yaml | kubectl apply -f -
kubectl apply -f argocd-apps/infrastructure/bootstrap/rbac-log-intel.yaml

# ---------------------------------------------------------------------
say "Phase 4: AWS Load Balancer Controller (Gateway API enabled)"
helm repo add eks https://aws.github.io/eks-charts >/dev/null 2>&1 || true
helm repo update >/dev/null
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system --version "$LBC_CHART_VERSION" \
  --set clusterName="$EKS_CLUSTER" \
  --set region="$REGION" \
  --set vpcId="$VPC_ID" \
  --set serviceAccount.create=true \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set "serviceAccount.annotations.eks\.amazonaws\.com/role-arn=$ALB_IRSA" \
  --set controllerConfig.featureGates.ALBGatewayAPI=true \
  --wait --timeout 5m

say "Phase 4b: metrics-server + redis"
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/ >/dev/null 2>&1 || true
helm upgrade --install metrics-server metrics-server/metrics-server \
  -n kube-system --set 'args={--kubelet-insecure-tls}' --wait --timeout 3m || true
kubectl apply -f argocd-apps/infrastructure/redis/redis.yaml

# ---------------------------------------------------------------------
say "Phase 5: knowledge base -> S3"
aws s3 sync knowledge-base "s3://$KB_BUCKET" --delete --region "$REGION" || true

# ---------------------------------------------------------------------
say "Phase 6: deploy microservices"
deploy_svc() {
  local svc="$1"; shift
  helm upgrade --install "$svc" "argocd-apps/microservices/$svc" -n "$NAMESPACE" \
    --set image.repository="$ECR_REGISTRY/infragui/$svc" \
    --set image.tag=latest \
    --set image.pullPolicy=Always \
    "$@"
}
deploy_svc rag-service
deploy_svc agent-service
deploy_svc ingestion-service --set knowledgeBaseBucket="$KB_BUCKET"
deploy_svc chat-service --set env.FRONTEND_ORIGIN="https://$DOMAIN"
deploy_svc frontend \
  --set cognito.userPoolId="$USER_POOL_ID" \
  --set cognito.appClientId="$APP_CLIENT_ID" \
  --set cognito.region="$REGION"

# ---------------------------------------------------------------------
say "Phase 7: Gateway API resources (ALB)"
sed "s|REPLACE_ACM_ARN|$ACM_ARN|g" \
  argocd-apps/infrastructure/ingress/ingress.yaml | kubectl apply -f -

say "Waiting for ALB address on the Gateway..."
ALB_DNS=""
for i in $(seq 1 40); do
  ALB_DNS=$(kubectl get gateway infraguid -n "$NAMESPACE" \
    -o jsonpath='{.status.addresses[0].value}' 2>/dev/null || true)
  [ -n "$ALB_DNS" ] && break
  sleep 15
done
[ -z "$ALB_DNS" ] && { echo "ERROR: ALB address not assigned yet"; exit 1; }
echo "ALB_DNS=$ALB_DNS"

# ---------------------------------------------------------------------
say "Phase 8: Route53 alias records -> ALB"
# us-east-1 ALB canonical hosted zone id
ALB_ZONE="Z35SXDOTRQ7X7K"
cat > /tmp/r53.json <<JSON
{
  "Changes": [
    {"Action":"UPSERT","ResourceRecordSet":{"Name":"$DOMAIN","Type":"A",
      "AliasTarget":{"HostedZoneId":"$ALB_ZONE","DNSName":"$ALB_DNS","EvaluateTargetHealth":true}}},
    {"Action":"UPSERT","ResourceRecordSet":{"Name":"www.$DOMAIN","Type":"A",
      "AliasTarget":{"HostedZoneId":"$ALB_ZONE","DNSName":"$ALB_DNS","EvaluateTargetHealth":true}}}
  ]
}
JSON
aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" \
  --change-batch file:///tmp/r53.json

say "Done. Verifying https://$DOMAIN (may take a few minutes for DNS + targets)"
for i in $(seq 1 20); do
  if curl -skf "https://$DOMAIN/api/health" >/dev/null; then
    echo "SUCCESS: https://$DOMAIN is live"; exit 0
  fi
  sleep 20
done
echo "Health check not green yet — check 'kubectl get pods -n $NAMESPACE' and target group health."
