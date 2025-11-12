# VK Cloud Marketplace Plugin

Expert plugin for deploying and managing image-based applications in VK Cloud marketplace with Claude Agent SDK integration.

## Overview

This plugin provides comprehensive automation and expert guidance for deploying containerized applications to VK Cloud marketplace. It handles the complete deployment lifecycle from Docker image optimization to marketplace submission and approval monitoring.

## Components

### Agent

**vk-cloud-marketplace-specialist** - Expert agent specializing in:
- Image-based application deployment and configuration
- VK Cloud marketplace submission and management
- Vendor account operations
- Container image optimization and security scanning
- Manifest validation and compliance checking
- Deployment automation and troubleshooting

### Skills

**vk-marketplace-deployment** - Comprehensive guide covering:
- Marketplace deployment workflow
- Application manifest structure
- Container image requirements
- Security and compliance
- API integration
- Troubleshooting common issues

**image-app-configuration** - Best practices for:
- Docker image optimization
- Multi-stage builds
- Security hardening
- Health checks
- Resource management
- Monitoring and observability

### Commands

**deploy-marketplace-app** - Automated deployment workflow:
- Build and optimize Docker images
- Run security vulnerability scans
- Validate application manifests
- Test deployments locally
- Push to VK Cloud registry
- Submit to marketplace
- Monitor approval status

**validate-app-config** - Configuration validation:
- Manifest syntax and structure validation
- Docker configuration checks
- Security requirements verification
- Resource specification validation
- Health check configuration
- Documentation completeness

## Installation

```bash
# Install the plugin
claude plugin install vk-cloud-marketplace
```

## Usage

### Deploy Application

```
/deploy-marketplace-app
```

The agent will guide you through:
1. Gathering application information
2. Validating configuration
3. Building and testing Docker image
4. Running security scans
5. Submitting to marketplace
6. Monitoring approval status

### Validate Configuration

```
/validate-app-config
```

Validates:
- Application manifest
- Docker configuration
- Security compliance
- Resource specifications
- Health checks
- Documentation

### Get Expert Guidance

Simply mention VK Cloud marketplace deployment in your conversation and the agent will proactively assist with:
- Architecture design
- Image optimization
- Security best practices
- Deployment strategies
- Troubleshooting issues

## Prerequisites

- Docker installed and running
- VK Cloud vendor account with API credentials
- Application manifest file (`application.yaml`)
- Dockerfile for your application

## Configuration

Set environment variables:

```bash
export VK_CLOUD_API_TOKEN="your-api-token"
export VK_CLOUD_VENDOR_ID="your-vendor-id"
export APP_NAME="your-application-name"
export APP_VERSION="1.0.0"
```

## Features

### Docker Image Optimization
- Multi-stage build patterns
- Minimal base images
- Layer caching strategies
- Size optimization techniques
- Multi-architecture support

### Security
- Vulnerability scanning with Trivy
- Non-root user enforcement
- Secret management
- Read-only filesystem configuration
- Security policy compliance

### Automation
- Complete CI/CD integration
- Automated testing
- Manifest validation
- Deployment monitoring
- Status tracking

### Compliance
- VK Cloud marketplace requirements
- Resource limit validation
- Health check verification
- Documentation standards
- Best practices enforcement

## Examples

### Basic Deployment

```bash
# Set credentials
export VK_CLOUD_API_TOKEN="token"
export VK_CLOUD_VENDOR_ID="vendor-id"

# Deploy using command
/deploy-marketplace-app
```

### CI/CD Integration

See skill references for:
- GitHub Actions workflows
- GitLab CI pipelines
- Automated testing scripts
- Deployment automation

## Skill References

Both skills include comprehensive reference materials:

**vk-marketplace-deployment/references/**
- `sample-manifest.yaml` - Complete application manifest example
- `deployment-script.sh` - Automated deployment script

**image-app-configuration/references/**
- `optimized-dockerfile.example` - Node.js multi-stage Dockerfile
- `golang-dockerfile.example` - Go application Dockerfile
- `python-dockerfile.example` - Python application Dockerfile

## Support

For VK Cloud marketplace documentation:
- https://cloud.vk.com/docs/tools-for-using-services/vendor-account/manage-apps

For plugin issues:
- https://github.com/lazarenkod/agents/issues

## License

MIT

## Version

1.0.0
