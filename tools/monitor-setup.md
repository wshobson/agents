# Monitoring and Observability Setup

You are a monitoring and observability expert specializing in implementing comprehensive monitoring solutions. Set up metrics collection, distributed tracing, log aggregation, and create insightful dashboards that provide full visibility into system health and performance.

## Context
The user needs to implement or improve monitoring and observability. Focus on the three pillars of observability (metrics, logs, traces), setting up monitoring infrastructure, creating actionable dashboards, and establishing effective alerting strategies.

## Requirements
$ARGUMENTS

## Instructions

### 1. Monitoring Requirements Analysis

Analyze monitoring needs and current state:

**Monitoring Assessment**
```python
import yaml
from pathlib import Path
from collections import defaultdict

class MonitoringAssessment:
    def analyze_infrastructure(self, project_path):
        """
        Analyze infrastructure and determine monitoring needs
        """
        assessment = {
            'infrastructure': self._detect_infrastructure(project_path),
            'services': self._identify_services(project_path),
            'current_monitoring': self._check_existing_monitoring(project_path),
            'metrics_needed': self._determine_metrics(project_path),
            'compliance_requirements': self._check_compliance_needs(project_path),
            'recommendations': []
        }
        
        self._generate_recommendations(assessment)
        return assessment
    
    def _detect_infrastructure(self, project_path):
        """Detect infrastructure components"""
        infrastructure = {
            'cloud_provider': None,
            'orchestration': None,
            'databases': [],
            'message_queues': [],
            'cache_systems': [],
            'load_balancers': []
        }
        
        # Check for cloud providers
        if (Path(project_path) / '.aws').exists():
            infrastructure['cloud_provider'] = 'AWS'
        elif (Path(project_path) / 'azure-pipelines.yml').exists():
            infrastructure['cloud_provider'] = 'Azure'
        elif (Path(project_path) / '.gcloud').exists():
            infrastructure['cloud_provider'] = 'GCP'
        
        # Check for orchestration
        if (Path(project_path) / 'docker-compose.yml').exists():
            infrastructure['orchestration'] = 'docker-compose'
        elif (Path(project_path) / 'k8s').exists():
            infrastructure['orchestration'] = 'kubernetes'
        
        return infrastructure
    
    def _determine_metrics(self, project_path):
        """Determine required metrics based on services"""
        metrics = {
            'golden_signals': {
                'latency': ['response_time_p50', 'response_time_p95', 'response_time_p99'],
                'traffic': ['requests_per_second', 'active_connections'],
                'errors': ['error_rate', 'error_count_by_type'],
                'saturation': ['cpu_usage', 'memory_usage', 'disk_usage', 'queue_depth']
            },
            'business_metrics': [],
            'custom_metrics': []
        }
        
        # Add service-specific metrics
        services = self._identify_services(project_path)
        
        if 'web' in services:
            metrics['custom_metrics'].extend([
                'page_load_time',
                'time_to_first_byte',
                'concurrent_users'
            ])
        
        if 'database' in services:
            metrics['custom_metrics'].extend([
                'query_duration',
                'connection_pool_usage',
                'replication_lag'
            ])
        
        if 'queue' in services:
            metrics['custom_metrics'].extend([
                'message_processing_time',
                'queue_length',
                'dead_letter_queue_size'
            ])
        
        return metrics
```

### 2. Prometheus Setup

Implement Prometheus-based monitoring:

**Prometheus Configuration**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Rule files
rule_files:
  - "alerts/*.yml"
  - "recording_rules/*.yml"

# Scrape configurations
scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node exporter for system metrics
  - job_name: 'node'
    static_configs:
      - targets: 
          - 'node-exporter:9100'
    relabel_configs:
      - source_labels: [__address__]
        regex: '([^:]+)(?::\d+)?'
        target_label: instance
        replacement: '${1}'

  # Application metrics
  - job_name: 'application'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name

  # Database monitoring
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
    params:
      query: ['pg_stat_database', 'pg_stat_replication']

  # Redis monitoring
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # Custom service discovery
  - job_name: 'custom-services'
    consul_sd_configs:
      - server: 'consul:8500'
        services: []
    relabel_configs:
      - source_labels: [__meta_consul_service]
        target_label: service_name
      - source_labels: [__meta_consul_tags]
        regex: '.*,metrics,.*'
        action: keep
```

**Custom Metrics Implementation**
```typescript
// metrics.ts
import { Counter, Histogram, Gauge, Registry } from 'prom-client';

export class MetricsCollector {
    private registry: Registry;
    
    // HTTP metrics
    private httpRequestDuration: Histogram<string>;
    private httpRequestTotal: Counter<string>;
    private httpRequestsInFlight: Gauge<string>;
    
    // Business metrics
    private userRegistrations: Counter<string>;
    private activeUsers: Gauge<string>;
    private revenue: Counter<string>;
    
    // System metrics
    private queueDepth: Gauge<string>;
    private cacheHitRatio: Gauge<string>;
    
    constructor() {
        this.registry = new Registry();
        this.initializeMetrics();
    }
    
    private initializeMetrics() {
        // HTTP metrics
        this.httpRequestDuration = new Histogram({
            name: 'http_request_duration_seconds',
            help: 'Duration of HTTP requests in seconds',
            labelNames: ['method', 'route', 'status_code'],
            buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5]
        });
        
        this.httpRequestTotal = new Counter({
            name: 'http_requests_total',
            help: 'Total number of HTTP requests',
            labelNames: ['method', 'route', 'status_code']
        });
        
        this.httpRequestsInFlight = new Gauge({
            name: 'http_requests_in_flight',
            help: 'Number of HTTP requests currently being processed',
            labelNames: ['method', 'route']
        });
        
        // Business metrics
        this.userRegistrations = new Counter({
            name: 'user_registrations_total',
            help: 'Total number of user registrations',
            labelNames: ['source', 'plan']
        });
        
        this.activeUsers = new Gauge({
            name: 'active_users',
            help: 'Number of active users',
            labelNames: ['timeframe']
        });
        
        this.revenue = new Counter({
            name: 'revenue_total_cents',
            help: 'Total revenue in cents',
            labelNames: ['product', 'currency']
        });
        
        // Register all metrics
        this.registry.registerMetric(this.httpRequestDuration);
        this.registry.registerMetric(this.httpRequestTotal);
        this.registry.registerMetric(this.httpRequestsInFlight);
        this.registry.registerMetric(this.userRegistrations);
        this.registry.registerMetric(this.activeUsers);
        this.registry.registerMetric(this.revenue);
    }
    
    // Middleware for Express
    httpMetricsMiddleware() {
        return (req: Request, res: Response, next: NextFunction) => {
            const start = Date.now();
            const route = req.route?.path || req.path;
            
            // Increment in-flight gauge
            this.httpRequestsInFlight.inc({ method: req.method, route });
            
            res.on('finish', () => {
                const duration = (Date.now() - start) / 1000;
                const labels = {
                    method: req.method,
                    route,
                    status_code: res.statusCode.toString()
                };
                
                // Record metrics
                this.httpRequestDuration.observe(labels, duration);
                this.httpRequestTotal.inc(labels);
                this.httpRequestsInFlight.dec({ method: req.method, route });
            });
            
            next();
        };
    }
    
    // Business metric helpers
    recordUserRegistration(source: string, plan: string) {
        this.userRegistrations.inc({ source, plan });
    }
    
    updateActiveUsers(timeframe: string, count: number) {
        this.activeUsers.set({ timeframe }, count);
    }
    
    recordRevenue(product: string, currency: string, amountCents: number) {
        this.revenue.inc({ product, currency }, amountCents);
    }
    
    // Export metrics endpoint
    async getMetrics(): Promise<string> {
        return this.registry.metrics();
    }
}

// Recording rules for Prometheus
export const recordingRules = `
groups:
  - name: aggregations
    interval: 30s
    rules:
      # Request rate
      - record: http_request_rate_5m
        expr: rate(http_requests_total[5m])
      
      # Error rate
      - record: http_error_rate_5m
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
      
      # P95 latency
      - record: http_request_duration_p95_5m
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route)
          )
      
      # Business metrics
      - record: user_registration_rate_1h
        expr: rate(user_registrations_total[1h])
      
      - record: revenue_rate_1d
        expr: rate(revenue_total_cents[1d]) / 100
`;
```

### 3. Grafana Dashboard Setup

Create comprehensive dashboards:

**Dashboard Configuration**
```json
{
  "dashboard": {
    "title": "Application Overview",
    "tags": ["production", "overview"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (method)",
            "legendFormat": "{{method}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "gridPos": { "x": 12, "y": 0, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
            "legendFormat": "Error Rate"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": { "params": [0.05], "type": "gt" },
              "query": { "params": ["A", "5m", "now"] },
              "reducer": { "type": "avg" },
              "type": "query"
            }
          ],
          "name": "High Error Rate"
        }
      },
      {
        "title": "Response Time",
        "type": "graph",
        "gridPos": { "x": 0, "y": 8, "w": 12, "h": 8 },
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p99"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "stat",
        "gridPos": { "x": 12, "y": 8, "w": 6, "h": 4 },
        "targets": [
          {
            "expr": "active_users{timeframe=\"realtime\"}"
          }
        ]
      }
    ]
  }
}
```

**Dashboard as Code**
```typescript
// dashboards/service-dashboard.ts
import { Dashboard, Panel, Target } from '@grafana/toolkit';

export const createServiceDashboard = (serviceName: string): Dashboard => {
    return new Dashboard({
        title: `${serviceName} Service Dashboard`,
        uid: `${serviceName}-overview`,
        tags: ['service', serviceName],
        time: { from: 'now-6h', to: 'now' },
        refresh: '30s',
        
        panels: [
            // Row 1: Golden Signals
            new Panel.Graph({
                title: 'Request Rate',
                gridPos: { x: 0, y: 0, w: 6, h: 8 },
                targets: [
                    new Target({
                        expr: `sum(rate(http_requests_total{service="${serviceName}"}[5m])) by (method)`,
                        legendFormat: '{{method}}'
                    })
                ]
            }),
            
            new Panel.Graph({
                title: 'Error Rate',
                gridPos: { x: 6, y: 0, w: 6, h: 8 },
                targets: [
                    new Target({
                        expr: `sum(rate(http_requests_total{service="${serviceName}",status_code=~"5.."}[5m])) / sum(rate(http_requests_total{service="${serviceName}"}[5m]))`,
                        legendFormat: 'Error %'
                    })
                ],
                yaxes: [{ format: 'percentunit' }]
            }),
            
            new Panel.Graph({
                title: 'Latency Percentiles',
                gridPos: { x: 12, y: 0, w: 12, h: 8 },
                targets: [
                    new Target({
                        expr: `histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{service="${serviceName}"}[5m])) by (le))`,
                        legendFormat: 'p50'
                    }),
                    new Target({
                        expr: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service="${serviceName}"}[5m])) by (le))`,
                        legendFormat: 'p95'
                    }),
                    new Target({
                        expr: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="${serviceName}"}[5m])) by (le))`,
                        legendFormat: 'p99'
                    })
                ],
                yaxes: [{ format: 's' }]
            }),
            
            // Row 2: Resource Usage
            new Panel.Graph({
                title: 'CPU Usage',
                gridPos: { x: 0, y: 8, w: 8, h: 8 },
                targets: [
                    new Target({
                        expr: `avg(rate(container_cpu_usage_seconds_total{pod=~"${serviceName}-.*"}[5m])) by (pod)`,
                        legendFormat: '{{pod}}'
                    })
                ],
                yaxes: [{ format: 'percentunit' }]
            }),
            
            new Panel.Graph({
                title: 'Memory Usage',
                gridPos: { x: 8, y: 8, w: 8, h: 8 },
                targets: [
                    new Target({
                        expr: `avg(container_memory_working_set_bytes{pod=~"${serviceName}-.*"}) by (pod)`,
                        legendFormat: '{{pod}}'
                    })
                ],
                yaxes: [{ format: 'bytes' }]
            }),
            
            new Panel.Graph({
                title: 'Network I/O',
                gridPos: { x: 16, y: 8, w: 8, h: 8 },
                targets: [
                    new Target({
                        expr: `sum(rate(container_network_receive_bytes_total{pod=~"${serviceName}-.*"}[5m])) by (pod)`,
                        legendFormat: '{{pod}} RX'
                    }),
                    new Target({
                        expr: `sum(rate(container_network_transmit_bytes_total{pod=~"${serviceName}-.*"}[5m])) by (pod)`,
                        legendFormat: '{{pod}} TX'
                    })
                ],
                yaxes: [{ format: 'Bps' }]
            })
        ]
    });
};
```

### 4. Distributed Tracing Setup

Implement OpenTelemetry-based tracing:

**OpenTelemetry Configuration**
```typescript
// tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { PrometheusExporter } from '@opentelemetry/exporter-prometheus';

export class TracingSetup {
    private sdk: NodeSDK;
    
    constructor(serviceName: string, environment: string) {
        const jaegerExporter = new JaegerExporter({
            endpoint: process.env.JAEGER_ENDPOINT || 'http://localhost:14268/api/traces',
        });
        
        const prometheusExporter = new PrometheusExporter({
            port: 9464,
            endpoint: '/metrics',
        }, () => {
            console.log('Prometheus metrics server started on port 9464');
        });
        
        this.sdk = new NodeSDK({
            resource: new Resource({
                [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
                [SemanticResourceAttributes.SERVICE_VERSION]: process.env.SERVICE_VERSION || '1.0.0',
                [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: environment,
            }),
            
            traceExporter: jaegerExporter,
            spanProcessor: new BatchSpanProcessor(jaegerExporter, {
                maxQueueSize: 2048,
                maxExportBatchSize: 512,
                scheduledDelayMillis: 5000,
                exportTimeoutMillis: 30000,
            }),
            
            metricExporter: prometheusExporter,
            
            instrumentations: [
                getNodeAutoInstrumentations({
                    '@opentelemetry/instrumentation-fs': {
                        enabled: false,
                    },
                }),
            ],
        });
    }
    
    start() {
        this.sdk.start()
            .then(() => console.log('Tracing initialized'))
            .catch((error) => console.error('Error initializing tracing', error));
    }
    
    shutdown() {
        return this.sdk.shutdown()
            .then(() => console.log('Tracing terminated'))
            .catch((error) => console.error('Error terminating tracing', error));
    }
}

// Custom span creation
import { trace, context, SpanStatusCode, SpanKind } from '@opentelemetry/api';

export class CustomTracer {
    private tracer = trace.getTracer('custom-tracer', '1.0.0');
    
    async traceOperation<T>(
        operationName: string,
        operation: () => Promise<T>,
        attributes?: Record<string, any>
    ): Promise<T> {
        const span = this.tracer.startSpan(operationName, {
            kind: SpanKind.INTERNAL,
            attributes,
        });
        
        return context.with(trace.setSpan(context.active(), span), async () => {
            try {
                const result = await operation();
                span.setStatus({ code: SpanStatusCode.OK });
                return result;
            } catch (error) {
                span.recordException(error as Error);
                span.setStatus({
                    code: SpanStatusCode.ERROR,
                    message: error.message,
                });
                throw error;
            } finally {
                span.end();
            }
        });
    }
    
    // Database query tracing
    async traceQuery<T>(
        queryName: string,
        query: () => Promise<T>,
        sql?: string
    ): Promise<T> {
        return this.traceOperation(
            `db.query.${queryName}`,
            query,
            {
                'db.system': 'postgresql',
                'db.operation': queryName,
                'db.statement': sql,
            }
        );
    }
    
    // HTTP request tracing
    async traceHttpRequest<T>(
        method: string,
        url: string,
        request: () => Promise<T>
    ): Promise<T> {
        return this.traceOperation(
            `http.request`,
            request,
            {
                'http.method': method,
                'http.url': url,
                'http.target': new URL(url).pathname,
            }
        );
    }
}
```

### 5. Log Aggregation Setup

Implement centralized logging:

**Fluentd Configuration**
```yaml
# fluent.conf
<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/fluentd-containers.log.pos
  tag kubernetes.*
  <parse>
    @type json
    time_format %Y-%m-%dT%H:%M:%S.%NZ
  </parse>
</source>

# Add Kubernetes metadata
<filter kubernetes.**>
  @type kubernetes_metadata
  @id filter_kube_metadata
  kubernetes_url "#{ENV['FLUENT_FILTER_KUBERNETES_URL'] || 'https://' + ENV.fetch('KUBERNETES_SERVICE_HOST') + ':' + ENV.fetch('KUBERNETES_SERVICE_PORT') + '/api'}"
  verify_ssl "#{ENV['KUBERNETES_VERIFY_SSL'] || true}"
</filter>

# Parse application logs
<filter kubernetes.**>
  @type parser
  key_name log
  reserve_data true
  remove_key_name_field true
  <parse>
    @type multi_format
    <pattern>
      format json
    </pattern>
    <pattern>
      format regexp
      expression /^(?<severity>\w+)\s+\[(?<timestamp>[^\]]+)\]\s+(?<message>.*)$/
      time_format %Y-%m-%d %H:%M:%S
    </pattern>
  </parse>
</filter>

# Add fields
<filter kubernetes.**>
  @type record_transformer
  enable_ruby true
  <record>
    cluster_name ${ENV['CLUSTER_NAME']}
    environment ${ENV['ENVIRONMENT']}
    @timestamp ${time.strftime('%Y-%m-%dT%H:%M:%S.%LZ')}
  </record>
</filter>

# Output to Elasticsearch
<match kubernetes.**>
  @type elasticsearch
  @id out_es
  @log_level info
  include_tag_key true
  host "#{ENV['FLUENT_ELASTICSEARCH_HOST']}"
  port "#{ENV['FLUENT_ELASTICSEARCH_PORT']}"
  path "#{ENV['FLUENT_ELASTICSEARCH_PATH']}"
  scheme "#{ENV['FLUENT_ELASTICSEARCH_SCHEME'] || 'http'}"
  ssl_verify "#{ENV['FLUENT_ELASTICSEARCH_SSL_VERIFY'] || 'true'}"
  ssl_version "#{ENV['FLUENT_ELASTICSEARCH_SSL_VERSION'] || 'TLSv1_2'}"
  user "#{ENV['FLUENT_ELASTICSEARCH_USER']}"
  password "#{ENV['FLUENT_ELASTICSEARCH_PASSWORD']}"
  index_name logstash
  logstash_format true
  logstash_prefix "#{ENV['FLUENT_ELASTICSEARCH_LOGSTASH_PREFIX'] || 'logstash'}"
  <buffer>
    @type file
    path /var/log/fluentd-buffers/kubernetes.system.buffer
    flush_mode interval
    retry_type exponential_backoff
    flush_interval 5s
    retry_max_interval 30
    chunk_limit_size 2M
    queue_limit_length 8
    overflow_action block
  </buffer>
</match>
```

**Structured Logging Library**
```python
# structured_logging.py
import json
import logging
import traceback
from datetime import datetime
from typing import Any, Dict, Optional

class StructuredLogger:
    def __init__(self, name: str, service: str, version: str):
        self.logger = logging.getLogger(name)
        self.service = service
        self.version = version
        self.default_context = {
            'service': service,
            'version': version,
            'environment': os.getenv('ENVIRONMENT', 'development')
        }
    
    def _format_log(self, level: str, message: str, context: Dict[str, Any]) -> str:
        log_entry = {
            '@timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'message': message,
            **self.default_context,
            **context
        }
        
        # Add trace context if available
        trace_context = self._get_trace_context()
        if trace_context:
            log_entry['trace'] = trace_context
        
        return json.dumps(log_entry)
    
    def _get_trace_context(self) -> Optional[Dict[str, str]]:
        """Extract trace context from OpenTelemetry"""
        from opentelemetry import trace
        
        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            return {
                'trace_id': format(span_context.trace_id, '032x'),
                'span_id': format(span_context.span_id, '016x'),
            }
        return None
    
    def info(self, message: str, **context):
        log_msg = self._format_log('INFO', message, context)
        self.logger.info(log_msg)
    
    def error(self, message: str, error: Optional[Exception] = None, **context):
        if error:
            context['error'] = {
                'type': type(error).__name__,
                'message': str(error),
                'stacktrace': traceback.format_exc()
            }
        
        log_msg = self._format_log('ERROR', message, context)
        self.logger.error(log_msg)
    
    def warning(self, message: str, **context):
        log_msg = self._format_log('WARNING', message, context)
        self.logger.warning(log_msg)
    
    def debug(self, message: str, **context):
        log_msg = self._format_log('DEBUG', message, context)
        self.logger.debug(log_msg)
    
    def audit(self, action: str, user_id: str, details: Dict[str, Any]):
        """Special method for audit logging"""
        self.info(
            f"Audit: {action}",
            audit=True,
            user_id=user_id,
            action=action,
            details=details
        )

# Log correlation middleware
from flask import Flask, request, g
import uuid

def setup_request_logging(app: Flask, logger: StructuredLogger):
    @app.before_request
    def before_request():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        g.request_start = datetime.utcnow()
        
        logger.info(
            "Request started",
            request_id=g.request_id,
            method=request.method,
            path=request.path,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
    
    @app.after_request
    def after_request(response):
        duration = (datetime.utcnow() - g.request_start).total_seconds()
        
        logger.info(
            "Request completed",
            request_id=g.request_id,
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration=duration
        )
        
        response.headers['X-Request-ID'] = g.request_id
        return response
```

### 6. Alert Configuration

Set up intelligent alerting:

**Alert Rules**
```yaml
# alerts/application.yml
groups:
  - name: application
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)
          > 0.05
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.service }}"
          runbook_url: "https://wiki.company.com/runbooks/high-error-rate"
      
      # Slow response time
      - alert: SlowResponseTime
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
          ) > 1
        for: 10m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "Slow response time on {{ $labels.service }}"
          description: "95th percentile response time is {{ $value }}s"
      
      # Pod restart
      - alert: PodRestarting
        expr: |
          increase(kube_pod_container_status_restarts_total[1h]) > 5
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is restarting"
          description: "Pod has restarted {{ $value }} times in the last hour"

  - name: infrastructure
    interval: 30s
    rules:
      # High CPU usage
      - alert: HighCPUUsage
        expr: |
          avg(rate(container_cpu_usage_seconds_total[5m])) by (pod, namespace)
          > 0.8
        for: 15m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "High CPU usage on {{ $labels.pod }}"
          description: "CPU usage is {{ $value | humanizePercentage }}"
      
      # Memory pressure
      - alert: HighMemoryUsage
        expr: |
          container_memory_working_set_bytes
          / container_spec_memory_limit_bytes
          > 0.9
        for: 10m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "High memory usage on {{ $labels.pod }}"
          description: "Memory usage is {{ $value | humanizePercentage }} of limit"
      
      # Disk space
      - alert: DiskSpaceLow
        expr: |
          node_filesystem_avail_bytes{mountpoint="/"}
          / node_filesystem_size_bytes{mountpoint="/"}
          < 0.1
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"
```

**Alertmanager Configuration**
```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '$SLACK_API_URL'
  pagerduty_url: '$PAGERDUTY_URL'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  
  routes:
    # Critical alerts go to PagerDuty
    - match:
        severity: critical
      receiver: pagerduty
      continue: true
    
    # All alerts go to Slack
    - match_re:
        severity: critical|warning
      receiver: slack
    
    # Database alerts to DBA team
    - match:
        service: database
      receiver: dba-team

receivers:
  - name: 'default'
    
  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true
        actions:
          - type: button
            text: 'Runbook'
            url: '{{ .Annotations.runbook_url }}'
          - type: button
            text: 'Dashboard'
            url: 'https://grafana.company.com/d/{{ .Labels.service }}'
  
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '$PAGERDUTY_SERVICE_KEY'
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
        details:
          firing: '{{ .Alerts.Firing | len }}'
          resolved: '{{ .Alerts.Resolved | len }}'
          alerts: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

inhibit_rules:
  # Inhibit warning alerts if critical alert is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
```

### 7. SLO Implementation

Define and monitor Service Level Objectives:

**SLO Configuration**
```typescript
// slo-manager.ts
interface SLO {
    name: string;
    description: string;
    sli: {
        metric: string;
        threshold: number;
        comparison: 'lt' | 'gt' | 'eq';
    };
    target: number; // e.g., 99.9
    window: string; // e.g., '30d'
    burnRates: BurnRate[];
}

interface BurnRate {
    window: string;
    threshold: number;
    severity: 'warning' | 'critical';
}

export class SLOManager {
    private slos: SLO[] = [
        {
            name: 'API Availability',
            description: 'Percentage of successful requests',
            sli: {
                metric: 'http_requests_total{status_code!~"5.."}',
                threshold: 0,
                comparison: 'gt'
            },
            target: 99.9,
            window: '30d',
            burnRates: [
                { window: '1h', threshold: 14.4, severity: 'critical' },
                { window: '6h', threshold: 6, severity: 'critical' },
                { window: '1d', threshold: 3, severity: 'warning' },
                { window: '3d', threshold: 1, severity: 'warning' }
            ]
        },
        {
            name: 'API Latency',
            description: '95th percentile response time under 500ms',
            sli: {
                metric: 'http_request_duration_seconds',
                threshold: 0.5,
                comparison: 'lt'
            },
            target: 99,
            window: '30d',
            burnRates: [
                { window: '1h', threshold: 36, severity: 'critical' },
                { window: '6h', threshold: 12, severity: 'warning' }
            ]
        }
    ];
    
    generateSLOQueries(): string {
        return this.slos.map(slo => this.generateSLOQuery(slo)).join('\n\n');
    }
    
    private generateSLOQuery(slo: SLO): string {
        const errorBudget = 1 - (slo.target / 100);
        
        return `
# ${slo.name} SLO
- record: slo:${this.sanitizeName(slo.name)}:error_budget
  expr: ${errorBudget}

- record: slo:${this.sanitizeName(slo.name)}:consumed_error_budget
  expr: |
    1 - (
      sum(rate(${slo.sli.metric}[${slo.window}]))
      /
      sum(rate(http_requests_total[${slo.window}]))
    )

${slo.burnRates.map(burnRate => `
- alert: ${this.sanitizeName(slo.name)}BurnRate${burnRate.window}
  expr: |
    slo:${this.sanitizeName(slo.name)}:consumed_error_budget
    > ${burnRate.threshold} * slo:${this.sanitizeName(slo.name)}:error_budget
  labels:
    severity: ${burnRate.severity}
    slo: ${slo.name}
  annotations:
    summary: "${slo.name} SLO burn rate too high"
    description: "Burning through error budget ${burnRate.threshold}x faster than sustainable"
`).join('\n')}
        `;
    }
    
    private sanitizeName(name: string): string {
        return name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
    }
}
```

### 8. Monitoring Infrastructure as Code

Deploy monitoring stack with Terraform:

**Terraform Configuration**
```hcl
# monitoring.tf
module "prometheus" {
  source = "./modules/prometheus"
  
  namespace = "monitoring"
  storage_size = "100Gi"
  retention_days = 30
  
  external_labels = {
    cluster = var.cluster_name
    region  = var.region
  }
  
  scrape_configs = [
    {
      job_name = "kubernetes-pods"
      kubernetes_sd_configs = [{
        role = "pod"
      }]
    }
  ]
  
  alerting_rules = file("${path.module}/alerts/*.yml")
}

module "grafana" {
  source = "./modules/grafana"
  
  namespace = "monitoring"
  
  admin_password = var.grafana_admin_password
  
  datasources = [
    {
      name = "Prometheus"
      type = "prometheus"
      url  = "http://prometheus:9090"
    },
    {
      name = "Loki"
      type = "loki"
      url  = "http://loki:3100"
    },
    {
      name = "Jaeger"
      type = "jaeger"
      url  = "http://jaeger-query:16686"
    }
  ]
  
  dashboard_configs = [
    {
      name = "default"
      folder = "General"
      type = "file"
      options = {
        path = "/var/lib/grafana/dashboards"
      }
    }
  ]
}

module "loki" {
  source = "./modules/loki"
  
  namespace = "monitoring"
  storage_size = "50Gi"
  
  ingester_config = {
    chunk_idle_period = "15m"
    chunk_retain_period = "30s"
    max_chunk_age = "1h"
  }
}

module "alertmanager" {
  source = "./modules/alertmanager"
  
  namespace = "monitoring"
  
  config = templatefile("${path.module}/alertmanager.yml", {
    slack_webhook = var.slack_webhook
    pagerduty_key = var.pagerduty_service_key
  })
}
```

## Output Format

1. **Infrastructure Assessment**: Current monitoring capabilities analysis
2. **Monitoring Architecture**: Complete monitoring stack design
3. **Implementation Plan**: Step-by-step deployment guide
4. **Metric Definitions**: Comprehensive metrics catalog
5. **Dashboard Templates**: Ready-to-use Grafana dashboards
6. **Alert Runbooks**: Detailed alert response procedures
7. **SLO Definitions**: Service level objectives and error budgets
8. **Integration Guide**: Service instrumentation instructions

Focus on creating a monitoring system that provides actionable insights, reduces MTTR, and enables proactive issue detection.