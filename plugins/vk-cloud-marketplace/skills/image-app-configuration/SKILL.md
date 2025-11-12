---
name: image-app-configuration
description: Best practices for configuring container images for VK Cloud marketplace deployment. Use when optimizing Docker images, implementing security hardening, or configuring cloud-native applications.
---

# Image-Based Application Configuration

## When to Use This Skill

- Building and optimizing container images for marketplace
- Implementing security best practices for containers
- Configuring cloud-native application patterns
- Troubleshooting container runtime issues
- Implementing efficient image layering and caching
- Setting up multi-architecture image support

## Core Concepts

### Container Image Architecture

A container image is a layered filesystem containing the application code, runtime, dependencies, and configuration. Each layer is immutable and cached for efficiency.

**Image Layers:**
```
┌─────────────────────────────┐
│  Application Code (Layer 5) │
├─────────────────────────────┤
│  Dependencies (Layer 4)      │
├─────────────────────────────┤
│  Runtime (Layer 3)           │
├─────────────────────────────┤
│  System Libraries (Layer 2)  │
├─────────────────────────────┤
│  Base OS (Layer 1)           │
└─────────────────────────────┘
```

**Optimization Principles:**
- Place frequently changing layers at the top
- Combine related operations into single layers
- Use multi-stage builds to exclude build-time dependencies
- Minimize total image size
- Leverage layer caching effectively

### Dockerfile Best Practices

#### Basic Structure

```dockerfile
# 1. Base image selection
FROM node:18-alpine AS base

# 2. Metadata
LABEL maintainer="team@example.com"
LABEL version="1.0.0"
LABEL description="My marketplace application"

# 3. System dependencies
RUN apk add --no-cache \
    ca-certificates \
    tzdata

# 4. Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# 5. Set working directory
WORKDIR /app

# 6. Copy dependency files first (for caching)
COPY package*.json ./

# 7. Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# 8. Copy application code
COPY --chown=nodejs:nodejs . .

# 9. Build application (if needed)
RUN npm run build

# 10. Switch to non-root user
USER nodejs

# 11. Expose ports
EXPOSE 8080

# 12. Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# 13. Define entrypoint and command
ENTRYPOINT ["node"]
CMD ["dist/server.js"]
```

#### Multi-Stage Builds

Multi-stage builds reduce final image size by separating build and runtime environments:

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /build

# Copy and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo \
    -ldflags="-w -s" -o app .

# Stage 2: Runtime
FROM alpine:3.18

# Install CA certificates
RUN apk --no-cache add ca-certificates

# Create non-root user
RUN adduser -D -u 1001 appuser

WORKDIR /app

# Copy only the binary from builder
COPY --from=builder /build/app .

# Switch to non-root user
USER appuser

EXPOSE 8080

CMD ["./app"]
```

### Security Hardening

#### User Management

**Never run as root:**
```dockerfile
# Create user with specific UID
RUN useradd -r -u 1001 -g appuser appuser

# Set ownership
COPY --chown=appuser:appuser . .

# Switch to user
USER appuser
```

#### Read-Only Filesystem

```dockerfile
# Define volume for writable directories
VOLUME ["/tmp", "/app/logs"]

# Kubernetes deployment with read-only root
# (in application manifest)
securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1001
```

#### Secret Management

**Never hardcode secrets:**
```dockerfile
# ❌ BAD - Hardcoded credentials
ENV DB_PASSWORD=secret123

# ✅ GOOD - Use runtime configuration
# Pass via environment variables at runtime
# or mount secrets from secret manager
```

**Kubernetes Secret Integration:**
```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-password

volumeMounts:
  - name: secrets
    mountPath: /etc/secrets
    readOnly: true
```

#### Vulnerability Scanning

Integrate scanning into CI/CD pipeline:

```bash
# Trivy scan
trivy image --severity HIGH,CRITICAL myapp:latest

# Fail build on high severity
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Generate report
trivy image --format json --output report.json myapp:latest
```

### Application Configuration

#### Environment-Based Configuration

```javascript
// config.js - 12-factor app configuration
module.exports = {
  port: process.env.PORT || 8080,
  database: {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    name: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD
  },
  redis: {
    url: process.env.REDIS_URL
  },
  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};
```

#### Configuration Files

```dockerfile
# Copy default configuration
COPY config/default.yaml /app/config/

# Allow override via mounted volume
VOLUME ["/app/config/custom"]

# Application merges default and custom config
```

### Health Checks

#### Readiness vs Liveness

**Readiness Check**: Indicates when the app is ready to receive traffic
**Liveness Check**: Indicates if the app is running properly

```javascript
// Express.js health check endpoints
const express = require('express');
const app = express();

// Readiness: checks dependencies
app.get('/health/ready', async (req, res) => {
  try {
    // Check database connection
    await db.ping();
    // Check Redis connection
    await redis.ping();
    // Check external APIs
    await externalService.check();

    res.status(200).json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

// Liveness: basic app health
app.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'alive' });
});
```

#### Dockerfile Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health/live || exit 1
```

### Resource Optimization

#### Image Size Reduction

**Techniques:**
1. Use minimal base images (Alpine, distroless)
2. Multi-stage builds
3. Clean up package manager caches
4. Remove unnecessary files
5. Use .dockerignore

**.dockerignore Example:**
```
# Version control
.git
.gitignore

# Dependencies
node_modules
vendor

# Build artifacts
dist
build
*.log

# Documentation
README.md
docs/

# Tests
__tests__
*.test.js
coverage/

# IDE
.vscode
.idea
*.swp
```

#### Layer Caching Strategy

```dockerfile
# ✅ GOOD - Dependencies cached separately
COPY package.json package-lock.json ./
RUN npm ci --only=production
COPY . .

# ❌ BAD - Cache invalidated on any change
COPY . .
RUN npm ci --only=production
```

### Multi-Architecture Support

Build for multiple platforms (amd64, arm64):

```bash
# Set up buildx
docker buildx create --name multiarch --use

# Build multi-arch image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:1.0.0 \
  --push \
  .

# View manifest
docker buildx imagetools inspect myapp:1.0.0
```

**Dockerfile for Multi-Arch:**
```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.21-alpine AS builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

WORKDIR /build

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build for target architecture
RUN GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o app .

FROM alpine:3.18
COPY --from=builder /build/app /app
CMD ["/app"]
```

## Advanced Patterns

### Init Containers

Use init containers for setup tasks:

```yaml
initContainers:
  - name: wait-for-db
    image: busybox:1.36
    command:
      - sh
      - -c
      - |
        until nc -z postgres 5432; do
          echo "Waiting for database..."
          sleep 2
        done

  - name: run-migrations
    image: myapp:1.0.0
    command: ["npm", "run", "migrate"]
    env:
      - name: DB_URL
        valueFrom:
          secretKeyRef:
            name: app-secrets
            key: database-url
```

### Sidecar Patterns

**Logging Sidecar:**
```yaml
containers:
  - name: app
    image: myapp:1.0.0
    volumeMounts:
      - name: logs
        mountPath: /var/log/app

  - name: log-shipper
    image: fluent/fluent-bit:2.0
    volumeMounts:
      - name: logs
        mountPath: /var/log/app
      - name: fluent-config
        mountPath: /fluent-bit/etc/
```

### Signal Handling

Graceful shutdown on SIGTERM:

```javascript
// Node.js graceful shutdown
const server = app.listen(8080);

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');

  server.close(() => {
    console.log('HTTP server closed');

    // Close database connections
    db.close();

    // Close other resources
    redis.quit();

    process.exit(0);
  });

  // Force shutdown after 30s
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30000);
});
```

## Monitoring and Observability

### Structured Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

// Usage
logger.info('User logged in', {
  userId: user.id,
  ip: req.ip,
  userAgent: req.headers['user-agent']
});
```

### Metrics Export

```javascript
const prometheus = require('prom-client');

// Create metrics
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code']
});

// Collect default metrics
prometheus.collectDefaultMetrics();

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(await prometheus.register.metrics());
});
```

### Distributed Tracing

```javascript
const opentelemetry = require('@opentelemetry/api');
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');

// Configure tracing
const provider = new NodeTracerProvider();
provider.addSpanProcessor(
  new SimpleSpanProcessor(new JaegerExporter())
);
provider.register();

const tracer = opentelemetry.trace.getTracer('my-app');

// Create spans
const span = tracer.startSpan('process-order');
try {
  // Process order
  span.setAttribute('order.id', orderId);
  span.setAttribute('order.amount', amount);
} finally {
  span.end();
}
```

## Testing

### Container Testing

```bash
# Test with different configurations
docker run -e LOG_LEVEL=debug myapp:1.0.0

# Test resource limits
docker run --memory=512m --cpus=0.5 myapp:1.0.0

# Test networking
docker run -p 8080:8080 myapp:1.0.0

# Test volumes
docker run -v $(pwd)/data:/app/data myapp:1.0.0

# Test with specific user
docker run --user 1001:1001 myapp:1.0.0
```

### Automated Testing

```bash
#!/bin/bash
# test-container.sh

# Build image
docker build -t myapp:test .

# Run container
CONTAINER_ID=$(docker run -d -p 8080:8080 myapp:test)

# Wait for startup
sleep 5

# Test health endpoint
if curl -f http://localhost:8080/health/live; then
  echo "✓ Health check passed"
else
  echo "✗ Health check failed"
  exit 1
fi

# Test application endpoint
if curl -f http://localhost:8080/api/status; then
  echo "✓ API check passed"
else
  echo "✗ API check failed"
  exit 1
fi

# Cleanup
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID

echo "All tests passed!"
```

## References

See `references/` directory for:
- Complete Dockerfile examples
- Security scanning configurations
- Health check implementations
- Configuration management patterns
- Testing scripts

See `assets/` directory for:
- Container architecture diagrams
- Security checklist
- Optimization guide
- Troubleshooting flowcharts
