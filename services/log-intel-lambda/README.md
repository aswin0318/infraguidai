# CS-02 Kubernetes Log Intelligence Agent (Lambda)

Event-triggered AWS Lambda that analyzes Kubernetes pod-log anomalies after
deployments and notifies the on-call engineer via SNS. Provisioned by
`terraform/modules/log-intel-lambda`.

## Flow

```
Pods → Fluent Bit (DaemonSet) → CloudWatch Logs (/infraguid/prod/pod-logs)
     → subscription filter (anomaly pattern) → THIS Lambda
     → Bedrock Claude (summary + P1–P4) → SNS → admin email
```

The Lambda runs **only** when a matching anomaly line is logged — it is not a
background process and does not touch the application's request path.

## Detected anomalies

`OOMKilled`, `CrashLoopBackOff`, `ImagePullBackOff` / `ErrImagePull`,
liveness/readiness probe failures, back-off restarts. See `collect.py`.

## Files

| File | Responsibility |
|---|---|
| `handler.py` | Decode CloudWatch Logs event, orchestrate per incident |
| `collect.py` | Parse Fluent Bit records → incidents; enrich from CloudWatch |
| `summarize.py` | Bedrock Claude summary + severity (heuristic fallback) |
| `notify.py` | `sns:Publish` the formatted alert |

## Environment (set by Terraform)

`SNS_TOPIC_ARN`, `BEDROCK_MODEL_ID`, `LOG_GROUP_NAME`, `EKS_CLUSTER_NAME`,
`ARGOCD_SECRET_ARN`, `ENABLE_ARGOCD`.

## Packaging

No third-party deps — the runtime bundles boto3. Terraform zips this directory
(`archive_file`) at apply time; CI re-zips and calls `update-function-code` on
changes (`.github/workflows/log-intel-lambda.yml`).
