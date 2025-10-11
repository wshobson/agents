# Kubernetes Manifest Generation

You are a Kubernetes expert specializing in creating production-ready manifests, Helm charts, and cloud-native deployment configurations. Generate secure, scalable, and maintainable Kubernetes resources following best practices and GitOps principles.

## Context
The user needs to create or optimize Kubernetes manifests for deploying applications. Focus on production readiness, security hardening, resource optimization, observability, and multi-environment configurations.

## Requirements
$ARGUMENTS

## Instructions

### 1. Application Analysis

Analyze the application to determine Kubernetes requirements:

**Framework-Specific Analysis**
```python
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any

class AdvancedK8sAnalyzer:
    def __init__(self):
        self.framework_patterns = {
            'react': {
                'files': ['package.json', 'src/App.js', 'src/index.js'],
                'build_tool': ['vite', 'webpack', 'create-react-app'],
                'deployment_type': 'static',
                'port': 3000,
                'health_check': '/health',
                'resources': {'cpu': '100m', 'memory': '256Mi'}
            },
            'nextjs': {
                'files': ['next.config.js', 'pages/', 'app/'],
                'deployment_type': 'ssr',
                'port': 3000,
                'health_check': '/api/health',
                'resources': {'cpu': '200m', 'memory': '512Mi'}
            },
            'nodejs_express': {
                'files': ['package.json', 'server.js', 'app.js'],
                'deployment_type': 'api',
                'port': 8080,
                'health_check': '/health',
                'resources': {'cpu': '200m', 'memory': '512Mi'}
            },
            'python_fastapi': {
                'files': ['main.py', 'requirements.txt', 'pyproject.toml'],
                'deployment_type': 'api',
                'port': 8000,
                'health_check': '/health',
                'resources': {'cpu': '250m', 'memory': '512Mi'}
            },
            'python_django': {
                'files': ['manage.py', 'settings.py', 'wsgi.py'],
                'deployment_type': 'web',
                'port': 8000,
                'health_check': '/health/',
                'resources': {'cpu': '300m', 'memory': '1Gi'}
            },
            'go': {
                'files': ['main.go', 'go.mod', 'go.sum'],
                'deployment_type': 'api',
                'port': 8080,
                'health_check': '/health',
                'resources': {'cpu': '100m', 'memory': '128Mi'}
            },
            'java_spring': {
                'files': ['pom.xml', 'build.gradle', 'src/main/java'],
                'deployment_type': 'api',
                'port': 8080,
                'health_check': '/actuator/health',
                'resources': {'cpu': '500m', 'memory': '1Gi'}
            },
            'dotnet': {
                'files': ['*.csproj', 'Program.cs', 'Startup.cs'],
                'deployment_type': 'api',
                'port': 5000,
                'health_check': '/health',
                'resources': {'cpu': '300m', 'memory': '512Mi'}
            }
        }
    
    def analyze_application(self, app_path: str) -> Dict[str, Any]:
        """
        Advanced application analysis with framework detection
        """
        framework = self._detect_framework(app_path)
        analysis = {
            'framework': framework,
            'app_type': self._detect_app_type(app_path),
            'services': self._identify_services(app_path),
            'dependencies': self._find_dependencies(app_path),
            'storage_needs': self._analyze_storage(app_path),
            'networking': self._analyze_networking(app_path),
            'resource_requirements': self._estimate_resources(app_path, framework),
            'security_requirements': self._analyze_security_needs(app_path),
            'observability_needs': self._analyze_observability(app_path),
            'scaling_strategy': self._recommend_scaling(app_path, framework)
        }
        
        return analysis
    
    def _detect_framework(self, app_path: str) -> str:
        """Detect application framework for optimized deployments"""
        app_path = Path(app_path)
        
        for framework, config in self.framework_patterns.items():
            if all((app_path / f).exists() for f in config['files'][:1]):
                if any((app_path / f).exists() for f in config['files']):
                    return framework
        
        return 'generic'
    
    def generate_framework_optimized_manifests(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate manifests optimized for specific frameworks"""
        framework = analysis['framework']
        if framework in self.framework_patterns:
            return self._generate_specialized_manifests(framework, analysis)
        return self._generate_generic_manifests(analysis)
    
    def _detect_app_type(self, app_path):
        """Detect application type and stack"""
        indicators = {
            'web': ['nginx.conf', 'httpd.conf', 'index.html'],
            'api': ['app.py', 'server.js', 'main.go'],
            'database': ['postgresql.conf', 'my.cnf', 'mongod.conf'],
            'worker': ['worker.py', 'consumer.js', 'processor.go'],
            'frontend': ['package.json', 'webpack.config.js', 'angular.json']
        }
        
        detected_types = []
        for app_type, files in indicators.items():
            if any((Path(app_path) / f).exists() for f in files):
                detected_types.append(app_type)
                
        return detected_types
    
    def _identify_services(self, app_path):
        """Identify microservices structure"""
        services = []
        
        # Check docker-compose.yml
        compose_file = Path(app_path) / 'docker-compose.yml'
        if compose_file.exists():
            with open(compose_file) as f:
                compose = yaml.safe_load(f)
                for service_name, config in compose.get('services', {}).items():
                    services.append({
                        'name': service_name,
                        'image': config.get('image', 'custom'),
                        'ports': config.get('ports', []),
                        'environment': config.get('environment', {}),
                        'volumes': config.get('volumes', [])
                    })
        
        return services
```

### 2. Deployment Manifest Generation

Create production-ready Deployment manifests:

**Deployment Template**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    version: ${VERSION}
    component: ${COMPONENT}
    managed-by: kubectl
spec:
  replicas: ${REPLICAS}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ${APP_NAME}
      component: ${COMPONENT}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        version: ${VERSION}
        component: ${COMPONENT}
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "${METRICS_PORT}"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: ${APP_NAME}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: ${PORT}
          protocol: TCP
        - name: metrics
          containerPort: ${METRICS_PORT}
          protocol: TCP
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        envFrom:
        - configMapRef:
            name: ${APP_NAME}-config
        - secretRef:
            name: ${APP_NAME}-secrets
        resources:
          requests:
            memory: "${MEMORY_REQUEST}"
            cpu: "${CPU_REQUEST}"
          limits:
            memory: "${MEMORY_LIMIT}"
            cpu: "${CPU_LIMIT}"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - ${APP_NAME}
              topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: ${APP_NAME}
```

### 3. Service and Networking

Generate Service and networking resources:

**Service Configuration**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    component: ${COMPONENT}
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: ClusterIP
  selector:
    app: ${APP_NAME}
    component: ${COMPONENT}
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: grpc
    protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}-headless
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: ${APP_NAME}
  ports:
  - name: http
    port: 80
    targetPort: http
```

**Ingress Configuration**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - ${DOMAIN}
    secretName: ${APP_NAME}-tls
  rules:
  - host: ${DOMAIN}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ${APP_NAME}
            port:
              name: http
```

### 4. Configuration Management

Create ConfigMaps and Secrets:

**ConfigMap Generator**
```python
def generate_configmap(app_name, config_data):
    """
    Generate ConfigMap manifest
    """
    configmap = {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {
            'name': f'{app_name}-config',
            'namespace': 'default',
            'labels': {
                'app': app_name
            }
        },
        'data': {}
    }
    
    # Handle different config formats
    for key, value in config_data.items():
        if isinstance(value, dict):
            # Nested config as YAML
            configmap['data'][key] = yaml.dump(value)
        elif isinstance(value, list):
            # List as JSON
            configmap['data'][key] = json.dumps(value)
        else:
            # Plain string
            configmap['data'][key] = str(value)
    
    return yaml.dump(configmap)

def generate_secret(app_name, secret_data):
    """
    Generate Secret manifest
    """
    import base64
    
    secret = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': f'{app_name}-secrets',
            'namespace': 'default',
            'labels': {
                'app': app_name
            }
        },
        'type': 'Opaque',
        'data': {}
    }
    
    # Base64 encode all values
    for key, value in secret_data.items():
        encoded = base64.b64encode(value.encode()).decode()
        secret['data'][key] = encoded
    
    return yaml.dump(secret)
```

### 5. Persistent Storage

Configure persistent volumes:

**StatefulSet with Storage**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  serviceName: ${APP_NAME}-headless
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        ports:
        - containerPort: ${PORT}
          name: http
        volumeMounts:
        - name: data
          mountPath: /data
        - name: config
          mountPath: /etc/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: ${APP_NAME}-config
  volumeClaimTemplates:
  - metadata:
      name: data
      labels:
        app: ${APP_NAME}
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: ${STORAGE_CLASS}
      resources:
        requests:
          storage: ${STORAGE_SIZE}
```

### 6. Helm Chart Generation

Create production Helm charts:

**Chart Structure**
```bash
#!/bin/bash
# generate-helm-chart.sh

create_helm_chart() {
    local chart_name="$1"
    
    mkdir -p "$chart_name"/{templates,charts}
    
    # Chart.yaml
    cat > "$chart_name/Chart.yaml" << EOF
apiVersion: v2
name: $chart_name
description: A Helm chart for $chart_name
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - $chart_name
home: https://github.com/org/$chart_name
sources:
  - https://github.com/org/$chart_name
maintainers:
  - name: Team Name
    email: team@example.com
dependencies: []
EOF

    # values.yaml
    cat > "$chart_name/values.yaml" << 'EOF'
# Default values for the application
replicaCount: 2

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: ""

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}
podSecurityContext:
  fsGroup: 2000
  runAsNonRoot: true
  runAsUser: 1000

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: false
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

persistence:
  enabled: false
  storageClass: ""
  accessMode: ReadWriteOnce
  size: 8Gi

nodeSelector: {}
tolerations: []
affinity: {}

# Application config
config:
  logLevel: info
  debug: false

# Secrets - use external secrets in production
secrets: {}

# Health check paths
healthcheck:
  liveness:
    path: /health
    initialDelaySeconds: 30
    periodSeconds: 10
  readiness:
    path: /ready
    initialDelaySeconds: 5
    periodSeconds: 5
EOF

    # _helpers.tpl
    cat > "$chart_name/templates/_helpers.tpl" << 'EOF'
{{/*
Expand the name of the chart.
*/}}
{{- define "app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "app.labels" -}}
helm.sh/chart: {{ include "app.chart" . }}
{{ include "app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
EOF
}
```

### 7. Advanced Multi-Environment Configuration

Handle environment-specific configurations with GitOps:

**FluxCD GitOps Setup**
```yaml
# infrastructure/flux-system/gotk-sync.yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 1m0s
  ref:
    branch: main
  url: https://github.com/org/k8s-gitops
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 10m0s
  path: "./clusters/production"
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  validation: client
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: myapp
      namespace: production

---
# Advanced Kustomization with Helm
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - namespace.yaml
  - ../../base
  - monitoring/
  - security/

namespace: production

helmCharts:
  - name: prometheus
    repo: https://prometheus-community.github.io/helm-charts
    version: 15.0.0
    releaseName: prometheus
    namespace: monitoring
    valuesInline:
      server:
        persistentVolume:
          size: 50Gi
      alertmanager:
        enabled: true

patchesStrategicMerge:
  - deployment-patch.yaml
  - service-patch.yaml

patchesJson6902:
  - target:
      version: v1
      kind: Deployment
      name: myapp
    patch: |
      - op: replace
        path: /spec/replicas
        value: 10
      - op: add
        path: /spec/template/spec/containers/0/resources/limits/nvidia.com~1gpu
        value: "1"

configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - ENV=production
      - LOG_LEVEL=warn
      - DATABASE_POOL_SIZE=20
      - CACHE_TTL=3600
    files:
      - config/production.yaml

secretGenerator:
  - name: app-secrets
    behavior: replace
    type: Opaque
    options:
      disableNameSuffixHash: true
    files:
      - .env.production

replicas:
  - name: myapp
    count: 10

images:
  - name: myapp
    newTag: v1.2.3

commonLabels:
  app: myapp
  env: production
  version: v1.2.3

commonAnnotations:
  deployment.kubernetes.io/revision: "1"
  prometheus.io/scrape: "true"

resources:
  - hpa.yaml
  - vpa.yaml
  - pdb.yaml
  - networkpolicy.yaml
  - servicemonitor.yaml
  - backup.yaml
```

### 8. Advanced Security Manifests

Create comprehensive security-focused resources:

**Pod Security Standards (PSS)**
```yaml
# Namespace with Pod Security Standards
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
    name: ${NAMESPACE}
---
# Advanced Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-netpol
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      app: ${APP_NAME}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
      podSelector: {}
    - namespaceSelector:
        matchLabels:
          name: monitoring
      podSelector:
        matchLabels:
          app: prometheus
    ports:
    - protocol: TCP
      port: 8080
    - protocol: TCP
      port: 9090  # metrics
  egress:
  # Database access
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
    - protocol: TCP
      port: 6379  # Redis
  # External API access
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 80
  # DNS resolution
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
---
# Open Policy Agent Gatekeeper Constraints
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: requiredlabels
spec:
  crd:
    spec:
      names:
        kind: RequiredLabels
      validation:
        properties:
          labels:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package requiredlabels
        
        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: RequiredLabels
metadata:
  name: must-have-app-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "version", "component"]
---
# Falco Security Rules
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-rules
  namespace: falco
data:
  application_rules.yaml: |
    - rule: Suspicious Network Activity
      desc: Detect suspicious network connections
      condition: >
        (spawned_process and container and
         ((proc.name in (nc, ncat, netcat, netcat.traditional) and
           proc.args contains "-l") or
          (proc.name = socat and proc.args contains "TCP-LISTEN")))
      output: >
        Suspicious network tool launched in container
        (user=%user.name command=%proc.cmdline image=%container.image.repository)
      priority: WARNING
      tags: [network, mitre_lateral_movement]
    
    - rule: Unexpected Outbound Connection
      desc: An unexpected outbound connection was established
      condition: >
        outbound and not proc.name in (known_outbound_processes) and
        not fd.sip in (allowed_external_ips)
      output: >
        Unexpected outbound connection
        (command=%proc.cmdline connection=%fd.name user=%user.name)
      priority: WARNING
      tags: [network, mitre_exfiltration]
---
# Service Mesh Security (Istio)
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: ${APP_NAME}-authz
  namespace: ${NAMESPACE}
spec:
  selector:
    matchLabels:
      app: ${APP_NAME}
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/frontend/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
  - from:
    - source:
        principals: ["cluster.local/ns/monitoring/sa/prometheus"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/metrics"]
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: ${APP_NAME}-peer-authn
  namespace: ${NAMESPACE}
spec:
  selector:
    matchLabels:
      app: ${APP_NAME}
  mtls:
    mode: STRICT
```

### 9. Advanced Observability Setup

Configure comprehensive monitoring, logging, and tracing:

**OpenTelemetry Integration**
```yaml
# OpenTelemetry Collector
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-collector
  namespace: ${NAMESPACE}
spec:
  mode: daemonset
  serviceAccount: otel-collector
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      prometheus:
        config:
          scrape_configs:
            - job_name: 'kubernetes-pods'
              kubernetes_sd_configs:
                - role: pod
      k8s_cluster:
        auth_type: serviceAccount
      kubeletstats:
        collection_interval: 20s
        auth_type: "serviceAccount"
        endpoint: "${env:K8S_NODE_NAME}:10250"
        insecure_skip_verify: true
    
    processors:
      batch:
        timeout: 1s
        send_batch_size: 1024
      memory_limiter:
        limit_mib: 512
      k8sattributes:
        auth_type: "serviceAccount"
        passthrough: false
        filter:
          node_from_env_var: KUBE_NODE_NAME
        extract:
          metadata:
            - k8s.pod.name
            - k8s.pod.uid
            - k8s.deployment.name
            - k8s.namespace.name
            - k8s.node.name
            - k8s.pod.start_time
    
    exporters:
      prometheus:
        endpoint: "0.0.0.0:8889"
      jaeger:
        endpoint: jaeger-collector:14250
        tls:
          insecure: true
      loki:
        endpoint: http://loki:3100/loki/api/v1/push
    
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [jaeger]
        metrics:
          receivers: [otlp, prometheus, k8s_cluster, kubeletstats]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [prometheus]
        logs:
          receivers: [otlp]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [loki]
---
# Enhanced ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app: ${APP_NAME}
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
    honorLabels: true
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'go_.*'
      action: drop
    - sourceLabels: [__name__]
      regex: 'promhttp_.*'
      action: drop
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - sourceLabels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      targetLabel: __metrics_path__
      regex: (.+)
    - sourceLabels: [__meta_kubernetes_pod_ip]
      action: replace
      targetLabel: __address__
      regex: (.*)
      replacement: $1:9090
---
# Custom Prometheus Rules
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ${APP_NAME}-rules
  namespace: ${NAMESPACE}
spec:
  groups:
  - name: ${APP_NAME}.rules
    rules:
    - alert: HighErrorRate
      expr: |
        (
          rate(http_requests_total{job="${APP_NAME}",status=~"5.."}[5m])
          /
          rate(http_requests_total{job="${APP_NAME}"}[5m])
        ) > 0.05
      for: 5m
      labels:
        severity: warning
        service: ${APP_NAME}
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.job }}"
    
    - alert: HighResponseTime
      expr: |
        histogram_quantile(0.95,
          rate(http_request_duration_seconds_bucket{job="${APP_NAME}"}[5m])
        ) > 0.5
      for: 5m
      labels:
        severity: warning
        service: ${APP_NAME}
      annotations:
        summary: "High response time detected"
        description: "95th percentile response time is {{ $value }}s for {{ $labels.job }}"
    
    - alert: PodCrashLooping
      expr: |
        increase(kube_pod_container_status_restarts_total{pod=~"${APP_NAME}-.*"}[1h]) > 5
      for: 5m
      labels:
        severity: critical
        service: ${APP_NAME}
      annotations:
        summary: "Pod is crash looping"
        description: "Pod {{ $labels.pod }} has restarted {{ $value }} times in the last hour"
---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "${APP_NAME} Dashboard",
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"${APP_NAME}\"}[5m])",
                "legendFormat": "{{ $labels.method }} {{ $labels.status }}"
              }
            ]
          },
          {
            "title": "Response Time",
            "type": "graph", 
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"${APP_NAME}\"}[5m]))",
                "legendFormat": "95th percentile"
              },
              {
                "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{job=\"${APP_NAME}\"}[5m]))",
                "legendFormat": "50th percentile"
              }
            ]
          }
        ]
      }
    }
```

### 10. Advanced GitOps Integration

Prepare manifests for enterprise GitOps:

**Multi-Cluster ArgoCD Application**
```yaml
# Application Set for Multi-Environment Deployment
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ${APP_NAME}-appset
  namespace: argocd
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          argocd.argoproj.io/secret-type: cluster
  - git:
      repoURL: https://github.com/org/k8s-manifests
      revision: HEAD
      directories:
      - path: apps/${APP_NAME}/overlays/*
  template:
    metadata:
      name: '${APP_NAME}-{{path.basename}}'
      labels:
        app: ${APP_NAME}
        env: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/k8s-manifests
        targetRevision: HEAD
        path: 'apps/${APP_NAME}/overlays/{{path.basename}}'
      destination:
        server: '{{server}}'
        namespace: '${APP_NAME}-{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
          allowEmpty: false
        syncOptions:
        - CreateNamespace=true
        - PrunePropagationPolicy=foreground
        - RespectIgnoreDifferences=true
        - ApplyOutOfSyncOnly=true
        managedNamespaceMetadata:
          labels:
            pod-security.kubernetes.io/enforce: restricted
            managed-by: argocd
        retry:
          limit: 5
          backoff:
            duration: 5s
            factor: 2
            maxDuration: 3m
      ignoreDifferences:
      - group: apps
        kind: Deployment
        jsonPointers:
        - /spec/replicas
      - group: autoscaling
        kind: HorizontalPodAutoscaler
        jsonPointers:
        - /spec/minReplicas
        - /spec/maxReplicas
---
# Progressive Rollout with Argo Rollouts
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 10
  strategy:
    canary:
      maxSurge: "25%"
      maxUnavailable: 0
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 2
        args:
        - name: service-name
          value: ${APP_NAME}
      steps:
      - setWeight: 10
      - pause: {duration: 60s}
      - setWeight: 20
      - pause: {duration: 60s}
      - analysis:
          templates:
          - templateName: success-rate
          args:
          - name: service-name
            value: ${APP_NAME}
      - setWeight: 40
      - pause: {duration: 60s}
      - setWeight: 60
      - pause: {duration: 60s}
      - setWeight: 80
      - pause: {duration: 60s}
      trafficRouting:
        istio:
          virtualService:
            name: ${APP_NAME}
            routes:
            - primary
          destinationRule:
            name: ${APP_NAME}
            canarySubsetName: canary
            stableSubsetName: stable
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
# Analysis Template for Rollouts
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
  namespace: ${NAMESPACE}
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 60s
    count: 5
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(
            rate(http_requests_total{job="{{args.service-name}}",status!~"5.."}[5m])
          ) /
          sum(
            rate(http_requests_total{job="{{args.service-name}}"}[5m])
          )
---
# Multi-Cluster Service Mirror (Linkerd)
apiVersion: linkerd.io/v1alpha2
kind: Link
metadata:
  name: ${APP_NAME}-west
  namespace: ${NAMESPACE}
  annotations:
    multicluster.linkerd.io/target-cluster-name: west
spec:
  targetClusterName: west
  targetClusterDomain: cluster.local
  selector:
    matchLabels:
      app: ${APP_NAME}
      mirror.linkerd.io/exported: "true"
```

### 11. Validation and Testing

Validate generated manifests:

**Manifest Validation Script**
```python
#!/usr/bin/env python3
import yaml
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class ManifestValidator:
    def __init__(self):
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        
        self.api_client = client.ApiClient()
    
    def validate_manifest(self, manifest_file):
        """
        Validate Kubernetes manifest
        """
        with open(manifest_file) as f:
            manifests = list(yaml.safe_load_all(f))
        
        results = []
        for manifest in manifests:
            result = {
                'kind': manifest.get('kind'),
                'name': manifest.get('metadata', {}).get('name'),
                'valid': False,
                'errors': []
            }
            
            # Dry run validation
            try:
                self._dry_run_apply(manifest)
                result['valid'] = True
            except ApiException as e:
                result['errors'].append(str(e))
            
            # Security checks
            security_issues = self._check_security(manifest)
            if security_issues:
                result['errors'].extend(security_issues)
            
            # Best practices checks
            bp_issues = self._check_best_practices(manifest)
            if bp_issues:
                result['errors'].extend(bp_issues)
            
            results.append(result)
        
        return results
    
    def _check_security(self, manifest):
        """Check security best practices"""
        issues = []
        
        if manifest.get('kind') == 'Deployment':
            spec = manifest.get('spec', {}).get('template', {}).get('spec', {})
            
            # Check security context
            if not spec.get('securityContext'):
                issues.append("Missing pod security context")
            
            # Check container security
            for container in spec.get('containers', []):
                if not container.get('securityContext'):
                    issues.append(f"Container {container['name']} missing security context")
                
                sec_ctx = container.get('securityContext', {})
                if not sec_ctx.get('runAsNonRoot'):
                    issues.append(f"Container {container['name']} not configured to run as non-root")
                
                if not sec_ctx.get('readOnlyRootFilesystem'):
                    issues.append(f"Container {container['name']} has writable root filesystem")
        
        return issues
```

### 11. Advanced Scaling and Performance

Implement intelligent scaling strategies:

**KEDA Autoscaling**
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: ${APP_NAME}-scaler
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    name: ${APP_NAME}
  pollingInterval: 30
  cooldownPeriod: 300
  idleReplicaCount: 2
  minReplicaCount: 2
  maxReplicaCount: 50
  fallback:
    failureThreshold: 3
    replicas: 5
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: http_requests_per_second
      threshold: '100'
      query: sum(rate(http_requests_total{job="${APP_NAME}"}[2m]))
  - type: memory
    metadata:
      type: Utilization
      value: "70"
  - type: cpu
    metadata:
      type: Utilization
      value: "70"
---
# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ${APP_NAME}-vpa
  namespace: ${NAMESPACE}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  updatePolicy:
    updateMode: "Auto"
    minReplicas: 2
  resourcePolicy:
    containerPolicies:
    - containerName: ${APP_NAME}
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
---
# Pod Disruption Budget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${APP_NAME}-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: ${APP_NAME}
```

### 12. CI/CD Integration

Modern deployment pipeline integration:

**GitHub Actions Workflow**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]
    paths: ['src/**', 'k8s/**', 'Dockerfile']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup GitVersion
      uses: gittools/actions/gitversion/setup@v0.9.15
      with:
        versionSpec: '5.x'
    
    - name: Determine Version
      uses: gittools/actions/gitversion/execute@v0.9.15
      id: gitversion
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.gitversion.outputs.semVer }}
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
        build-args: |
          VERSION=${{ steps.gitversion.outputs.semVer }}
          COMMIT_SHA=${{ github.sha }}
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.gitversion.outputs.semVer }}'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Install kubectl and kustomize
      run: |
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl && sudo mv kubectl /usr/local/bin/
        curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
        sudo mv kustomize /usr/local/bin/
    
    - name: Validate Kubernetes manifests
      run: |
        kubectl --dry-run=client --validate=true apply -k k8s/overlays/staging
    
    - name: Deploy to staging
      if: github.ref == 'refs/heads/main'
      run: |
        cd k8s/overlays/staging
        kustomize edit set image app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.gitversion.outputs.semVer }}
        kubectl apply -k .
        kubectl rollout status deployment/${APP_NAME} -n staging --timeout=300s
    
    - name: Run integration tests
      if: github.ref == 'refs/heads/main'
      run: |
        # Wait for deployment to be ready
        kubectl wait --for=condition=available --timeout=300s deployment/${APP_NAME} -n staging
        # Run tests
        npm run test:integration
    
    - name: Deploy to production
      if: github.ref == 'refs/heads/main' && success()
      run: |
        cd k8s/overlays/production
        kustomize edit set image app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.gitversion.outputs.semVer }}
        kubectl apply -k .
        kubectl rollout status deployment/${APP_NAME} -n production --timeout=600s
```

## Output Format

1. **Framework-Optimized Manifests**: Tailored deployment configurations
2. **Advanced Security Bundle**: PSS, OPA, Falco, service mesh policies
3. **GitOps Repository Structure**: Multi-environment with FluxCD/ArgoCD
4. **Observability Stack**: OpenTelemetry, Prometheus, Grafana, Jaeger
5. **Progressive Delivery Setup**: Argo Rollouts with canary deployment
6. **Auto-scaling Configuration**: HPA, VPA, KEDA for intelligent scaling
7. **Multi-Cluster Setup**: Service mesh and cross-cluster communication
8. **CI/CD Pipeline**: Complete GitHub Actions workflow with security scanning
9. **Disaster Recovery Plan**: Backup strategies and restoration procedures
10. **Performance Benchmarks**: Load testing and optimization recommendations

## Cross-Command Integration

### Complete Cloud-Native Deployment Workflow

**Enterprise Kubernetes Pipeline**
```bash
# 1. Generate cloud-native API scaffolding
/api-scaffold
framework: "fastapi"
deployment_target: "kubernetes"
cloud_native: true
observability: ["prometheus", "jaeger", "grafana"]

# 2. Optimize containers for Kubernetes
/docker-optimize
optimization_level: "kubernetes"
multi_arch_build: true
security_hardening: true

# 3. Comprehensive security scanning
/security-scan
scan_types: ["k8s", "container", "iac", "rbac"]
compliance: ["cis", "nsa", "pci"]

# 4. Generate production K8s manifests
/k8s-manifest
environment: "production"
security_level: "enterprise"
auto_scaling: true
service_mesh: true
```

**Integrated Kubernetes Configuration**
```python
# k8s-integration-config.py - Shared across all commands
class IntegratedKubernetesConfig:
    def __init__(self):
        self.api_config = self.load_api_config()           # From /api-scaffold
        self.container_config = self.load_container_config() # From /docker-optimize
        self.security_config = self.load_security_config() # From /security-scan
        self.test_config = self.load_test_config()         # From /test-harness
        
    def generate_application_manifests(self):
        """Generate complete K8s manifests for the application stack"""
        manifests = {
            'namespace': self.generate_namespace_manifest(),
            'secrets': self.generate_secrets_manifests(),
            'configmaps': self.generate_configmap_manifests(),
            'deployments': self.generate_deployment_manifests(),
            'services': self.generate_service_manifests(),
            'ingress': self.generate_ingress_manifests(),
            'security': self.generate_security_manifests(),
            'monitoring': self.generate_monitoring_manifests(),
            'autoscaling': self.generate_autoscaling_manifests()
        }
        return manifests
    
    def generate_deployment_manifests(self):
        """Generate deployment manifests from API and container configs"""
        deployments = []
        
        # API deployment
        if self.api_config.get('framework'):
            api_deployment = {
                'apiVersion': 'apps/v1',
                'kind': 'Deployment',
                'metadata': {
                    'name': f"{self.api_config['name']}-api",
                    'namespace': self.api_config.get('namespace', 'default'),
                    'labels': {
                        'app': f"{self.api_config['name']}-api",
                        'framework': self.api_config['framework'],
                        'version': self.api_config.get('version', 'v1.0.0'),
                        'component': 'backend'
                    }
                },
                'spec': {
                    'replicas': self.calculate_replica_count(),
                    'selector': {
                        'matchLabels': {
                            'app': f"{self.api_config['name']}-api"
                        }
                    },
                    'template': {
                        'metadata': {
                            'labels': {
                                'app': f"{self.api_config['name']}-api"
                            },
                            'annotations': self.generate_pod_annotations()
                        },
                        'spec': self.generate_pod_spec()
                    }
                }
            }
            deployments.append(api_deployment)
        
        return deployments
    
    def generate_pod_spec(self):
        """Generate optimized pod specification"""
        containers = []
        
        # Main application container
        app_container = {
            'name': 'app',
            'image': self.container_config.get('image_name', 'app:latest'),
            'imagePullPolicy': 'Always',
            'ports': [
                {
                    'name': 'http',
                    'containerPort': self.api_config.get('port', 8000),
                    'protocol': 'TCP'
                }
            ],
            'env': self.generate_environment_variables(),
            'resources': self.calculate_resource_requirements(),
            'securityContext': self.generate_security_context(),
            'livenessProbe': self.generate_health_probes('liveness'),
            'readinessProbe': self.generate_health_probes('readiness'),
            'startupProbe': self.generate_health_probes('startup'),
            'volumeMounts': self.generate_volume_mounts()
        }
        containers.append(app_container)
        
        # Sidecar containers (monitoring, security, etc.)
        if self.should_include_monitoring_sidecar():
            containers.append(self.generate_monitoring_sidecar())
        
        if self.should_include_security_sidecar():
            containers.append(self.generate_security_sidecar())
        
        pod_spec = {
            'serviceAccountName': f"{self.api_config['name']}-sa",
            'securityContext': self.generate_pod_security_context(),
            'containers': containers,
            'volumes': self.generate_volumes(),
            'initContainers': self.generate_init_containers(),
            'nodeSelector': self.generate_node_selector(),
            'tolerations': self.generate_tolerations(),
            'affinity': self.generate_affinity_rules(),
            'topologySpreadConstraints': self.generate_topology_constraints()
        }
        
        return pod_spec
    
    def generate_security_context(self):
        """Generate container security context from security scan results"""
        security_level = self.security_config.get('level', 'standard')
        
        base_context = {
            'allowPrivilegeEscalation': False,
            'readOnlyRootFilesystem': True,
            'runAsNonRoot': True,
            'runAsUser': 1001,
            'capabilities': {
                'drop': ['ALL']
            }
        }
        
        if security_level == 'enterprise':
            base_context.update({
                'seccompProfile': {'type': 'RuntimeDefault'},
                'capabilities': {
                    'drop': ['ALL'],
                    'add': ['NET_BIND_SERVICE'] if self.api_config.get('privileged_port') else []
                }
            })
        
        return base_context
```

**Database Integration with Kubernetes**
```yaml
# database-k8s-manifests.yaml - From /db-migrate + /k8s-manifest
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
  namespace: production
type: Opaque
data:
  username: cG9zdGdyZXM=  # postgres (base64)
  password: <ENCODED_PASSWORD>
  database: YXBwX2Ri  # app_db (base64)

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: database-config
  namespace: production
data:
  postgresql.conf: |
    # Performance tuning from /db-migrate analysis
    shared_buffers = 256MB
    effective_cache_size = 1GB
    work_mem = 4MB
    maintenance_work_mem = 64MB
    
    # Security settings from /security-scan
    ssl = on
    log_connections = on
    log_disconnections = on
    log_statement = 'all'
    
    # Monitoring settings
    shared_preload_libraries = 'pg_stat_statements'
    track_activity_query_size = 2048

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
  namespace: production
spec:
  serviceName: database-headless
  replicas: 3  # High availability setup
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      serviceAccountName: database-sa
      securityContext:
        runAsUser: 999
        runAsGroup: 999
        fsGroup: 999
      containers:
      - name: postgresql
        image: postgres:15-alpine
        ports:
        - name: postgresql
          containerPort: 5432
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: password
        - name: POSTGRES_DB
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: database
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - name: database-storage
          mountPath: /var/lib/postgresql/data
        - name: database-config
          mountPath: /etc/postgresql/postgresql.conf
          subPath: postgresql.conf
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 5
          periodSeconds: 5
      # Migration init container from /db-migrate
      initContainers:
      - name: migration
        image: migration-runner:latest
        env:
        - name: DATABASE_URL
          value: "postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@localhost:5432/$(POSTGRES_DB)"
        envFrom:
        - secretRef:
            name: database-credentials
        command:
        - sh
        - -c
        - |
          echo "Running database migrations..."
          alembic upgrade head
          echo "Migrations completed successfully"
      volumes:
      - name: database-config
        configMap:
          name: database-config
  volumeClaimTemplates:
  - metadata:
      name: database-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi

---
apiVersion: v1
kind: Service
metadata:
  name: database-headless
  namespace: production
spec:
  clusterIP: None
  selector:
    app: database
  ports:
  - name: postgresql
    port: 5432
    targetPort: 5432

---
apiVersion: v1
kind: Service
metadata:
  name: database
  namespace: production
spec:
  selector:
    app: database
  ports:
  - name: postgresql
    port: 5432
    targetPort: 5432
  type: ClusterIP
```

**Frontend + Backend Integration**
```yaml
# fullstack-k8s-deployment.yaml - Integration across all commands
apiVersion: v1
kind: Namespace
metadata:
  name: fullstack-app
  labels:
    name: fullstack-app
    security-policy: strict

---
# API deployment (from /api-scaffold + optimizations)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  namespace: fullstack-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
      tier: backend
  template:
    metadata:
      labels:
        app: api
        tier: backend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: api-service-account
      containers:
      - name: api
        image: registry.company.com/api:optimized-latest
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1001
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
# Frontend deployment (from /frontend-optimize + container optimization)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  namespace: fullstack-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
      tier: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
    spec:
      containers:
      - name: frontend
        image: registry.company.com/frontend:optimized-latest
        ports:
        - containerPort: 80
          name: http
        env:
        - name: API_URL
          value: "http://api-service:8000"
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1001
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5

---
# Services
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: fullstack-app
spec:
  selector:
    app: api
    tier: backend
  ports:
  - name: http
    port: 8000
    targetPort: 8000
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: fullstack-app
spec:
  selector:
    app: frontend
    tier: frontend
  ports:
  - name: http
    port: 80
    targetPort: 80
  type: ClusterIP

---
# Ingress with security configurations from /security-scan
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: fullstack-app
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/add-base-url: "true"
    nginx.ingress.kubernetes.io/proxy-buffer-size: "8k"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.company.com
    secretName: app-tls-secret
  rules:
  - host: app.company.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

**Security Integration**
```yaml
# security-k8s-manifests.yaml - From /security-scan integration
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-service-account
  namespace: fullstack-app
automountServiceAccountToken: false

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: api-role
  namespace: fullstack-app
rules:
- apiGroups: [""]
  resources: ["secrets", "configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-role-binding
  namespace: fullstack-app
subjects:
- kind: ServiceAccount
  name: api-service-account
  namespace: fullstack-app
roleRef:
  kind: Role
  name: api-role
  apiGroup: rbac.authorization.k8s.io

---
# Network policies for security isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: fullstack-app
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []  # Allow DNS
    ports:
    - protocol: UDP
      port: 53

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-network-policy
  namespace: fullstack-app
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: api
    ports:
    - protocol: TCP
      port: 8000

---
# Pod Security Standards
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
  namespace: fullstack-app
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
      ephemeral-storage: "1Gi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
      ephemeral-storage: "500Mi"
    type: Container
  - max:
      cpu: "2"
      memory: "4Gi"
      ephemeral-storage: "10Gi"
    type: Container

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
  namespace: fullstack-app
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: api

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: frontend-pdb
  namespace: fullstack-app
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: frontend
```

**Monitoring and Observability Integration**
```yaml
# monitoring-k8s-manifests.yaml - Complete observability stack
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: api-monitor
  namespace: fullstack-app
  labels:
    app: api
spec:
  selector:
    matchLabels:
      app: api
  endpoints:
  - port: http
    path: /metrics
    interval: 30s

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: monitoring
data:
  app-dashboard.json: |
    {
      "dashboard": {
        "title": "Application Metrics",
        "panels": [
          {
            "title": "API Response Time",
            "targets": [
              {
                "expr": "http_request_duration_seconds{job=\"api-service\"}",
                "legendFormat": "Response Time"
              }
            ]
          },
          {
            "title": "Error Rate",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"api-service\",status=~\"5..\"}[5m])",
                "legendFormat": "5xx Errors"
              }
            ]
          }
        ]
      }
    }

---
# Jaeger tracing configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-config
  namespace: fullstack-app
data:
  jaeger.yaml: |
    sampling:
      type: probabilistic
      param: 0.1
    reporter:
      logSpans: true
      localAgentHostPort: jaeger-agent:6831

---
# Application logging configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: fullstack-app
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         1
        Log_Level     info
        Daemon        off
        Parsers_File  parsers.conf
    
    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Parser            docker
        Tag               kube.*
        Refresh_Interval  5
        Mem_Buf_Limit     5MB
        Skip_Long_Lines   On
    
    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc:443
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
        Merge_Log           On
    
    [OUTPUT]
        Name  es
        Match *
        Host  elasticsearch.logging.svc.cluster.local
        Port  9200
        Index app-logs
```

**Auto-scaling Integration**
```yaml
# autoscaling-k8s-manifests.yaml - Intelligent scaling based on multiple metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: fullstack-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 25
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15

---
apiVersion: autoscaling/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
  namespace: fullstack-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: api
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
      controlledResources: ["cpu", "memory"]

---
# KEDA for advanced autoscaling based on external metrics
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: api-scaled-object
  namespace: fullstack-app
spec:
  scaleTargetRef:
    name: api-deployment
  minReplicaCount: 2
  maxReplicaCount: 50
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus.monitoring.svc.cluster.local:9090
      metricName: http_requests_per_second
      threshold: '1000'
      query: sum(rate(http_requests_total{job="api-service"}[1m]))
  - type: redis
    metadata:
      address: redis.fullstack-app.svc.cluster.local:6379
      listName: task_queue
      listLength: '10'
```

**CI/CD Integration Pipeline**
```yaml
# .github/workflows/k8s-deployment.yml
name: Kubernetes Deployment Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  CLUSTER_NAME: production-cluster

jobs:
  deploy-to-kubernetes:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
      id-token: write
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    # 1. Setup kubectl and helm
    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.28.0'
    
    - name: Setup Helm
      uses: azure/setup-helm@v3
      with:
        version: 'v3.12.0'
    
    # 2. Authenticate with cluster
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: us-west-2
    
    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --region us-west-2 --name ${{ env.CLUSTER_NAME }}
    
    # 3. Validate manifests
    - name: Validate Kubernetes manifests
      run: |
        # Validate syntax
        kubectl --dry-run=client apply -f k8s/
        
        # Security validation with kubesec
        docker run --rm -v $(pwd):/workspace kubesec/kubesec:latest scan /workspace/k8s/*.yaml
        
        # Policy validation with OPA Gatekeeper
        conftest verify --policy opa-policies/ k8s/
    
    # 4. Deploy to staging
    - name: Deploy to staging
      if: github.ref == 'refs/heads/develop'
      run: |
        # Update image tags
        sed -i "s|registry.company.com/api:.*|registry.company.com/api:${{ github.sha }}|g" k8s/api-deployment.yaml
        sed -i "s|registry.company.com/frontend:.*|registry.company.com/frontend:${{ github.sha }}|g" k8s/frontend-deployment.yaml
        
        # Apply manifests to staging namespace
        kubectl apply -f k8s/ --namespace=staging
        
        # Wait for rollout to complete
        kubectl rollout status deployment/api-deployment --namespace=staging --timeout=300s
        kubectl rollout status deployment/frontend-deployment --namespace=staging --timeout=300s
    
    # 5. Run integration tests
    - name: Run integration tests
      if: github.ref == 'refs/heads/develop'
      run: |
        # Wait for services to be ready
        kubectl wait --for=condition=ready pod -l app=api --namespace=staging --timeout=300s
        
        # Get service URLs
        API_URL=$(kubectl get service api-service --namespace=staging -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
        
        # Run tests from /test-harness
        pytest tests/integration/ --api-url="http://${API_URL}:8000" -v
    
    # 6. Deploy to production (on main branch)
    - name: Deploy to production
      if: github.ref == 'refs/heads/main'
      run: |
        # Update image tags
        sed -i "s|registry.company.com/api:.*|registry.company.com/api:${{ github.sha }}|g" k8s/api-deployment.yaml
        sed -i "s|registry.company.com/frontend:.*|registry.company.com/frontend:${{ github.sha }}|g" k8s/frontend-deployment.yaml
        
        # Apply manifests to production namespace with rolling update
        kubectl apply -f k8s/ --namespace=production
        
        # Monitor rollout
        kubectl rollout status deployment/api-deployment --namespace=production --timeout=600s
        kubectl rollout status deployment/frontend-deployment --namespace=production --timeout=600s
        
        # Verify deployment health
        kubectl get pods --namespace=production -l app=api
        kubectl get pods --namespace=production -l app=frontend
    
    # 7. Post-deployment verification
    - name: Post-deployment verification
      if: github.ref == 'refs/heads/main'
      run: |
        # Health checks
        kubectl exec -n production deployment/api-deployment -- curl -f http://localhost:8000/health
        
        # Performance baseline check
        kubectl run --rm -i --tty load-test --image=loadimpact/k6:latest --restart=Never -- run - <<EOF
        import http from 'k6/http';
        import { check } from 'k6';
        
        export let options = {
          stages: [
            { duration: '2m', target: 100 },
            { duration: '5m', target: 100 },
            { duration: '2m', target: 0 },
          ],
        };
        
        export default function () {
          let response = http.get('http://api-service.production.svc.cluster.local:8000/health');
          check(response, {
            'status is 200': (r) => r.status === 200,
            'response time < 500ms': (r) => r.timings.duration < 500,
          });
        }
        EOF
    
    # 8. Cleanup on failure
    - name: Rollback on failure
      if: failure()
      run: |
        # Rollback to previous version
        kubectl rollout undo deployment/api-deployment --namespace=production
        kubectl rollout undo deployment/frontend-deployment --namespace=production
        
        # Notify team
        echo "Deployment failed and rolled back" >> $GITHUB_STEP_SUMMARY
```

This comprehensive integration ensures that Kubernetes deployments leverage all optimizations from container builds, security hardening, database migrations, and monitoring configurations while providing enterprise-grade reliability and observability.

Focus on creating enterprise-grade, cloud-native deployments with zero-downtime deployment capabilities and comprehensive observability.