# Configuration Validation

You are a configuration management expert specializing in validating, testing, and ensuring the correctness of application configurations. Create comprehensive validation schemas, implement configuration testing strategies, and ensure configurations are secure, consistent, and error-free across all environments.

## Context
The user needs to validate configuration files, implement configuration schemas, ensure consistency across environments, and prevent configuration-related errors. Focus on creating robust validation rules, type safety, security checks, and automated validation processes.

## Requirements
$ARGUMENTS

## Instructions

### 1. Configuration Analysis

Analyze existing configuration structure and identify validation needs:

**Configuration Scanner**
```python
import os
import yaml
import json
import toml
import configparser
from pathlib import Path
from typing import Dict, List, Any, Set

class ConfigurationAnalyzer:
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze project configuration files and patterns
        """
        analysis = {
            'config_files': self._find_config_files(project_path),
            'config_patterns': self._identify_patterns(project_path),
            'security_issues': self._check_security_issues(project_path),
            'consistency_issues': self._check_consistency(project_path),
            'validation_coverage': self._assess_validation(project_path),
            'recommendations': []
        }
        
        self._generate_recommendations(analysis)
        return analysis
    
    def _find_config_files(self, project_path: str) -> List[Dict]:
        """Find all configuration files in project"""
        config_patterns = [
            '**/*.json', '**/*.yaml', '**/*.yml', '**/*.toml',
            '**/*.ini', '**/*.conf', '**/*.config', '**/*.env*',
            '**/*.properties', '**/config.js', '**/config.ts'
        ]
        
        config_files = []
        for pattern in config_patterns:
            for file_path in Path(project_path).glob(pattern):
                if not self._should_ignore(file_path):
                    config_files.append({
                        'path': str(file_path),
                        'type': self._detect_config_type(file_path),
                        'size': file_path.stat().st_size,
                        'environment': self._detect_environment(file_path)
                    })
        
        return config_files
    
    def _check_security_issues(self, project_path: str) -> List[Dict]:
        """Check for security issues in configurations"""
        issues = []
        
        # Patterns that might indicate secrets
        secret_patterns = [
            r'(api[_-]?key|apikey)',
            r'(secret|password|passwd|pwd)',
            r'(token|auth)',
            r'(private[_-]?key)',
            r'(aws[_-]?access|aws[_-]?secret)',
            r'(database[_-]?url|db[_-]?connection)'
        ]
        
        for config_file in self._find_config_files(project_path):
            content = Path(config_file['path']).read_text()
            
            for pattern in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    # Check if it's a placeholder or actual secret
                    if self._looks_like_real_secret(content, pattern):
                        issues.append({
                            'file': config_file['path'],
                            'type': 'potential_secret',
                            'pattern': pattern,
                            'severity': 'high'
                        })
        
        return issues
    
    def _check_consistency(self, project_path: str) -> List[Dict]:
        """Check configuration consistency across environments"""
        inconsistencies = []
        
        # Group configs by base name
        config_groups = defaultdict(list)
        for config in self._find_config_files(project_path):
            base_name = self._get_base_config_name(config['path'])
            config_groups[base_name].append(config)
        
        # Check each group for inconsistencies
        for base_name, configs in config_groups.items():
            if len(configs) > 1:
                keys_by_env = {}
                for config in configs:
                    env = config.get('environment', 'default')
                    keys = self._extract_config_keys(config['path'])
                    keys_by_env[env] = keys
                
                # Find missing keys
                all_keys = set()
                for keys in keys_by_env.values():
                    all_keys.update(keys)
                
                for env, keys in keys_by_env.items():
                    missing = all_keys - keys
                    if missing:
                        inconsistencies.append({
                            'config_group': base_name,
                            'environment': env,
                            'missing_keys': list(missing),
                            'severity': 'medium'
                        })
        
        return inconsistencies
```

### 2. Schema Definition and Validation

Implement configuration schema validation:

**JSON Schema Validator**
```typescript
// config-validator.ts
import Ajv from 'ajv';
import ajvFormats from 'ajv-formats';
import ajvKeywords from 'ajv-keywords';
import { JSONSchema7 } from 'json-schema';

interface ValidationResult {
  valid: boolean;
  errors?: Array<{
    path: string;
    message: string;
    keyword: string;
    params: any;
  }>;
}

export class ConfigValidator {
  private ajv: Ajv;
  private schemas: Map<string, JSONSchema7> = new Map();
  
  constructor() {
    this.ajv = new Ajv({
      allErrors: true,
      verbose: true,
      strict: false,
      coerceTypes: true
    });
    
    // Add formats support
    ajvFormats(this.ajv);
    ajvKeywords(this.ajv);
    
    // Add custom formats
    this.addCustomFormats();
  }
  
  private addCustomFormats() {
    // URL format with protocol validation
    this.ajv.addFormat('url-https', {
      type: 'string',
      validate: (data: string) => {
        try {
          const url = new URL(data);
          return url.protocol === 'https:';
        } catch {
          return false;
        }
      }
    });
    
    // Environment variable reference
    this.ajv.addFormat('env-var', {
      type: 'string',
      validate: /^\$\{[A-Z_][A-Z0-9_]*\}$/
    });
    
    // Semantic version
    this.ajv.addFormat('semver', {
      type: 'string',
      validate: /^\d+\.\d+\.\d+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$/
    });
    
    // Port number
    this.ajv.addFormat('port', {
      type: 'number',
      validate: (data: number) => data >= 1 && data <= 65535
    });
    
    // Duration format (e.g., "5m", "1h", "30s")
    this.ajv.addFormat('duration', {
      type: 'string',
      validate: /^\d+[smhd]$/
    });
  }
  
  registerSchema(name: string, schema: JSONSchema7): void {
    this.schemas.set(name, schema);
    this.ajv.addSchema(schema, name);
  }
  
  validate(configData: any, schemaName: string): ValidationResult {
    const validate = this.ajv.getSchema(schemaName);
    
    if (!validate) {
      throw new Error(`Schema '${schemaName}' not found`);
    }
    
    const valid = validate(configData);
    
    if (!valid && validate.errors) {
      return {
        valid: false,
        errors: validate.errors.map(error => ({
          path: error.instancePath || '/',
          message: error.message || 'Validation error',
          keyword: error.keyword,
          params: error.params
        }))
      };
    }
    
    return { valid: true };
  }
  
  generateSchema(sampleConfig: any): JSONSchema7 {
    // Auto-generate schema from sample configuration
    const schema: JSONSchema7 = {
      type: 'object',
      properties: {},
      required: []
    };
    
    for (const [key, value] of Object.entries(sampleConfig)) {
      schema.properties![key] = this.inferSchema(value);
      
      // Make all top-level properties required by default
      if (schema.required && !key.startsWith('optional_')) {
        schema.required.push(key);
      }
    }
    
    return schema;
  }
  
  private inferSchema(value: any): JSONSchema7 {
    if (value === null) {
      return { type: 'null' };
    }
    
    if (Array.isArray(value)) {
      return {
        type: 'array',
        items: value.length > 0 ? this.inferSchema(value[0]) : {}
      };
    }
    
    if (typeof value === 'object') {
      const properties: Record<string, JSONSchema7> = {};
      const required: string[] = [];
      
      for (const [k, v] of Object.entries(value)) {
        properties[k] = this.inferSchema(v);
        if (v !== null && v !== undefined) {
          required.push(k);
        }
      }
      
      return {
        type: 'object',
        properties,
        required
      };
    }
    
    // Infer format from value patterns
    if (typeof value === 'string') {
      if (value.match(/^https?:\/\//)) {
        return { type: 'string', format: 'uri' };
      }
      if (value.match(/^\d{4}-\d{2}-\d{2}$/)) {
        return { type: 'string', format: 'date' };
      }
      if (value.match(/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i)) {
        return { type: 'string', format: 'uuid' };
      }
    }
    
    return { type: typeof value as JSONSchema7['type'] };
  }
}

// Example schemas
export const schemas = {
  database: {
    type: 'object',
    properties: {
      host: { type: 'string', format: 'hostname' },
      port: { type: 'integer', format: 'port' },
      database: { type: 'string', minLength: 1 },
      user: { type: 'string', minLength: 1 },
      password: { type: 'string', minLength: 8 },
      ssl: {
        type: 'object',
        properties: {
          enabled: { type: 'boolean' },
          ca: { type: 'string' },
          cert: { type: 'string' },
          key: { type: 'string' }
        },
        required: ['enabled']
      },
      pool: {
        type: 'object',
        properties: {
          min: { type: 'integer', minimum: 0 },
          max: { type: 'integer', minimum: 1 },
          idleTimeout: { type: 'string', format: 'duration' }
        }
      }
    },
    required: ['host', 'port', 'database', 'user', 'password'],
    additionalProperties: false
  },
  
  api: {
    type: 'object',
    properties: {
      server: {
        type: 'object',
        properties: {
          host: { type: 'string', default: '0.0.0.0' },
          port: { type: 'integer', format: 'port', default: 3000 },
          cors: {
            type: 'object',
            properties: {
              enabled: { type: 'boolean' },
              origins: {
                type: 'array',
                items: { type: 'string', format: 'uri' }
              },
              credentials: { type: 'boolean' }
            }
          }
        },
        required: ['port']
      },
      auth: {
        type: 'object',
        properties: {
          jwt: {
            type: 'object',
            properties: {
              secret: { type: 'string', minLength: 32 },
              expiresIn: { type: 'string', format: 'duration' },
              algorithm: {
                type: 'string',
                enum: ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512']
              }
            },
            required: ['secret', 'expiresIn']
          }
        }
      },
      rateLimit: {
        type: 'object',
        properties: {
          windowMs: { type: 'integer', minimum: 1000 },
          max: { type: 'integer', minimum: 1 },
          message: { type: 'string' }
        }
      }
    },
    required: ['server', 'auth']
  }
};
```

### 3. Environment-Specific Validation

Validate configurations across environments:

**Environment Validator**
```python
# environment_validator.py
from typing import Dict, List, Set, Any
import os
import re

class EnvironmentValidator:
    def __init__(self):
        self.environments = ['development', 'staging', 'production']
        self.environment_rules = self._define_environment_rules()
    
    def _define_environment_rules(self) -> Dict[str, Dict]:
        """Define environment-specific validation rules"""
        return {
            'development': {
                'allow_debug': True,
                'require_https': False,
                'allow_wildcards': True,
                'min_password_length': 8,
                'allowed_log_levels': ['debug', 'info', 'warn', 'error']
            },
            'staging': {
                'allow_debug': True,
                'require_https': True,
                'allow_wildcards': False,
                'min_password_length': 12,
                'allowed_log_levels': ['info', 'warn', 'error']
            },
            'production': {
                'allow_debug': False,
                'require_https': True,
                'allow_wildcards': False,
                'min_password_length': 16,
                'allowed_log_levels': ['warn', 'error'],
                'require_encryption': True,
                'require_backup': True
            }
        }
    
    def validate_config(self, config: Dict, environment: str) -> List[Dict]:
        """Validate configuration for specific environment"""
        if environment not in self.environment_rules:
            raise ValueError(f"Unknown environment: {environment}")
        
        rules = self.environment_rules[environment]
        violations = []
        
        # Check debug settings
        if not rules['allow_debug'] and config.get('debug', False):
            violations.append({
                'rule': 'no_debug_in_production',
                'message': 'Debug mode is not allowed in production',
                'severity': 'critical',
                'path': 'debug'
            })
        
        # Check HTTPS requirements
        if rules['require_https']:
            urls = self._extract_urls(config)
            for url_path, url in urls:
                if url.startswith('http://') and 'localhost' not in url:
                    violations.append({
                        'rule': 'require_https',
                        'message': f'HTTPS required for {url_path}',
                        'severity': 'high',
                        'path': url_path,
                        'value': url
                    })
        
        # Check log levels
        log_level = config.get('logging', {}).get('level')
        if log_level and log_level not in rules['allowed_log_levels']:
            violations.append({
                'rule': 'invalid_log_level',
                'message': f"Log level '{log_level}' not allowed in {environment}",
                'severity': 'medium',
                'path': 'logging.level',
                'allowed': rules['allowed_log_levels']
            })
        
        # Check production-specific requirements
        if environment == 'production':
            violations.extend(self._validate_production_requirements(config))
        
        return violations
    
    def _validate_production_requirements(self, config: Dict) -> List[Dict]:
        """Additional validation for production environment"""
        violations = []
        
        # Check encryption settings
        if not config.get('security', {}).get('encryption', {}).get('enabled'):
            violations.append({
                'rule': 'encryption_required',
                'message': 'Encryption must be enabled in production',
                'severity': 'critical',
                'path': 'security.encryption.enabled'
            })
        
        # Check backup configuration
        if not config.get('backup', {}).get('enabled'):
            violations.append({
                'rule': 'backup_required',
                'message': 'Backup must be configured for production',
                'severity': 'high',
                'path': 'backup.enabled'
            })
        
        # Check monitoring
        if not config.get('monitoring', {}).get('enabled'):
            violations.append({
                'rule': 'monitoring_required',
                'message': 'Monitoring must be enabled in production',
                'severity': 'high',
                'path': 'monitoring.enabled'
            })
        
        return violations
    
    def _extract_urls(self, obj: Any, path: str = '') -> List[tuple]:
        """Recursively extract URLs from configuration"""
        urls = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                urls.extend(self._extract_urls(value, new_path))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                urls.extend(self._extract_urls(item, new_path))
        elif isinstance(obj, str) and re.match(r'^https?://', obj):
            urls.append((path, obj))
        
        return urls

# Cross-environment consistency checker
class ConsistencyChecker:
    def check_consistency(self, configs: Dict[str, Dict]) -> List[Dict]:
        """Check configuration consistency across environments"""
        issues = []
        
        # Get all unique keys across environments
        all_keys = set()
        env_keys = {}
        
        for env, config in configs.items():
            keys = self._flatten_keys(config)
            env_keys[env] = keys
            all_keys.update(keys)
        
        # Check for missing keys
        for env, keys in env_keys.items():
            missing_keys = all_keys - keys
            if missing_keys:
                issues.append({
                    'type': 'missing_keys',
                    'environment': env,
                    'keys': list(missing_keys),
                    'severity': 'medium'
                })
        
        # Check for type inconsistencies
        for key in all_keys:
            types_by_env = {}
            for env, config in configs.items():
                value = self._get_nested_value(config, key)
                if value is not None:
                    types_by_env[env] = type(value).__name__
            
            unique_types = set(types_by_env.values())
            if len(unique_types) > 1:
                issues.append({
                    'type': 'type_mismatch',
                    'key': key,
                    'types': types_by_env,
                    'severity': 'high'
                })
        
        return issues
```

### 4. Configuration Testing Framework

Implement configuration testing:

**Config Test Suite**
```typescript
// config-test.ts
import { describe, it, expect, beforeEach } from '@jest/globals';
import { ConfigValidator } from './config-validator';
import { loadConfig } from './config-loader';

interface ConfigTestCase {
  name: string;
  config: any;
  environment: string;
  expectedValid: boolean;
  expectedErrors?: string[];
}

export class ConfigTestSuite {
  private validator: ConfigValidator;
  
  constructor() {
    this.validator = new ConfigValidator();
  }
  
  async runTests(testCases: ConfigTestCase[]): Promise<TestResults> {
    const results: TestResults = {
      passed: 0,
      failed: 0,
      errors: []
    };
    
    for (const testCase of testCases) {
      try {
        const result = await this.runTestCase(testCase);
        if (result.passed) {
          results.passed++;
        } else {
          results.failed++;
          results.errors.push({
            testName: testCase.name,
            errors: result.errors
          });
        }
      } catch (error) {
        results.failed++;
        results.errors.push({
          testName: testCase.name,
          errors: [error.message]
        });
      }
    }
    
    return results;
  }
  
  private async runTestCase(testCase: ConfigTestCase): Promise<TestResult> {
    // Load and validate config
    const validationResult = this.validator.validate(
      testCase.config,
      testCase.environment
    );
    
    const result: TestResult = {
      passed: validationResult.valid === testCase.expectedValid,
      errors: []
    };
    
    // Check expected errors
    if (testCase.expectedErrors && validationResult.errors) {
      for (const expectedError of testCase.expectedErrors) {
        const found = validationResult.errors.some(
          error => error.message.includes(expectedError)
        );
        
        if (!found) {
          result.passed = false;
          result.errors.push(`Expected error not found: ${expectedError}`);
        }
      }
    }
    
    return result;
  }
}

// Jest test examples
describe('Configuration Validation', () => {
  let validator: ConfigValidator;
  
  beforeEach(() => {
    validator = new ConfigValidator();
  });
  
  describe('Database Configuration', () => {
    it('should validate valid database config', () => {
      const config = {
        host: 'localhost',
        port: 5432,
        database: 'myapp',
        user: 'dbuser',
        password: 'securepassword123'
      };
      
      const result = validator.validate(config, 'database');
      expect(result.valid).toBe(true);
    });
    
    it('should reject invalid port number', () => {
      const config = {
        host: 'localhost',
        port: 70000, // Invalid port
        database: 'myapp',
        user: 'dbuser',
        password: 'securepassword123'
      };
      
      const result = validator.validate(config, 'database');
      expect(result.valid).toBe(false);
      expect(result.errors?.[0].path).toBe('/port');
    });
    
    it('should require SSL in production', () => {
      const config = {
        host: 'prod-db.example.com',
        port: 5432,
        database: 'myapp',
        user: 'dbuser',
        password: 'securepassword123',
        ssl: { enabled: false }
      };
      
      const envValidator = new EnvironmentValidator();
      const violations = envValidator.validate_config(config, 'production');
      
      expect(violations).toContainEqual(
        expect.objectContaining({
          rule: 'ssl_required_in_production'
        })
      );
    });
  });
  
  describe('API Configuration', () => {
    it('should validate CORS settings', () => {
      const config = {
        server: {
          port: 3000,
          cors: {
            enabled: true,
            origins: ['https://example.com', 'https://app.example.com'],
            credentials: true
          }
        },
        auth: {
          jwt: {
            secret: 'a'.repeat(32),
            expiresIn: '1h',
            algorithm: 'HS256'
          }
        }
      };
      
      const result = validator.validate(config, 'api');
      expect(result.valid).toBe(true);
    });
    
    it('should reject short JWT secrets', () => {
      const config = {
        server: { port: 3000 },
        auth: {
          jwt: {
            secret: 'tooshort',
            expiresIn: '1h'
          }
        }
      };
      
      const result = validator.validate(config, 'api');
      expect(result.valid).toBe(false);
      expect(result.errors?.[0].path).toBe('/auth/jwt/secret');
    });
  });
});
```

### 5. Runtime Configuration Validation

Implement runtime validation and hot-reloading:

**Runtime Config Validator**
```typescript
// runtime-validator.ts
import { EventEmitter } from 'events';
import * as chokidar from 'chokidar';
import { ConfigValidator } from './config-validator';

export class RuntimeConfigValidator extends EventEmitter {
  private validator: ConfigValidator;
  private currentConfig: any;
  private watchers: Map<string, chokidar.FSWatcher> = new Map();
  private validationCache: Map<string, ValidationResult> = new Map();
  
  constructor() {
    super();
    this.validator = new ConfigValidator();
  }
  
  async initialize(configPath: string): Promise<void> {
    // Load initial config
    this.currentConfig = await this.loadAndValidate(configPath);
    
    // Setup file watcher for hot-reloading
    this.watchConfig(configPath);
  }
  
  private async loadAndValidate(configPath: string): Promise<any> {
    try {
      // Load config
      const config = await this.loadConfig(configPath);
      
      // Validate config
      const validationResult = this.validator.validate(
        config,
        this.detectEnvironment()
      );
      
      if (!validationResult.valid) {
        this.emit('validation:error', {
          path: configPath,
          errors: validationResult.errors
        });
        
        // In development, log errors but continue
        if (this.isDevelopment()) {
          console.error('Configuration validation errors:', validationResult.errors);
          return config;
        }
        
        // In production, throw error
        throw new ConfigValidationError(
          'Configuration validation failed',
          validationResult.errors
        );
      }
      
      this.emit('validation:success', { path: configPath });
      return config;
    } catch (error) {
      this.emit('validation:error', { path: configPath, error });
      throw error;
    }
  }
  
  private watchConfig(configPath: string): void {
    const watcher = chokidar.watch(configPath, {
      persistent: true,
      ignoreInitial: true
    });
    
    watcher.on('change', async () => {
      console.log(`Configuration file changed: ${configPath}`);
      
      try {
        const newConfig = await this.loadAndValidate(configPath);
        
        // Check if config actually changed
        if (JSON.stringify(newConfig) !== JSON.stringify(this.currentConfig)) {
          const oldConfig = this.currentConfig;
          this.currentConfig = newConfig;
          
          this.emit('config:changed', {
            oldConfig,
            newConfig,
            changedKeys: this.findChangedKeys(oldConfig, newConfig)
          });
        }
      } catch (error) {
        this.emit('config:error', { error });
      }
    });
    
    this.watchers.set(configPath, watcher);
  }
  
  private findChangedKeys(oldConfig: any, newConfig: any): string[] {
    const changed: string[] = [];
    
    const findDiff = (old: any, new_: any, path: string = '') => {
      // Check all keys in old config
      for (const key in old) {
        const currentPath = path ? `${path}.${key}` : key;
        
        if (!(key in new_)) {
          changed.push(`${currentPath} (removed)`);
        } else if (typeof old[key] === 'object' && typeof new_[key] === 'object') {
          findDiff(old[key], new_[key], currentPath);
        } else if (old[key] !== new_[key]) {
          changed.push(currentPath);
        }
      }
      
      // Check for new keys
      for (const key in new_) {
        if (!(key in old)) {
          const currentPath = path ? `${path}.${key}` : key;
          changed.push(`${currentPath} (added)`);
        }
      }
    };
    
    findDiff(oldConfig, newConfig);
    return changed;
  }
  
  validateValue(path: string, value: any): ValidationResult {
    // Use cached schema for performance
    const cacheKey = `${path}:${JSON.stringify(value)}`;
    if (this.validationCache.has(cacheKey)) {
      return this.validationCache.get(cacheKey)!;
    }
    
    // Extract schema for specific path
    const schema = this.getSchemaForPath(path);
    if (!schema) {
      return { valid: true }; // No schema defined for this path
    }
    
    const result = this.validator.validateValue(value, schema);
    this.validationCache.set(cacheKey, result);
    
    return result;
  }
  
  async shutdown(): Promise<void> {
    // Close all watchers
    for (const watcher of this.watchers.values()) {
      await watcher.close();
    }
    
    this.watchers.clear();
    this.validationCache.clear();
  }
}

// Type-safe configuration access
export class TypedConfig<T> {
  constructor(
    private config: T,
    private validator: RuntimeConfigValidator
  ) {}
  
  get<K extends keyof T>(key: K): T[K] {
    const value = this.config[key];
    
    // Validate on access in development
    if (process.env.NODE_ENV === 'development') {
      const result = this.validator.validateValue(String(key), value);
      if (!result.valid) {
        console.warn(`Invalid config value for ${String(key)}:`, result.errors);
      }
    }
    
    return value;
  }
  
  getOrDefault<K extends keyof T>(key: K, defaultValue: T[K]): T[K] {
    return this.config[key] ?? defaultValue;
  }
  
  require<K extends keyof T>(key: K): NonNullable<T[K]> {
    const value = this.config[key];
    
    if (value === null || value === undefined) {
      throw new Error(`Required configuration '${String(key)}' is missing`);
    }
    
    return value as NonNullable<T[K]>;
  }
}
```

### 6. Configuration Migration

Implement configuration migration and versioning:

**Config Migration System**
```python
# config_migration.py
from typing import Dict, List, Callable, Any
from abc import ABC, abstractmethod
import semver

class ConfigMigration(ABC):
    """Base class for configuration migrations"""
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Target version for this migration"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this migration does"""
        pass
    
    @abstractmethod
    def up(self, config: Dict) -> Dict:
        """Apply migration to config"""
        pass
    
    @abstractmethod
    def down(self, config: Dict) -> Dict:
        """Revert migration from config"""
        pass
    
    def validate(self, config: Dict) -> bool:
        """Validate config after migration"""
        return True

class ConfigMigrator:
    def __init__(self):
        self.migrations: List[ConfigMigration] = []
    
    def register_migration(self, migration: ConfigMigration):
        """Register a migration"""
        self.migrations.append(migration)
        # Sort by version
        self.migrations.sort(key=lambda m: semver.VersionInfo.parse(m.version))
    
    def migrate(self, config: Dict, target_version: str) -> Dict:
        """Migrate config to target version"""
        current_version = config.get('_version', '0.0.0')
        
        if semver.compare(current_version, target_version) == 0:
            return config  # Already at target version
        
        if semver.compare(current_version, target_version) > 0:
            # Downgrade
            return self._downgrade(config, current_version, target_version)
        else:
            # Upgrade
            return self._upgrade(config, current_version, target_version)
    
    def _upgrade(self, config: Dict, from_version: str, to_version: str) -> Dict:
        """Upgrade config from one version to another"""
        result = config.copy()
        
        for migration in self.migrations:
            if (semver.compare(migration.version, from_version) > 0 and
                semver.compare(migration.version, to_version) <= 0):
                
                print(f"Applying migration to v{migration.version}: {migration.description}")
                result = migration.up(result)
                
                if not migration.validate(result):
                    raise ValueError(f"Migration to v{migration.version} failed validation")
                
                result['_version'] = migration.version
        
        return result
    
    def _downgrade(self, config: Dict, from_version: str, to_version: str) -> Dict:
        """Downgrade config from one version to another"""
        result = config.copy()
        
        # Apply migrations in reverse order
        for migration in reversed(self.migrations):
            if (semver.compare(migration.version, to_version) > 0 and
                semver.compare(migration.version, from_version) <= 0):
                
                print(f"Reverting migration from v{migration.version}: {migration.description}")
                result = migration.down(result)
                
                # Update version to previous migration's version
                prev_version = self._get_previous_version(migration.version)
                result['_version'] = prev_version
        
        return result
    
    def _get_previous_version(self, version: str) -> str:
        """Get the version before the given version"""
        for i, migration in enumerate(self.migrations):
            if migration.version == version:
                return self.migrations[i-1].version if i > 0 else '0.0.0'
        return '0.0.0'

# Example migrations
class MigrationV1_0_0(ConfigMigration):
    @property
    def version(self) -> str:
        return '1.0.0'
    
    @property
    def description(self) -> str:
        return 'Initial configuration structure'
    
    def up(self, config: Dict) -> Dict:
        # Add default structure
        return {
            '_version': '1.0.0',
            'app': config.get('app', {}),
            'database': config.get('database', {}),
            'logging': config.get('logging', {'level': 'info'})
        }
    
    def down(self, config: Dict) -> Dict:
        # Remove version info
        result = config.copy()
        result.pop('_version', None)
        return result

class MigrationV1_1_0(ConfigMigration):
    @property
    def version(self) -> str:
        return '1.1.0'
    
    @property
    def description(self) -> str:
        return 'Split database config into read/write connections'
    
    def up(self, config: Dict) -> Dict:
        result = config.copy()
        
        # Transform single database config to read/write split
        if 'database' in result and not isinstance(result['database'], dict):
            old_db = result['database']
            result['database'] = {
                'write': old_db,
                'read': old_db.copy()  # Same as write initially
            }
        
        return result
    
    def down(self, config: Dict) -> Dict:
        result = config.copy()
        
        # Revert to single database config
        if 'database' in result and 'write' in result['database']:
            result['database'] = result['database']['write']
        
        return result

class MigrationV2_0_0(ConfigMigration):
    @property
    def version(self) -> str:
        return '2.0.0'
    
    @property
    def description(self) -> str:
        return 'Add security configuration section'
    
    def up(self, config: Dict) -> Dict:
        result = config.copy()
        
        # Add security section with defaults
        if 'security' not in result:
            result['security'] = {
                'encryption': {
                    'enabled': True,
                    'algorithm': 'AES-256-GCM'
                },
                'tls': {
                    'minVersion': '1.2',
                    'ciphers': ['TLS_AES_256_GCM_SHA384', 'TLS_AES_128_GCM_SHA256']
                }
            }
        
        return result
    
    def down(self, config: Dict) -> Dict:
        result = config.copy()
        result.pop('security', None)
        return result
```

### 7. Configuration Security

Implement secure configuration handling:

**Secure Config Manager**
```typescript
// secure-config.ts
import * as crypto from 'crypto';
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';
import { KeyVaultSecret, SecretClient } from '@azure/keyvault-secrets';

interface EncryptedValue {
  encrypted: true;
  value: string;
  algorithm: string;
  iv: string;
  authTag?: string;
}

export class SecureConfigManager {
  private secretsCache: Map<string, any> = new Map();
  private encryptionKey: Buffer;
  
  constructor(private options: SecureConfigOptions) {
    this.encryptionKey = this.deriveKey(options.masterKey);
  }
  
  private deriveKey(masterKey: string): Buffer {
    return crypto.pbkdf2Sync(masterKey, 'config-salt', 100000, 32, 'sha256');
  }
  
  encrypt(value: any): EncryptedValue {
    const algorithm = 'aes-256-gcm';
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(algorithm, this.encryptionKey, iv);
    
    const stringValue = JSON.stringify(value);
    let encrypted = cipher.update(stringValue, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return {
      encrypted: true,
      value: encrypted,
      algorithm,
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex')
    };
  }
  
  decrypt(encryptedValue: EncryptedValue): any {
    const decipher = crypto.createDecipheriv(
      encryptedValue.algorithm,
      this.encryptionKey,
      Buffer.from(encryptedValue.iv, 'hex')
    );
    
    if (encryptedValue.authTag) {
      decipher.setAuthTag(Buffer.from(encryptedValue.authTag, 'hex'));
    }
    
    let decrypted = decipher.update(encryptedValue.value, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return JSON.parse(decrypted);
  }
  
  async processConfig(config: any): Promise<any> {
    const processed = {};
    
    for (const [key, value] of Object.entries(config)) {
      if (this.isEncryptedValue(value)) {
        // Decrypt encrypted values
        processed[key] = this.decrypt(value as EncryptedValue);
      } else if (this.isSecretReference(value)) {
        // Fetch from secret manager
        processed[key] = await this.fetchSecret(value as string);
      } else if (typeof value === 'object' && value !== null) {
        // Recursively process nested objects
        processed[key] = await this.processConfig(value);
      } else {
        processed[key] = value;
      }
    }
    
    return processed;
  }
  
  private isEncryptedValue(value: any): boolean {
    return typeof value === 'object' && 
           value !== null && 
           value.encrypted === true;
  }
  
  private isSecretReference(value: any): boolean {
    return typeof value === 'string' && 
           (value.startsWith('secret://') || 
            value.startsWith('vault://') ||
            value.startsWith('aws-secret://'));
  }
  
  private async fetchSecret(reference: string): Promise<any> {
    // Check cache first
    if (this.secretsCache.has(reference)) {
      return this.secretsCache.get(reference);
    }
    
    let secretValue: any;
    
    if (reference.startsWith('secret://')) {
      // Google Secret Manager
      secretValue = await this.fetchGoogleSecret(reference);
    } else if (reference.startsWith('vault://')) {
      // Azure Key Vault
      secretValue = await this.fetchAzureSecret(reference);
    } else if (reference.startsWith('aws-secret://')) {
      // AWS Secrets Manager
      secretValue = await this.fetchAWSSecret(reference);
    }
    
    // Cache the secret
    this.secretsCache.set(reference, secretValue);
    
    return secretValue;
  }
  
  private async fetchGoogleSecret(reference: string): Promise<any> {
    const secretName = reference.replace('secret://', '');
    const client = new SecretManagerServiceClient();
    
    const [version] = await client.accessSecretVersion({
      name: `projects/${this.options.gcpProject}/secrets/${secretName}/versions/latest`
    });
    
    const payload = version.payload?.data;
    if (!payload) {
      throw new Error(`Secret ${secretName} has no payload`);
    }
    
    return JSON.parse(payload.toString());
  }
  
  validateSecureConfig(config: any): ValidationResult {
    const errors: string[] = [];
    
    const checkSecrets = (obj: any, path: string = '') => {
      for (const [key, value] of Object.entries(obj)) {
        const currentPath = path ? `${path}.${key}` : key;
        
        // Check for plaintext secrets
        if (this.looksLikeSecret(key) && typeof value === 'string') {
          if (!this.isEncryptedValue(value) && !this.isSecretReference(value)) {
            errors.push(`Potential plaintext secret at ${currentPath}`);
          }
        }
        
        // Recursively check nested objects
        if (typeof value === 'object' && value !== null && !this.isEncryptedValue(value)) {
          checkSecrets(value, currentPath);
        }
      }
    };
    
    checkSecrets(config);
    
    return {
      valid: errors.length === 0,
      errors: errors.map(message => ({
        path: '',
        message,
        keyword: 'security',
        params: {}
      }))
    };
  }
  
  private looksLikeSecret(key: string): boolean {
    const secretPatterns = [
      'password', 'secret', 'key', 'token', 'credential',
      'api_key', 'apikey', 'private_key', 'auth'
    ];
    
    const lowerKey = key.toLowerCase();
    return secretPatterns.some(pattern => lowerKey.includes(pattern));
  }
}
```

### 8. Configuration Documentation

Generate configuration documentation:

**Config Documentation Generator**
```python
# config_docs_generator.py
from typing import Dict, List, Any
import json
import yaml

class ConfigDocGenerator:
    def generate_docs(self, schema: Dict, examples: Dict) -> str:
        """Generate comprehensive configuration documentation"""
        docs = ["# Configuration Reference\n"]
        
        # Add overview
        docs.append("## Overview\n")
        docs.append("This document describes all available configuration options.\n")
        
        # Add table of contents
        docs.append("## Table of Contents\n")
        toc = self._generate_toc(schema.get('properties', {}))
        docs.extend(toc)
        
        # Add configuration sections
        docs.append("\n## Configuration Options\n")
        sections = self._generate_sections(schema.get('properties', {}), examples)
        docs.extend(sections)
        
        # Add examples
        docs.append("\n## Complete Examples\n")
        docs.extend(self._generate_examples(examples))
        
        # Add validation rules
        docs.append("\n## Validation Rules\n")
        docs.extend(self._generate_validation_rules(schema))
        
        return '\n'.join(docs)
    
    def _generate_sections(self, properties: Dict, examples: Dict, level: int = 3) -> List[str]:
        """Generate documentation for each configuration section"""
        sections = []
        
        for prop_name, prop_schema in properties.items():
            # Section header
            sections.append(f"{'#' * level} {prop_name}\n")
            
            # Description
            if 'description' in prop_schema:
                sections.append(f"{prop_schema['description']}\n")
            
            # Type information
            sections.append(f"**Type:** `{prop_schema.get('type', 'any')}`\n")
            
            # Required
            if prop_name in prop_schema.get('required', []):
                sections.append("**Required:** Yes\n")
            
            # Default value
            if 'default' in prop_schema:
                sections.append(f"**Default:** `{json.dumps(prop_schema['default'])}`\n")
            
            # Validation constraints
            constraints = self._extract_constraints(prop_schema)
            if constraints:
                sections.append("**Constraints:**")
                for constraint in constraints:
                    sections.append(f"- {constraint}")
                sections.append("")
            
            # Example
            if prop_name in examples:
                sections.append("**Example:**")
                sections.append("```yaml")
                sections.append(yaml.dump({prop_name: examples[prop_name]}, default_flow_style=False))
                sections.append("```\n")
            
            # Nested properties
            if prop_schema.get('type') == 'object' and 'properties' in prop_schema:
                nested = self._generate_sections(
                    prop_schema['properties'],
                    examples.get(prop_name, {}),
                    level + 1
                )
                sections.extend(nested)
        
        return sections
    
    def _extract_constraints(self, schema: Dict) -> List[str]:
        """Extract validation constraints from schema"""
        constraints = []
        
        if 'enum' in schema:
            constraints.append(f"Must be one of: {', '.join(map(str, schema['enum']))}")
        
        if 'minimum' in schema:
            constraints.append(f"Minimum value: {schema['minimum']}")
        
        if 'maximum' in schema:
            constraints.append(f"Maximum value: {schema['maximum']}")
        
        if 'minLength' in schema:
            constraints.append(f"Minimum length: {schema['minLength']}")
        
        if 'maxLength' in schema:
            constraints.append(f"Maximum length: {schema['maxLength']}")
        
        if 'pattern' in schema:
            constraints.append(f"Must match pattern: `{schema['pattern']}`")
        
        if 'format' in schema:
            constraints.append(f"Format: {schema['format']}")
        
        return constraints

# Generate interactive config builder
class InteractiveConfigBuilder:
    def generate_html_builder(self, schema: Dict) -> str:
        """Generate interactive HTML configuration builder"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Configuration Builder</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .config-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        .config-field { margin: 10px 0; }
        label { display: inline-block; width: 200px; font-weight: bold; }
        input, select { width: 300px; padding: 5px; }
        .error { color: red; font-size: 12px; }
        .preview { background: #f5f5f5; padding: 20px; margin-top: 20px; }
        pre { background: white; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Configuration Builder</h1>
    <div id="config-form"></div>
    <button onclick="validateConfig()">Validate</button>
    <button onclick="exportConfig()">Export</button>
    
    <div class="preview">
        <h2>Preview</h2>
        <pre id="config-preview"></pre>
    </div>
    
    <script>
        const schema = """ + json.dumps(schema) + """;
        
        function buildForm() {
            const container = document.getElementById('config-form');
            container.innerHTML = renderSchema(schema.properties);
        }
        
        function renderSchema(properties, prefix = '') {
            let html = '';
            
            for (const [key, prop] of Object.entries(properties)) {
                const fieldId = prefix ? `${prefix}.${key}` : key;
                
                html += '<div class="config-field">';
                html += `<label for="${fieldId}">${key}:</label>`;
                
                if (prop.enum) {
                    html += `<select id="${fieldId}" onchange="updatePreview()">`;
                    for (const option of prop.enum) {
                        html += `<option value="${option}">${option}</option>`;
                    }
                    html += '</select>';
                } else if (prop.type === 'boolean') {
                    html += `<input type="checkbox" id="${fieldId}" onchange="updatePreview()">`;
                } else if (prop.type === 'number' || prop.type === 'integer') {
                    html += `<input type="number" id="${fieldId}" onchange="updatePreview()">`;
                } else {
                    html += `<input type="text" id="${fieldId}" onchange="updatePreview()">`;
                }
                
                html += `<div class="error" id="${fieldId}-error"></div>`;
                html += '</div>';
                
                if (prop.type === 'object' && prop.properties) {
                    html += '<div class="config-section">';
                    html += renderSchema(prop.properties, fieldId);
                    html += '</div>';
                }
            }
            
            return html;
        }
        
        function updatePreview() {
            const config = buildConfig();
            document.getElementById('config-preview').textContent = 
                JSON.stringify(config, null, 2);
        }
        
        function buildConfig() {
            // Build configuration from form values
            const config = {};
            // Implementation here
            return config;
        }
        
        function validateConfig() {
            // Validate against schema
            const config = buildConfig();
            // Implementation here
        }
        
        function exportConfig() {
            const config = buildConfig();
            const blob = new Blob([JSON.stringify(config, null, 2)], 
                                 {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'config.json';
            a.click();
        }
        
        // Initialize
        buildForm();
        updatePreview();
    </script>
</body>
</html>
        """
        return html
```

## Output Format

1. **Configuration Analysis**: Current configuration assessment
2. **Validation Schemas**: JSON Schema definitions for all configs
3. **Environment Rules**: Environment-specific validation rules
4. **Test Suite**: Comprehensive configuration tests
5. **Migration Scripts**: Version migration implementations
6. **Security Report**: Security issues and recommendations
7. **Documentation**: Auto-generated configuration reference
8. **Validation Pipeline**: CI/CD integration for config validation
9. **Interactive Tools**: Configuration builders and validators

Focus on preventing configuration errors, ensuring consistency across environments, and maintaining security best practices.