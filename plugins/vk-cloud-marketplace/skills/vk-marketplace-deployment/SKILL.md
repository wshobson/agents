---
name: vk-marketplace-deployment
description: Comprehensive guide for deploying image-based applications to VK Cloud marketplace. Use when deploying apps, managing submissions, or troubleshooting marketplace deployments.
---

# VK Cloud Marketplace Deployment

## When to Use This Skill

- Deploying new image-based applications to VK Cloud marketplace
- Updating existing marketplace applications
- Managing vendor account and application lifecycle
- Troubleshooting deployment issues
- Understanding VK Cloud marketplace requirements and workflows
- Configuring application metadata and resources

## Core Concepts

### Marketplace Architecture

VK Cloud marketplace supports image-based applications deployed as containerized workloads. Applications are submitted through vendor accounts and go through validation before being published.

**Key Components:**
- **Vendor Account**: Organization-level account for managing marketplace listings
- **Application Manifest**: Configuration file defining app metadata, resources, and deployment
- **Container Image**: Docker image containing the application
- **Marketplace API**: RESTful API for programmatic management
- **Application Catalog**: Public listing of available marketplace apps

### Deployment Workflow

```
1. Preparation Phase
   └─ Prepare container image
   └─ Create application manifest
   └─ Gather required documentation

2. Validation Phase
   └─ Validate image security
   └─ Test deployment locally
   └─ Verify resource requirements

3. Submission Phase
   └─ Submit via marketplace portal or API
   └─ Provide metadata and documentation
   └─ Set pricing and billing

4. Review Phase
   └─ VK Cloud team reviews submission
   └─ Address any feedback
   └─ Make required changes

5. Publication Phase
   └─ Application approved and published
   └─ Monitor initial deployments
   └─ Gather user feedback

6. Maintenance Phase
   └─ Release updates and patches
   └─ Monitor performance and usage
   └─ Provide customer support
```

### Application Manifest Structure

The application manifest defines all aspects of the marketplace app:

```yaml
apiVersion: marketplace.vk.com/v1
kind: Application
metadata:
  name: my-application
  displayName: My Application
  version: "1.0.0"
  description: |
    Comprehensive description of the application,
    its features, and use cases.
  category: databases|web-apps|monitoring|security|other
  icon: https://example.com/icon.png

spec:
  # Container image configuration
  image:
    repository: registry.example.com/my-app
    tag: "1.0.0"
    pullPolicy: IfNotPresent
    pullSecrets:
      - name: registry-credentials

  # Resource requirements
  resources:
    requests:
      cpu: "500m"
      memory: "512Mi"
      storage: "10Gi"
    limits:
      cpu: "2000m"
      memory: "2Gi"

  # Networking configuration
  networking:
    ports:
      - name: http
        port: 8080
        protocol: TCP
      - name: https
        port: 8443
        protocol: TCP
    ingress:
      enabled: true
      hostname: "{instance-id}.apps.vkcloud.com"

  # Environment configuration
  environment:
    - name: APP_MODE
      value: "production"
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: database-url

  # Persistent storage
  persistence:
    enabled: true
    size: "10Gi"
    storageClass: "standard"
    mountPath: "/data"

  # Health checks
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

  # Scaling configuration
  scaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 10
    targetCPUUtilization: 70

# Pricing configuration
pricing:
  model: subscription|usage-based|free
  tiers:
    - name: Basic
      price: 500
      currency: RUB
      period: month
    - name: Professional
      price: 2000
      currency: RUB
      period: month

# Support and documentation
support:
  email: support@example.com
  documentation: https://docs.example.com
  website: https://example.com
```

## Container Image Requirements

### Image Optimization

**Base Image Selection:**
- Use official, minimal base images
- Prefer Alpine Linux or distroless images
- Avoid images with known vulnerabilities

**Multi-Stage Builds:**
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 8080
CMD ["node", "dist/server.js"]
```

### Security Requirements

**Required Security Practices:**
1. Run as non-root user
2. No hardcoded secrets or credentials
3. Scan for vulnerabilities (CVE score < 7.0)
4. Use read-only filesystem where possible
5. Minimize attack surface (remove unnecessary tools)

**Image Scanning:**
```bash
# Scan with Trivy
trivy image --severity HIGH,CRITICAL myapp:1.0.0

# Scan with Grype
grype myapp:1.0.0 --fail-on high
```

### Image Tagging Strategy

**Recommended Tagging:**
- Semantic versioning: `1.0.0`, `1.0.1`, `2.0.0`
- Major version: `1`, `2`
- Latest: `latest` (points to current stable)
- SHA-based: `sha-abc123` (for immutability)

## API Integration

### Authentication

VK Cloud marketplace API uses token-based authentication:

```bash
# Set API credentials
export VK_CLOUD_API_TOKEN="your-api-token"
export VK_CLOUD_VENDOR_ID="your-vendor-id"

# Test authentication
curl -H "Authorization: Bearer $VK_CLOUD_API_TOKEN" \
     https://api.cloud.vk.com/marketplace/v1/vendor/info
```

### Application Submission via API

```bash
# Submit new application
curl -X POST \
  -H "Authorization: Bearer $VK_CLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @application-manifest.json \
  https://api.cloud.vk.com/marketplace/v1/applications

# Get submission status
curl -H "Authorization: Bearer $VK_CLOUD_API_TOKEN" \
     https://api.cloud.vk.com/marketplace/v1/applications/{app-id}/status

# Update existing application
curl -X PUT \
  -H "Authorization: Bearer $VK_CLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @application-manifest.json \
  https://api.cloud.vk.com/marketplace/v1/applications/{app-id}
```

## Deployment Validation

### Pre-Submission Checklist

Before submitting to marketplace:

- [ ] Container image built and pushed to registry
- [ ] Image scanned for vulnerabilities (passing)
- [ ] Application manifest validated
- [ ] Local deployment tested successfully
- [ ] Health checks configured and working
- [ ] Resource limits appropriate
- [ ] Documentation complete
- [ ] Support contact information provided
- [ ] Pricing configured (if applicable)
- [ ] Legal and compliance requirements met

### Testing Deployment

**Local Testing with Docker:**
```bash
# Run container locally
docker run -d \
  -p 8080:8080 \
  -e APP_MODE=production \
  --name test-app \
  myapp:1.0.0

# Test health checks
curl http://localhost:8080/health/ready
curl http://localhost:8080/health/live

# Check logs
docker logs test-app

# Stop and remove
docker stop test-app && docker rm test-app
```

**Kubernetes Testing:**
```bash
# Create test namespace
kubectl create namespace marketplace-test

# Deploy application
kubectl apply -f application-manifest.yaml -n marketplace-test

# Check deployment status
kubectl get pods -n marketplace-test
kubectl describe deployment my-app -n marketplace-test

# Test service
kubectl port-forward svc/my-app 8080:8080 -n marketplace-test
curl http://localhost:8080

# Clean up
kubectl delete namespace marketplace-test
```

## Troubleshooting

### Common Issues

**Issue: Image Pull Failed**
```
Error: ImagePullBackOff
Solution:
1. Verify image exists in registry
2. Check pull credentials are configured
3. Ensure registry is accessible from VK Cloud
4. Validate image tag is correct
```

**Issue: Pod Crashes After Start**
```
Error: CrashLoopBackOff
Solution:
1. Check application logs: kubectl logs <pod-name>
2. Verify environment variables are set correctly
3. Check resource limits are sufficient
4. Validate health check endpoints
5. Review startup command and arguments
```

**Issue: Submission Validation Failed**
```
Error: Manifest validation failed
Solution:
1. Validate manifest syntax (YAML/JSON)
2. Check all required fields are present
3. Verify resource values are within limits
4. Ensure API version is supported
5. Review error message details
```

## Best Practices

### Version Management

- Use semantic versioning for all releases
- Maintain changelog for version updates
- Support backward compatibility when possible
- Provide migration guides for breaking changes
- Test upgrades from previous versions

### Documentation

**Required Documentation:**
1. Getting Started Guide
2. Configuration Reference
3. API Documentation (if applicable)
4. Troubleshooting Guide
5. FAQ
6. Support Contact Information

### Monitoring and Observability

**Implement Comprehensive Monitoring:**
- Application metrics (requests, errors, latency)
- Resource utilization (CPU, memory, disk)
- Health check status
- Custom business metrics
- Distributed tracing

**Logging Best Practices:**
- Structured logging (JSON format)
- Appropriate log levels (ERROR, WARN, INFO, DEBUG)
- Include request IDs for tracing
- Avoid logging sensitive data
- Configure log retention policies

## References

See `references/` directory for:
- Sample application manifests
- Dockerfile templates
- CI/CD pipeline examples
- Testing scripts
- API integration examples

See `assets/` directory for:
- Deployment workflow diagrams
- Architecture patterns
- Troubleshooting flowcharts
