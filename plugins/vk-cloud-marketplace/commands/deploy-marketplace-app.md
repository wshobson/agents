---
name: deploy-marketplace-app
description: Automated deployment of image-based applications to VK Cloud marketplace. Handles build, validation, testing, and submission.
---

# Deploy Marketplace App

Automates the complete workflow for deploying image-based applications to VK Cloud marketplace, from building container images to submitting applications for approval.

## Purpose

This command orchestrates the entire deployment pipeline including:
- Docker image building and optimization
- Security vulnerability scanning
- Configuration validation
- Local testing
- Image registry push
- Marketplace submission
- Status monitoring

## Prerequisites

Before running this command, ensure:

1. **Docker**: Installed and running
2. **VK Cloud Credentials**: API token and vendor ID configured
3. **Application Manifest**: `application.yaml` file present in project root
4. **Dockerfile**: Present in project root
5. **Dependencies**: `curl`, `jq`, `yq` installed

## Configuration

Set the following environment variables:

```bash
# Required
export VK_CLOUD_API_TOKEN="your-api-token"
export VK_CLOUD_VENDOR_ID="your-vendor-id"
export APP_NAME="my-application"
export APP_VERSION="1.0.0"

# Optional
export IMAGE_REGISTRY="registry.vkcloud.io"
export MANIFEST_FILE="application.yaml"
export API_BASE_URL="https://api.cloud.vk.com/marketplace/v1"
```

## Usage

### Interactive Mode

When you invoke this command, I will guide you through the deployment process:

1. **Gather Information**
   - Prompt for application name and version
   - Check for VK Cloud credentials
   - Verify required files exist

2. **Validate Configuration**
   - Validate application manifest syntax
   - Check required manifest fields
   - Verify Docker configuration

3. **Build and Test**
   - Build Docker image with optimizations
   - Run security vulnerability scan
   - Test container locally
   - Verify health checks

4. **Deploy to Marketplace**
   - Push image to VK Cloud registry
   - Submit application manifest
   - Monitor submission status
   - Report approval status

### Automated Mode

For CI/CD integration, use the provided automation script:

```bash
# Clone the deployment script
cd your-project

# Set environment variables
export VK_CLOUD_API_TOKEN="your-token"
export VK_CLOUD_VENDOR_ID="your-vendor-id"
export APP_NAME="my-app"
export APP_VERSION="1.0.0"

# Run deployment
./scripts/vk-cloud-deploy.sh deploy
```

## Workflow Steps

### Step 1: Preparation

```
[Verify prerequisites]
├─ Check Docker installation
├─ Verify credentials
├─ Validate manifest file
└─ Check Dockerfile
```

I will validate your environment and configuration before proceeding.

### Step 2: Image Building

```
[Build container image]
├─ Analyze Dockerfile
├─ Optimize build arguments
├─ Execute multi-stage build
├─ Tag image appropriately
└─ Verify build success
```

I will build your Docker image with optimizations and best practices.

### Step 3: Security Scanning

```
[Scan for vulnerabilities]
├─ Run Trivy scanner
├─ Check CVE database
├─ Analyze severity levels
├─ Generate scan report
└─ Fail on critical issues
```

Images with HIGH or CRITICAL vulnerabilities will be rejected.

### Step 4: Local Testing

```
[Test deployment]
├─ Run container locally
├─ Wait for startup
├─ Test health endpoints
├─ Verify functionality
└─ Cleanup test container
```

I will ensure your application starts correctly and passes health checks.

### Step 5: Registry Push

```
[Push to registry]
├─ Authenticate with registry
├─ Tag image for VK Cloud
├─ Push image layers
├─ Verify push success
└─ Record image digest
```

Your image will be pushed to VK Cloud container registry.

### Step 6: Marketplace Submission

```
[Submit to marketplace]
├─ Convert manifest to JSON
├─ Submit via API
├─ Receive application ID
├─ Monitor review status
└─ Report approval
```

I will submit your application and track its approval status.

## Example Interaction

```
You: /deploy-marketplace-app

Claude: I'll help you deploy your application to VK Cloud marketplace.

First, let me gather some information:

1. Application name: my-awesome-app
2. Version: 1.0.0
3. VK Cloud API token: [Found in environment]
4. Vendor ID: [Found in environment]

Validating configuration...
✓ Manifest file found: application.yaml
✓ Dockerfile found
✓ Manifest validation passed

Building Docker image...
✓ Image built: registry.vkcloud.io/my-awesome-app:1.0.0

Scanning for vulnerabilities...
✓ Security scan passed (0 critical, 0 high severity issues)

Testing deployment locally...
✓ Container started successfully
✓ Health check passed
✓ Local testing completed

Pushing to VK Cloud registry...
✓ Image pushed successfully

Submitting to marketplace...
✓ Application submitted (ID: app-abc123)

Monitoring submission status...
✓ Status: pending review

Your application has been submitted successfully!
Application ID: app-abc123

You can check the status with:
./scripts/vk-cloud-deploy.sh status
```

## Validation Rules

### Manifest Validation

The command validates your manifest against these rules:

1. **Required Fields**
   - `metadata.name`: Must be lowercase, alphanumeric with hyphens
   - `metadata.version`: Must follow semantic versioning
   - `metadata.description`: Minimum 50 characters
   - `spec.image.repository`: Valid registry URL
   - `spec.image.tag`: Must match metadata.version

2. **Resource Requirements**
   - CPU: Between 100m and 32000m
   - Memory: Between 128Mi and 128Gi
   - Storage: Between 1Gi and 1000Gi

3. **Health Checks**
   - At least one health check required
   - Readiness check recommended
   - Liveness check mandatory

4. **Security**
   - Must run as non-root user
   - No privileged containers
   - Read-only root filesystem recommended

### Image Validation

Your Docker image must pass these checks:

1. **Security**
   - No critical or high severity CVEs
   - Runs as non-root user
   - No hardcoded secrets
   - Minimal attack surface

2. **Optimization**
   - Size under 2GB recommended
   - Uses layer caching effectively
   - Multi-stage build preferred

3. **Configuration**
   - Health check endpoint implemented
   - Graceful shutdown handling
   - Proper signal handling

## Troubleshooting

### Build Failures

**Issue**: Docker build fails
```
Solution:
1. Check Dockerfile syntax
2. Verify base image is accessible
3. Review build logs for specific errors
4. Ensure dependencies are available
```

**Issue**: Image too large
```
Solution:
1. Use multi-stage builds
2. Choose minimal base image (Alpine, distroless)
3. Clean up package manager caches
4. Remove unnecessary files with .dockerignore
```

### Security Scan Failures

**Issue**: Critical vulnerabilities detected
```
Solution:
1. Update base image to latest version
2. Update dependencies to patched versions
3. Review CVE details and apply fixes
4. Consider alternative packages
```

### Deployment Failures

**Issue**: Container fails to start
```
Solution:
1. Check application logs
2. Verify environment variables
3. Test locally with same configuration
4. Review resource limits
```

**Issue**: Health check fails
```
Solution:
1. Verify health check endpoint exists
2. Check endpoint returns 200 status
3. Increase initialDelaySeconds
4. Review application startup time
```

### Submission Failures

**Issue**: API authentication fails
```
Solution:
1. Verify VK_CLOUD_API_TOKEN is set
2. Check token hasn't expired
3. Verify vendor ID is correct
4. Test API access with curl
```

**Issue**: Manifest validation rejected
```
Solution:
1. Review error message details
2. Check manifest against requirements
3. Validate YAML syntax
4. Ensure all required fields present
```

## Automation Script

A complete automation script is available in the skill references:

```bash
# Download the script
curl -O https://raw.githubusercontent.com/example/scripts/vk-cloud-deploy.sh

# Make executable
chmod +x vk-cloud-deploy.sh

# Run deployment
./vk-cloud-deploy.sh deploy

# Check status
./vk-cloud-deploy.sh status

# Validate only
./vk-cloud-deploy.sh validate
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to VK Cloud Marketplace

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y curl jq
          sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
          sudo chmod +x /usr/local/bin/yq

      - name: Deploy to marketplace
        env:
          VK_CLOUD_API_TOKEN: ${{ secrets.VK_CLOUD_API_TOKEN }}
          VK_CLOUD_VENDOR_ID: ${{ secrets.VK_CLOUD_VENDOR_ID }}
          APP_NAME: my-app
          APP_VERSION: ${{ github.ref_name }}
        run: |
          ./scripts/vk-cloud-deploy.sh deploy
```

### GitLab CI Example

```yaml
deploy-marketplace:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache curl jq bash
    - wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    - chmod +x /usr/local/bin/yq
  script:
    - export APP_VERSION=$CI_COMMIT_TAG
    - ./scripts/vk-cloud-deploy.sh deploy
  only:
    - tags
  variables:
    VK_CLOUD_API_TOKEN: $VK_CLOUD_API_TOKEN
    VK_CLOUD_VENDOR_ID: $VK_CLOUD_VENDOR_ID
    APP_NAME: "my-app"
```

## Best Practices

1. **Version Management**
   - Use semantic versioning
   - Tag releases in git
   - Maintain changelog
   - Test upgrades

2. **Security**
   - Scan images regularly
   - Update dependencies
   - Use minimal base images
   - Follow least privilege principle

3. **Testing**
   - Test locally before submission
   - Verify health checks
   - Test resource limits
   - Validate configuration

4. **Documentation**
   - Document configuration options
   - Provide usage examples
   - Maintain troubleshooting guide
   - Update changelog

5. **Monitoring**
   - Set up alerts
   - Monitor submission status
   - Track deployment metrics
   - Review user feedback

## Related Resources

- **Agent**: `vk-cloud-marketplace-specialist`
- **Skill**: `vk-marketplace-deployment`
- **Skill**: `image-app-configuration`
- **Command**: `/validate-app-config`

## When I Use This Command

I will proactively suggest this command when:
- You mention deploying to VK Cloud marketplace
- You ask about marketplace submission
- You need to publish a container application
- You want to automate deployment workflow
- You're setting up CI/CD for marketplace apps
