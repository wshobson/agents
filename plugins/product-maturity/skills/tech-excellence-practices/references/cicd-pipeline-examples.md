# CI/CD Pipeline Examples from FAANG

## GitHub Actions Example (Google-style)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '18'

jobs:
  # Stage 1: Build
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Cache build artifacts
        uses: actions/cache@v3
        with:
          path: ./dist
          key: build-${{ github.sha }}

  # Stage 2: Test (parallel)
  unit-tests:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npm ci
      - name: Run unit tests
        run: npm run test:unit -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  integration-tests:
    needs: build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npm ci
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  e2e-tests:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npm ci
      - name: Run E2E tests
        run: npm run test:e2e
      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-screenshots
          path: ./test-results

  # Stage 3: Quality Gates
  quality:
    needs: [unit-tests, integration-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Security scan
        run: npm audit --audit-level=high

      - name: Dependency check
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  # Stage 4: Deploy to Staging
  deploy-staging:
    needs: [unit-tests, integration-tests, e2e-tests, quality]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to staging
        run: |
          aws ecs update-service \
            --cluster staging-cluster \
            --service app-service \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster staging-cluster \
            --services app-service

      - name: Smoke tests
        run: npm run test:smoke
        env:
          API_URL: https://staging-api.example.com

  # Stage 5: Deploy to Production (with approval)
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      # Blue-Green Deployment
      - name: Deploy new version (green)
        run: |
          # Deploy to new target group
          aws ecs create-service \
            --cluster prod-cluster \
            --service-name app-service-green \
            --task-definition app-task:${{ github.sha }}

      - name: Health check
        run: |
          # Wait and verify health
          sleep 60
          curl -f https://green.example.com/health || exit 1

      - name: Switch traffic
        run: |
          # Update load balancer to point to green
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.LISTENER_ARN }} \
            --default-actions TargetGroupArn=${{ secrets.GREEN_TG_ARN }}

      - name: Monitor metrics
        run: |
          # Check error rate, latency for 10 minutes
          npm run monitor -- --duration 600

      - name: Cleanup old version (blue)
        run: |
          # Delete old service
          aws ecs delete-service \
            --cluster prod-cluster \
            --service app-service-blue \
            --force

  # Rollback job (manual trigger)
  rollback:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    environment:
      name: production
    steps:
      - name: Rollback to previous version
        run: |
          aws ecs update-service \
            --cluster prod-cluster \
            --service app-service \
            --task-definition app-task:previous
```

## AWS CodePipeline Example (Amazon-style)

```yaml
# buildspec.yml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}

  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG

  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG
      - echo Writing image definitions file...
      - printf '[{"name":"%s","imageUri":"%s"}]' $CONTAINER_NAME $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG > imagedefinitions.json

      # Run tests
      - echo Running tests...
      - docker run $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG npm test

      # Security scan
      - echo Scanning for vulnerabilities...
      - aws ecr start-image-scan --repository-name $IMAGE_REPO_NAME --image-id imageTag=$IMAGE_TAG

artifacts:
  files:
    - imagedefinitions.json
    - appspec.yml
```

## GitLab CI Example (Meta-style)

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - staging
  - canary
  - production

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

# Build stage
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build --cache-from $CI_REGISTRY_IMAGE:latest -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - merge_requests

# Test stages (parallel)
unit-tests:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm run test:unit -- --coverage --maxWorkers=4
  coverage: '/Statements\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

integration-tests:
  stage: test
  image: node:18
  services:
    - postgres:14
    - redis:7
  variables:
    POSTGRES_DB: test
    POSTGRES_PASSWORD: test
  script:
    - npm ci
    - npm run test:integration

e2e-tests:
  stage: test
  image: mcr.microsoft.com/playwright:latest
  script:
    - npm ci
    - npx playwright install
    - npm run test:e2e
  artifacts:
    when: on_failure
    paths:
      - test-results/
    expire_in: 1 week

# Security stage
sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json -o sast-report.json
  artifacts:
    reports:
      sast: sast-report.json

dependency-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --severity HIGH,CRITICAL $IMAGE_TAG

# Staging deployment
deploy-staging:
  stage: staging
  image: google/cloud-sdk:alpine
  script:
    - gcloud auth activate-service-account --key-file=$GCP_SERVICE_KEY
    - gcloud run deploy app-staging
        --image $IMAGE_TAG
        --platform managed
        --region us-central1
    - sleep 30
    - curl -f https://staging.example.com/health || exit 1
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main

# Canary deployment (1%)
deploy-canary:
  stage: canary
  image: google/cloud-sdk:alpine
  script:
    - gcloud run services update-traffic app-production
        --to-revisions=LATEST=1,PREVIOUS=99

    # Monitor for 15 minutes
    - |
      for i in {1..15}; do
        ERROR_RATE=$(curl -s https://api.example.com/metrics/errors)
        if [ $ERROR_RATE -gt 1 ]; then
          echo "Error rate too high: $ERROR_RATE%"
          gcloud run services update-traffic app-production --to-revisions=PREVIOUS=100
          exit 1
        fi
        sleep 60
      done
  environment:
    name: production-canary
    url: https://example.com
  only:
    - main
  when: manual

# Full production deployment
deploy-production:
  stage: production
  image: google/cloud-sdk:alpine
  script:
    # Gradual rollout: 10%, 50%, 100%
    - gcloud run services update-traffic app-production --to-revisions=LATEST=10,PREVIOUS=90
    - sleep 300  # 5 minutes
    - ./scripts/check-metrics.sh || exit 1

    - gcloud run services update-traffic app-production --to-revisions=LATEST=50,PREVIOUS=50
    - sleep 300
    - ./scripts/check-metrics.sh || exit 1

    - gcloud run services update-traffic app-production --to-revisions=LATEST=100
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

## Netflix-style Deployment with Spinnaker

```json
// spinnaker-pipeline.json
{
  "name": "Deploy to Production",
  "application": "myapp",
  "stages": [
    {
      "type": "bake",
      "name": "Bake AMI",
      "baseOs": "ubuntu",
      "package": "myapp",
      "regions": ["us-east-1"]
    },
    {
      "type": "deploy",
      "name": "Deploy Canary",
      "clusters": [{
        "account": "prod",
        "application": "myapp",
        "capacity": {
          "min": 1,
          "max": 1,
          "desired": 1
        },
        "strategy": "highlander"
      }]
    },
    {
      "type": "wait",
      "name": "Canary Analysis Period",
      "waitTime": 1800
    },
    {
      "type": "kayentaCanary",
      "name": "Canary Analysis",
      "canaryConfig": {
        "scoreThresholds": {
          "pass": 90,
          "marginal": 75
        },
        "metrics": [
          {
            "name": "Error Rate",
            "query": "sum:errors{app:myapp}/sum:requests{app:myapp}",
            "direction": "decrease"
          },
          {
            "name": "Latency p99",
            "query": "p99:latency{app:myapp}",
            "direction": "decrease"
          }
        ]
      }
    },
    {
      "type": "checkPreconditions",
      "name": "Check Canary Results",
      "preconditions": [{
        "type": "expression",
        "context": {
          "expression": "${ canaryScore >= 90 }"
        }
      }]
    },
    {
      "type": "deploy",
      "name": "Deploy to All Regions",
      "clusters": [
        {
          "account": "prod",
          "application": "myapp",
          "region": "us-east-1",
          "capacity": {"desired": 10}
        },
        {
          "account": "prod",
          "application": "myapp",
          "region": "us-west-2",
          "capacity": {"desired": 10}
        },
        {
          "account": "prod",
          "application": "myapp",
          "region": "eu-west-1",
          "capacity": {"desired": 5}
        }
      ],
      "strategy": "redblack"
    }
  ],
  "triggers": [{
    "type": "jenkins",
    "job": "myapp-build",
    "master": "jenkins-master"
  }]
}
```

## Key Patterns Summary

### Google Pattern
- Trunk-based development
- Hermetic builds
- Extensive pre-submit checks
- Canary deployments

### Amazon/AWS Pattern
- Multi-stage validation (gamma → production)
- One-box deploy first
- Regional rollout
- Automated rollback on metrics

### Meta Pattern
- Fast iteration
- Parallel testing
- A/B testing integration
- Gradual rollout with monitoring

### Netflix Pattern
- Immutable infrastructure
- Chaos testing integrated
- Red/black deployments
- Multi-region orchestration

## Common Anti-Patterns to Avoid

❌ **Manual steps in pipeline**: Automate everything
❌ **Long-running tests**: Parallelize and optimize
❌ **No rollback capability**: Always have a way back
❌ **Deploy without monitoring**: Instrument first
❌ **No gradual rollout**: Start small, expand gradually
❌ **Ignoring failed tests**: Tests must be gates
❌ **No security scanning**: Shift security left
