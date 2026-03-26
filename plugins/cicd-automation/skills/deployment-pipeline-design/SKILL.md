---
name: deployment-pipeline-design
description: Design multi-stage CI/CD pipelines with approval gates, security checks, and deployment orchestration. Use this skill when designing zero-downtime deployment pipelines, implementing canary rollout strategies, setting up multi-environment promotion workflows, or debugging failed deployment gates in CI/CD.
---

# Deployment Pipeline Design

Architecture patterns for multi-stage CI/CD pipelines with approval gates, deployment strategies, and environment promotion workflows.

## Purpose

Design robust, secure deployment pipelines that balance speed with safety through proper stage organization, automated quality gates, and progressive delivery strategies. This skill covers both the structural design of pipeline architecture and the operational patterns for reliable production deployments.

## Input / Output

### What You Provide

- **Application type**: Language/runtime, containerized or bare-metal, monolith or microservices
- **Deployment target**: Kubernetes, ECS, VMs, serverless, or platform-as-a-service
- **Environment topology**: Number of environments (dev/staging/prod), region layout, air-gap requirements
- **Rollout requirements**: Acceptable downtime, rollback SLA, traffic splitting needs, canary vs blue-green preference
- **Gate constraints**: Approval teams, required test coverage thresholds, compliance scans (SAST, DAST, SCA)
- **Monitoring stack**: Prometheus, Datadog, CloudWatch, or other metrics sources used for automated promotion decisions

### What This Skill Produces

- **Pipeline configuration**: Stage definitions, job dependencies, parallelism, and caching strategy
- **Deployment strategy**: Chosen rollout pattern with annotated configuration (canary weights, blue-green switchover, rolling parameters)
- **Health check setup**: Shallow vs deep readiness probes, post-deployment smoke test scripts
- **Gate definitions**: Automated metric thresholds and manual approval workflows
- **Rollback plan**: Automated rollback triggers and manual runbook steps

## When to Use

- Design CI/CD architecture for a new service or platform migration
- Implement deployment gates between environments
- Configure multi-environment pipelines with mandatory security scanning
- Establish progressive delivery with canary or blue-green strategies
- Debug pipelines where stages succeed but production behavior is wrong
- Reduce mean time to recovery by automating rollback on metric degradation

## Pipeline Stages

### Standard Pipeline Flow

```
┌─────────┐   ┌──────┐   ┌─────────┐   ┌────────┐   ┌──────────┐
│  Build  │ → │ Test │ → │ Staging │ → │ Approve│ → │Production│
└─────────┘   └──────┘   └─────────┘   └────────┘   └──────────┘
```

### Detailed Stage Breakdown

1. **Source** - Code checkout, dependency graph resolution
2. **Build** - Compile, package, containerize, sign artifacts
3. **Test** - Unit, integration, SAST/SCA security scans
4. **Staging Deploy** - Deploy to staging environment with smoke tests
5. **Integration Tests** - E2E, contract tests, performance baselines
6. **Approval Gate** - Manual or automated metric-based gate
7. **Production Deploy** - Canary, blue-green, or rolling strategy
8. **Verification** - Deep health checks, synthetic monitoring
9. **Rollback** - Automated rollback on failure signals

## Approval Gate Patterns

### Pattern 1: Manual Approval (GitHub Actions)

```yaml
production-deploy:
  needs: staging-deploy
  environment:
    name: production
    url: https://app.example.com
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to production
      run: kubectl apply -f k8s/production/
```

Environment protection rules in GitHub enforce required reviewers before this job starts. Configure reviewers at **Settings → Environments → production → Required reviewers**.

### Pattern 2: Time-Based Approval (GitLab CI)

```yaml
deploy:production:
  stage: deploy
  script:
    - deploy.sh production
  environment:
    name: production
  when: delayed
  start_in: 30 minutes
  only:
    - main
```

### Pattern 3: Multi-Approver (Azure Pipelines)

```yaml
stages:
  - stage: Production
    dependsOn: Staging
    jobs:
      - deployment: Deploy
        environment:
          name: production
          resourceType: Kubernetes
        strategy:
          runOnce:
            preDeploy:
              steps:
                - task: ManualValidation@0
                  inputs:
                    notifyUsers: "team-leads@example.com"
                    instructions: "Review staging metrics before approving"
```

### Pattern 4: Automated Metric Gate

Use an AnalysisTemplate (Argo Rollouts) or a custom gate script to block promotion when error rates exceed a threshold:

```yaml
# Argo Rollouts AnalysisTemplate — blocks canary promotion automatically
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
  - name: success-rate
    interval: 60s
    successCondition: "result[0] >= 0.95"
    failureCondition: "result[0] < 0.90"
    inconclusiveLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{status!~"5..",job="my-app"}[2m]))
          / sum(rate(http_requests_total{job="my-app"}[2m]))
```

## Deployment Strategies

### Decision Table

| Strategy     | Downtime | Rollback Speed | Cost Impact     | Best For                        |
|-------------|----------|----------------|-----------------|----------------------------------|
| Rolling      | None     | ~minutes       | None            | Most stateless services          |
| Blue-Green   | None     | Instant        | 2x infra (temp) | High-risk or database migrations |
| Canary       | None     | Instant        | Minimal         | High-traffic, metric-driven      |
| Recreate     | Yes      | Fast           | None            | Dev/test, batch jobs             |
| Feature Flag | None     | Instant        | None            | Gradual feature exposure         |

### 1. Rolling Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2         # at most 12 pods during rollout
      maxUnavailable: 1   # at least 9 pods always serving
```

Characteristics: gradual rollout, zero downtime, easy rollback, best for most applications.

### 2. Blue-Green Deployment

```bash
# Switch traffic from blue to green
kubectl apply -f k8s/green-deployment.yaml
kubectl rollout status deployment/my-app-green

# Flip the service selector
kubectl patch service my-app -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback instantly if needed
kubectl patch service my-app -p '{"spec":{"selector":{"version":"blue"}}}'
```

Characteristics: instant switchover, easy rollback, doubles infrastructure cost temporarily, good for high-risk deployments with long warm-up times.

### 3. Canary Deployment (Argo Rollouts)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
      steps:
        - setWeight: 10
        - pause: { duration: 5m }
        - setWeight: 25
        - pause: { duration: 5m }
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 100
```

Characteristics: gradual traffic shift, real-user metric validation, automated promotion or rollback, requires Argo Rollouts or a service mesh.

### 4. Feature Flags

```python
from flagsmith import Flagsmith

flagsmith = Flagsmith(environment_key="API_KEY")

if flagsmith.has_feature("new_checkout_flow"):
    process_checkout_v2()
else:
    process_checkout_v1()
```

Characteristics: deploy without releasing, A/B testing, instant rollback per user segment, granular control independent of deployment.

## Pipeline Orchestration

### Multi-Stage Pipeline Example (GitHub Actions)

```yaml
name: Production Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.build.outputs.image }}
    steps:
      - uses: actions/checkout@v4
      - name: Build and push Docker image
        id: build
        run: |
          IMAGE=myapp:${{ github.sha }}
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Unit tests
        run: make test
      - name: Security scan
        run: trivy image ${{ needs.build.outputs.image }}

  deploy-staging:
    needs: test
    environment:
      name: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: kubectl apply -f k8s/staging/

  integration-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E tests
        run: npm run test:e2e

  deploy-production:
    needs: integration-test
    environment:
      name: production        # blocks here until required reviewers approve
    runs-on: ubuntu-latest
    steps:
      - name: Canary deployment
        run: |
          kubectl apply -f k8s/production/
          kubectl argo rollouts promote my-app

  verify:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: Deep health check
        run: |
          for i in {1..12}; do
            STATUS=$(curl -sf https://app.example.com/health/ready | jq -r '.status')
            [ "$STATUS" = "ok" ] && exit 0
            sleep 10
          done
          exit 1
      - name: Notify on success
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"Production deployment successful: ${{ github.sha }}"}'
```

## Health Checks

### Shallow vs Deep Health Endpoints

A shallow `/ping` returns 200 even when downstream dependencies are broken. Use a deep readiness endpoint that verifies actual dependencies before promoting traffic.

```python
# /health/ready — checks real dependencies, used by pipeline gate
@app.get("/health/ready")
async def readiness():
    checks = {
        "database": await check_db_connection(),
        "cache":    await check_redis_connection(),
        "queue":    await check_queue_connection(),
    }
    status = "ok" if all(checks.values()) else "degraded"
    code = 200 if status == "ok" else 503
    return JSONResponse({"status": status, "checks": checks}, status_code=code)
```

### Post-Deployment Verification Script

```bash
#!/usr/bin/env bash
# verify-deployment.sh — run after every production deploy
set -euo pipefail

ENDPOINT="${1:?usage: verify-deployment.sh <base-url>}"
MAX_ATTEMPTS=12
SLEEP_SECONDS=10

for i in $(seq 1 $MAX_ATTEMPTS); do
  STATUS=$(curl -sf "$ENDPOINT/health/ready" | jq -r '.status' 2>/dev/null || echo "unreachable")
  if [ "$STATUS" = "ok" ]; then
    echo "Health check passed after $((i * SLEEP_SECONDS))s"
    exit 0
  fi
  echo "Attempt $i/$MAX_ATTEMPTS: status=$STATUS — retrying in ${SLEEP_SECONDS}s"
  sleep "$SLEEP_SECONDS"
done

echo "Health check failed after $((MAX_ATTEMPTS * SLEEP_SECONDS))s"
exit 1
```

## Rollback Strategies

### Automated Rollback in Pipeline

```yaml
deploy-and-verify:
  steps:
    - name: Deploy new version
      run: kubectl apply -f k8s/

    - name: Wait for rollout
      run: kubectl rollout status deployment/my-app --timeout=5m

    - name: Post-deployment health check
      id: health
      run: ./scripts/verify-deployment.sh https://app.example.com

    - name: Rollback on failure
      if: failure()
      run: |
        kubectl rollout undo deployment/my-app
        echo "Rolled back to previous revision"
```

### Manual Rollback Commands

```bash
# List revision history with change-cause annotations
kubectl rollout history deployment/my-app

# Rollback to previous version
kubectl rollout undo deployment/my-app

# Rollback to a specific revision
kubectl rollout undo deployment/my-app --to-revision=3

# Verify rollback completed
kubectl rollout status deployment/my-app
```

For advanced rollback strategies including database migration rollbacks and Argo Rollouts abort flows, see [`references/advanced-strategies.md`](references/advanced-strategies.md).

## Monitoring and Metrics

### Key DORA Metrics to Track

| Metric                    | Target (Elite) | How to Measure                           |
|--------------------------|----------------|------------------------------------------|
| Deployment Frequency      | Multiple/day   | Pipeline run count per day               |
| Lead Time for Changes     | < 1 hour       | Commit timestamp → production deploy     |
| Change Failure Rate       | < 5%           | Failed deploys / total deploys           |
| Mean Time to Recovery     | < 1 hour       | Incident open → service restored         |

### Post-Deployment Metric Verification

```yaml
- name: Verify error rate post-deployment
  run: |
    sleep 60  # allow metrics to accumulate

    ERROR_RATE=$(curl -sf "$PROMETHEUS_URL/api/v1/query" \
      --data-urlencode 'query=sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' \
      | jq '.data.result[0].value[1]')

    echo "Current error rate: $ERROR_RATE"
    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "Error rate $ERROR_RATE exceeds 1% threshold — triggering rollback"
      exit 1
    fi
```

## Pipeline Best Practices

1. **Fail fast** — Run quick checks (lint, unit tests) before slow ones (E2E, security scans)
2. **Parallel execution** — Run independent jobs concurrently to minimize total pipeline time
3. **Caching** — Cache dependency layers and build artifacts between runs
4. **Artifact promotion** — Build once, promote the same artifact through all environments
5. **Environment parity** — Keep staging infrastructure as close to production as possible
6. **Secrets management** — Use secret stores (Vault, AWS Secrets Manager, GitHub encrypted secrets) — never hardcode
7. **Deployment windows** — Prefer low-traffic windows; enforce change freeze periods via gate policies
8. **Idempotent deploys** — Ensure re-running a deploy produces the same result
9. **Rollback automation** — Trigger rollback automatically on health check or metric threshold failure
10. **Annotate deployments** — Send deployment markers to monitoring tools (Datadog, Grafana) for correlation

## Troubleshooting

### Health check passes in pipeline but service is unhealthy in production

The pipeline health check is hitting a shallow `/ping` endpoint that returns 200 even when the database is unreachable. Use a deep readiness check that verifies actual dependencies (see Health Checks section above).

### Canary deployment never promotes to 100%

Argo Rollouts requires a valid `AnalysisTemplate` to auto-promote. If the Prometheus query returns no data (e.g., metric name changed), the analysis stays inconclusive and promotion stalls. Add `inconclusiveLimit` so the rollout fails fast rather than hanging:

```yaml
spec:
  metrics:
  - name: error-rate
    failureCondition: "result[0] > 0.05"
    inconclusiveLimit: 2   # fail after 2 inconclusive results, not hang indefinitely
    provider:
      prometheus:
        query: |
          sum(rate(http_requests_total{status=~"5.."}[2m]))
          / sum(rate(http_requests_total[2m]))
```

### Staging deploy succeeds but production job never starts

Check that production environment protection rules are configured — a missing reviewer assignment means the approval gate waits indefinitely with no notification. In GitHub Actions, ensure `Required reviewers` is set to an existing user or team in **Settings → Environments → production**.

### Docker layer cache busted on every run causing slow builds

If `COPY . .` appears before dependency installation, any source file change invalidates the dependency layer. Reorder to copy dependency manifests first:

```dockerfile
# Good: dependencies cached separately from source code
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
```

### Rollback leaves database migrations applied to old code

A service rollback without a migration rollback causes schema/code mismatch errors. Always make migrations backward-compatible (additive only) for at least one release cycle, and keep undo scripts versioned alongside the migration:

```bash
# migrations/V20240315__add_nullable_column.sql       (forward)
# migrations/V20240315__add_nullable_column.undo.sql  (backward)
```

Never run destructive migrations (DROP COLUMN, ALTER NOT NULL) until the old code version is fully retired from all environments.

## Advanced Topics

For platform-specific pipeline configurations, multi-region promotion workflows, and advanced Argo Rollouts patterns, see:

- [`references/advanced-strategies.md`](references/advanced-strategies.md) — Extended YAML examples, platform-specific configs (GitHub Actions, GitLab CI, Azure Pipelines), multi-region canary patterns, and database migration rollback strategies

## Related Skills

- `github-actions-templates` - For GitHub Actions implementation patterns and reusable workflows
- `gitlab-ci-patterns` - For GitLab CI/CD pipeline implementation
- `secrets-management` - For secrets handling in CI/CD pipelines
