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

### Deployment Workflow for Image-Based Applications

```
1. Image Preparation Phase
   └─ Create Packer configuration (.images.yaml and .pkr.hcl)
   └─ Develop Ansible playbooks (provision.yml, start.yml)
   └─ Organize Ansible roles (provision_roles, service_roles, common_roles)
   └─ Build VM image with required software (Cloud-init, Qemu-guest-agent, etc.)
   └─ Test image locally with Packer

2. Service Package Creation Phase
   └─ Create directory structure (service_name/)
   └─ Generate version.yaml (version: 0.0.1)
   └─ Create service.yaml with UUID4 service ID and revision
   └─ Define parameters in parameters/ directory
   └─ Create plan directories in plans/
   └─ Write plan.yaml and display.yaml for each plan
   └─ Prepare service icons (PNG/SVG, max 1MB)
   └─ Write full_description.md with comprehensive documentation

3. Terraform Manifest Development Phase
   └─ Create deployment/deploy.tf in plan directory
   └─ Define required variables (instance_uuid, email, user parameters)
   └─ Configure vkcs provider resources (compute, network, storage)
   └─ Configure ivkcs provider resources (agent, monitoring, scripts)
   └─ Set up ivkcs_agent_exec to run start.yml playbook
   └─ Define outputs for user credentials and access information
   └─ Create deployment/settings.yaml (preset: base_v3, retry: no)

4. Local Testing Phase
   └─ Validate Terraform manifest syntax
   └─ Test with valid resource IDs (flavors, subnets, availability zones)
   └─ Use data sources to verify existing resources
   └─ Test Ansible playbook execution locally
   └─ Verify health check endpoints
   └─ Validate monitoring integration

5. Deployment System Testing Phase
   └─ Upload service package to vendor account
   └─ Deploy in test namespace with test bonuses
   └─ Monitor deployment logs and agent execution
   └─ Verify script results and outputs
   └─ Test health checks and auto-recovery
   └─ Validate complete user workflow

6. Image Publication Phase
   └─ Upload image to VK Cloud platform
   └─ Publish image (makes data publicly accessible)
   └─ Verify image accessibility for deployments
   └─ Test deployment with published image

7. Service Publication Phase
   └─ Publish service to open marketplace namespaces
   └─ Service becomes available to end users
   └─ Monitor initial deployments
   └─ Gather user feedback
   └─ Track usage metrics and billing

8. Maintenance Phase
   └─ Release updates with new revisions
   └─ Update Terraform manifests for new features
   └─ Rebuild images with updated software
   └─ Monitor performance and usage
   └─ Provide customer support
```

### Service Package Structure (Image-Based Applications)

VK Cloud marketplace uses a specific service package structure for image-based applications:

```
service_name/               # Root directory (Latin letters, underscores only)
├── version.yaml            # Generator version (0.0.1)
├── service.yaml            # Service metadata and configuration
├── full_description.md     # Comprehensive service documentation
├── images/                 # Service icons
│   └── logo.svg           # Service icon (PNG/SVG, max 1MB, min 62x62px)
├── parameters/            # Parameter definitions
│   ├── ds-az.yaml        # Availability zone parameter
│   ├── ds-flavor.yaml    # VM flavor parameter
│   ├── ds-subnet.yaml    # Subnet parameter
│   ├── root_type.yaml    # Boot volume type parameter
│   ├── root_size.yaml    # Boot volume size parameter
│   └── custom-param.yaml # Service-specific parameters
└── plans/                 # Plan configurations
    └── basic/             # Plan directory name
        ├── plan.yaml      # Plan metadata and billing
        ├── display.yaml   # Configuration wizard UI
        └── deployment/    # Terraform deployment
            ├── deploy.tf  # Main Terraform manifest
            └── settings.yaml  # Deployment settings
```

**version.yaml Example:**
```yaml
version: 0.0.1
```

**service.yaml Example:**
```yaml
id: 11bd457f-5006-4a5e-9aa3-e07586a487c2  # UUID4
revision: "v1.2.0"
name: OpenVPN
short_description: Свободная реализация технологии VPN
description: " "  # Leave empty, use full_description.md
singleton: false
auto_bind: true
icon: logo.svg
help: https://cloud.vk.com/docs/vendors-products/marketplace/...
bindable: true
plan_updateable: false  # Always false for image-based apps
deactivatable: true
bindings_retrievable: false
instances_retrievable: false
allow_context_updates: false
delete_failed: true

plans:
  - name: basic  # Must match plan directory name

preview:
  parameters: []  # List parameter names for tariff matrix
```

**plan.yaml Example:**
```yaml
id: 8e2a46c5-405b-4487-b95f-6ba282dd1a21  # UUID4 (different from service ID)
revision: "v1.2.0"  # Match service revision
name: basic
description: Базовый
free: true  # true for free plans
short_description: Базовый
full_description: Базовый
billing:
  cost: 0  # Price per billing period (0 for free)
  refundable: false  # Return unused funds
  billing_cycle_flat: "1 mons 0 days"  # or "30 days" (1 mons ≠ 30 days)
```

**Parameter YAML Example (ds-flavor.yaml):**
```yaml
actions:
  - create
schema:
  description: Тип виртуальной машины
  hint: "Тип виртуальной машины, который будет использоваться при создании"
  type: string
  datasource:
    type: flavor
    filter:
      vcpus:
        minimum: 1
      ram:
        minimum: 1024
```

**display.yaml Example:**
```yaml
pages:
  - name: Настройки
    groups:
      - name: Виртуальная машина
        parameters:
          - name: ds-subnet
          - name: ds-az
          - name: ds-flavor
      - name: Системный диск
        parameters:
          - name: root_type
          - name: root_size

entities:
  - entity: vm
    description: Виртуальные машины
    count:
      const: 1
    flavor:
      param: ds-flavor
    disks:
      - type:
          param: root_type
        size:
          param: root_size
```

**deployment/settings.yaml Example:**
```yaml
preset: base_v3
retry: no
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
