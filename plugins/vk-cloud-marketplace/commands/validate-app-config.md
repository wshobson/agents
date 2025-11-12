---
name: validate-app-config
description: Validates VK Cloud marketplace application configuration, manifest, and Docker image setup. Ensures compliance with marketplace requirements before deployment.
---

# Validate App Config

Comprehensive validation tool for VK Cloud marketplace applications. Checks manifest syntax, Docker configuration, security requirements, and marketplace compliance before submission.

## Purpose

This command performs thorough validation of:
- Application manifest (YAML/JSON)
- Docker image configuration
- Security and compliance requirements
- Resource specifications
- Health check configuration
- Documentation completeness

## What Gets Validated

### 1. Manifest Structure

**Syntax Validation**
- Valid YAML/JSON syntax
- Correct API version
- Proper indentation and structure
- No duplicate keys

**Required Fields**
- `metadata.name`: Application identifier
- `metadata.displayName`: Human-readable name
- `metadata.version`: Semantic version
- `metadata.description`: Detailed description (min 50 chars)
- `metadata.category`: Valid category
- `spec.image`: Container image configuration
- `spec.resources`: Resource requirements
- `spec.healthCheck`: Health check configuration

**Optional But Recommended**
- `metadata.icon`: Application icon URL
- `metadata.keywords`: Search keywords
- `spec.networking`: Network configuration
- `spec.persistence`: Storage configuration
- `spec.scaling`: Autoscaling settings
- `pricing`: Pricing model
- `support`: Support information

### 2. Image Configuration

**Dockerfile Validation**
- Multi-stage build usage
- Non-root user configuration
- Health check definition
- Proper EXPOSE directives
- Optimized layer structure

**Image Properties**
- Valid base image
- Appropriate size (< 2GB recommended)
- Tagged appropriately
- No hardcoded secrets
- Security best practices

### 3. Security Requirements

**Container Security**
- Runs as non-root user (UID > 0)
- No privileged mode
- Read-only root filesystem (recommended)
- Dropped capabilities
- No sensitive data in environment

**Image Security**
- No critical CVEs
- Updated base image
- Minimal attack surface
- Security scanning passed
- Signed images (recommended)

### 4. Resource Specifications

**CPU Requirements**
- Request: 100m - 32000m
- Limit: >= Request
- Reasonable for workload

**Memory Requirements**
- Request: 128Mi - 128Gi
- Limit: >= Request
- Sufficient for application

**Storage Requirements**
- Size: 1Gi - 1000Gi
- Storage class specified
- Backup configuration

### 5. Health Checks

**Readiness Probe**
- Endpoint or command defined
- Appropriate timing values
- Tests dependencies
- Returns correct status codes

**Liveness Probe**
- Endpoint or command defined
- Prevents restart loops
- Longer timeout than readiness
- Tests core functionality

### 6. Documentation

**Required Documentation**
- Clear description
- Installation instructions
- Configuration guide
- Troubleshooting section
- Support contact

**Recommended Documentation**
- Architecture overview
- API documentation
- Migration guides
- FAQ section
- Changelog

## Usage

### Interactive Mode

When you invoke this command, I will:

1. **Locate Configuration Files**
   - Find application manifest
   - Locate Dockerfile
   - Check for additional configs

2. **Run Validation Checks**
   - Validate manifest syntax and structure
   - Check Docker configuration
   - Verify security requirements
   - Validate resource specifications
   - Check health check configuration

3. **Generate Report**
   - List all issues found
   - Categorize by severity (error/warning/info)
   - Provide fix suggestions
   - Show compliance score

4. **Provide Recommendations**
   - Suggest optimizations
   - Highlight best practices
   - Recommend improvements

### Command Line Mode

```bash
# Validate current directory
validate-config

# Validate specific manifest
validate-config --manifest=path/to/application.yaml

# Validate with specific Dockerfile
validate-config --dockerfile=path/to/Dockerfile

# Output JSON report
validate-config --format=json

# Strict mode (fail on warnings)
validate-config --strict

# Check specific aspects only
validate-config --check=manifest,security
```

## Validation Report Example

```
VK Cloud Marketplace Configuration Validation Report
====================================================

Application: my-awesome-app
Version: 1.0.0
Timestamp: 2024-01-15 10:30:45

MANIFEST VALIDATION
-------------------
✓ Syntax: Valid YAML
✓ API Version: marketplace.vk.com/v1
✓ Required Fields: All present
✓ Naming Convention: Compliant
⚠ Description: 45 characters (minimum 50 recommended)
✓ Category: Valid (databases)

DOCKER CONFIGURATION
--------------------
✓ Dockerfile: Found
✓ Multi-stage Build: Yes
✓ Base Image: node:18-alpine (valid)
⚠ Image Size: 850MB (recommended < 500MB)
✓ Non-root User: Configured (UID 1001)
✓ Health Check: Defined

SECURITY VALIDATION
-------------------
✓ Runs as Non-root: Yes
✓ Read-only Filesystem: Configured
✓ No Privileged Mode: Confirmed
✓ Capabilities Dropped: Yes
✗ Vulnerability Scan: Not performed yet
⚠ Secrets in ENV: Review recommended

RESOURCE SPECIFICATIONS
-----------------------
✓ CPU Request: 500m (valid)
✓ CPU Limit: 2000m (valid)
✓ Memory Request: 512Mi (valid)
✓ Memory Limit: 2Gi (valid)
✓ Storage Request: 10Gi (valid)
ℹ Autoscaling: Not configured

HEALTH CHECKS
-------------
✓ Readiness Probe: HTTP GET /health/ready
✓ Liveness Probe: HTTP GET /health/live
✓ Initial Delay: 10s (appropriate)
✓ Timeout: 3s (appropriate)
⚠ Failure Threshold: 3 (consider 5 for liveness)

DOCUMENTATION
-------------
✓ Description: Present
✓ Support Email: Provided
✓ Documentation URL: Provided
⚠ Changelog: Not found
ℹ FAQ: Not provided

SUMMARY
-------
Errors: 1
Warnings: 4
Info: 2

Compliance Score: 85/100 (Good)

NEXT STEPS
----------
1. Run vulnerability scan on Docker image
2. Increase description length to 50+ characters
3. Consider reducing image size with optimization
4. Add changelog file
5. Review environment variables for secrets

Overall: READY FOR DEPLOYMENT (after addressing errors)
```

## Validation Rules

### Critical (Must Fix)

These issues prevent marketplace submission:

1. **Invalid Manifest Syntax**
   - Malformed YAML/JSON
   - Missing required fields
   - Invalid field values

2. **Security Violations**
   - Running as root user
   - Privileged containers
   - Critical vulnerabilities

3. **Invalid Resource Specs**
   - Resources outside allowed ranges
   - Invalid storage classes
   - Missing health checks

### Warnings (Should Fix)

These issues should be addressed before submission:

1. **Suboptimal Configuration**
   - Large image size
   - Missing documentation
   - No autoscaling configuration

2. **Security Concerns**
   - Outdated base images
   - Missing security context
   - Potential secret exposure

3. **Performance Issues**
   - Inefficient resource allocation
   - Missing readiness probe
   - Poor health check timing

### Informational (Consider)

These are recommendations for improvement:

1. **Optimizations**
   - Layer caching opportunities
   - Resource right-sizing
   - Additional monitoring

2. **Best Practices**
   - Enhanced documentation
   - Backup configuration
   - Multi-architecture support

## Common Issues and Fixes

### Issue: Missing Required Fields

```yaml
# ❌ Invalid - missing required fields
metadata:
  name: my-app

# ✅ Valid - all required fields present
metadata:
  name: my-app
  displayName: My Application
  version: "1.0.0"
  description: Comprehensive description of the application...
  category: web-apps
```

### Issue: Invalid Resource Values

```yaml
# ❌ Invalid - values outside allowed range
resources:
  requests:
    cpu: "50m"      # Too low (min 100m)
    memory: "64Mi"  # Too low (min 128Mi)

# ✅ Valid - within allowed ranges
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "2000m"
    memory: "2Gi"
```

### Issue: Missing Health Checks

```yaml
# ❌ Invalid - no health checks
spec:
  image:
    repository: myapp
    tag: "1.0.0"

# ✅ Valid - health checks configured
spec:
  image:
    repository: myapp
    tag: "1.0.0"
  healthCheck:
    readiness:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
    liveness:
      httpGet:
        path: /health/live
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
```

### Issue: Security Misconfiguration

```dockerfile
# ❌ Invalid - running as root
FROM node:18-alpine
WORKDIR /app
COPY . .
CMD ["node", "server.js"]

# ✅ Valid - non-root user
FROM node:18-alpine
RUN adduser -D -u 1001 nodejs
WORKDIR /app
COPY --chown=nodejs:nodejs . .
USER nodejs
CMD ["node", "server.js"]
```

### Issue: Invalid Naming

```yaml
# ❌ Invalid - uppercase and underscores
metadata:
  name: My_Application

# ✅ Valid - lowercase with hyphens
metadata:
  name: my-application
```

## Automated Validation

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating VK Cloud marketplace configuration..."

# Run validation
if ! validate-config --strict; then
    echo "Validation failed. Fix issues before committing."
    exit 1
fi

echo "Validation passed!"
```

### CI/CD Integration

```yaml
# GitHub Actions
name: Validate Configuration

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate marketplace config
        run: |
          # Install validation tools
          npm install -g yaml-validator

          # Validate manifest
          yaml-validator application.yaml

          # Validate Dockerfile
          docker run --rm -i hadolint/hadolint < Dockerfile

          # Run custom validation
          ./scripts/validate-config.sh
```

## Validation Checklist

Use this checklist to ensure comprehensive validation:

### Manifest Validation
- [ ] Valid YAML syntax
- [ ] API version specified
- [ ] All required fields present
- [ ] Version follows semantic versioning
- [ ] Description is comprehensive (50+ chars)
- [ ] Category is valid
- [ ] Image configuration complete
- [ ] Resources within limits
- [ ] Health checks configured

### Docker Validation
- [ ] Dockerfile exists
- [ ] Multi-stage build used
- [ ] Non-root user configured
- [ ] Image size optimized
- [ ] Health check defined
- [ ] Proper EXPOSE directives
- [ ] No hardcoded secrets
- [ ] .dockerignore present

### Security Validation
- [ ] Runs as non-root
- [ ] No privileged mode
- [ ] Capabilities dropped
- [ ] Read-only filesystem configured
- [ ] No critical vulnerabilities
- [ ] Secrets managed properly
- [ ] Base image up to date

### Documentation Validation
- [ ] Description present
- [ ] Support contact provided
- [ ] Documentation URL provided
- [ ] Installation guide available
- [ ] Troubleshooting guide available
- [ ] Changelog maintained

## Advanced Validation

### Schema Validation

```bash
# Validate against JSON schema
yq eval -o=json application.yaml | \
  jsonschema -i /dev/stdin vk-cloud-marketplace-schema.json
```

### Policy Validation

```bash
# Validate with Open Policy Agent
opa eval --data policies/ --input application.yaml "data.marketplace.allow"
```

### Custom Validation Scripts

```bash
#!/bin/bash
# custom-validation.sh

# Check image exists in registry
IMAGE=$(yq eval '.spec.image.repository' application.yaml)
TAG=$(yq eval '.spec.image.tag' application.yaml)

if ! docker manifest inspect "$IMAGE:$TAG" > /dev/null 2>&1; then
    echo "Error: Image $IMAGE:$TAG not found in registry"
    exit 1
fi

# Verify health check endpoint
PORT=$(yq eval '.spec.networking.ports[0].port' application.yaml)
HEALTH_PATH=$(yq eval '.spec.healthCheck.liveness.httpGet.path' application.yaml)

docker run -d --name test-container -p "$PORT:$PORT" "$IMAGE:$TAG"
sleep 10

if ! curl -f "http://localhost:$PORT$HEALTH_PATH"; then
    echo "Error: Health check endpoint not responding"
    docker stop test-container
    exit 1
fi

docker stop test-container
echo "Validation passed!"
```

## Related Resources

- **Agent**: `vk-cloud-marketplace-specialist`
- **Skill**: `vk-marketplace-deployment`
- **Skill**: `image-app-configuration`
- **Command**: `/deploy-marketplace-app`

## When I Use This Command

I will proactively suggest this command when:
- You're preparing to deploy to marketplace
- You modify application manifest
- You update Dockerfile
- You want to check compliance
- Before running deployment
- During troubleshooting configuration issues
