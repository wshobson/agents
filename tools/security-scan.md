# Security Scan and Vulnerability Assessment

You are a security expert specializing in application security, vulnerability assessment, and secure coding practices. Perform comprehensive security audits to identify vulnerabilities, provide remediation guidance, and implement security best practices.

## Context
The user needs a thorough security analysis to identify vulnerabilities, assess risks, and implement protection measures. Focus on OWASP Top 10, dependency vulnerabilities, and security misconfigurations with actionable remediation steps.

## Requirements
$ARGUMENTS

## Instructions

### 1. Security Scanning Tool Selection

Choose appropriate security scanning tools based on your technology stack and requirements:

**Tool Selection Matrix**
```python
security_tools = {
    'python': {
        'sast': {
            'bandit': {
                'strengths': ['Built for Python', 'Fast', 'Good defaults', 'AST-based'],
                'best_for': ['Python codebases', 'CI/CD pipelines', 'Quick scans'],
                'command': 'bandit -r . -f json -o bandit-report.json',
                'config_file': '.bandit'
            },
            'semgrep': {
                'strengths': ['Multi-language', 'Custom rules', 'Low false positives'],
                'best_for': ['Complex projects', 'Custom security patterns', 'Enterprise'],
                'command': 'semgrep --config=auto --json --output=semgrep-report.json',
                'config_file': '.semgrep.yml'
            }
        },
        'dependency_scan': {
            'safety': {
                'command': 'safety check --json --output safety-report.json',
                'database': 'PyUp.io vulnerability database',
                'best_for': 'Python package vulnerabilities'
            },
            'pip_audit': {
                'command': 'pip-audit --format=json --output=pip-audit-report.json',
                'database': 'OSV database',
                'best_for': 'Comprehensive Python vulnerability scanning'
            }
        }
    },
    
    'javascript': {
        'sast': {
            'eslint_security': {
                'command': 'eslint . --ext .js,.jsx,.ts,.tsx --format json > eslint-security.json',
                'plugins': ['@eslint/plugin-security', 'eslint-plugin-no-secrets'],
                'best_for': 'JavaScript/TypeScript security linting'
            },
            'sonarjs': {
                'command': 'sonar-scanner -Dsonar.projectKey=myproject',
                'best_for': 'Comprehensive code quality and security',
                'features': ['Vulnerability detection', 'Code smells', 'Technical debt']
            }
        },
        'dependency_scan': {
            'npm_audit': {
                'command': 'npm audit --json > npm-audit-report.json',
                'fix': 'npm audit fix',
                'best_for': 'NPM package vulnerabilities'
            },
            'yarn_audit': {
                'command': 'yarn audit --json > yarn-audit-report.json',
                'best_for': 'Yarn package vulnerabilities'
            },
            'snyk': {
                'command': 'snyk test --json > snyk-report.json',
                'fix': 'snyk wizard',
                'best_for': 'Comprehensive vulnerability management'
            }
        }
    },
    
    'container': {
        'trivy': {
            'image_scan': 'trivy image --format json --output trivy-image.json myimage:latest',
            'fs_scan': 'trivy fs --format json --output trivy-fs.json .',
            'repo_scan': 'trivy repo --format json --output trivy-repo.json .',
            'strengths': ['Fast', 'Accurate', 'Multiple targets', 'SBOM generation'],
            'best_for': 'Container and filesystem vulnerability scanning'
        },
        'grype': {
            'command': 'grype dir:. -o json > grype-report.json',
            'strengths': ['Fast', 'Accurate vulnerability detection'],
            'best_for': 'Container image and filesystem scanning'
        },
        'clair': {
            'api_based': True,
            'strengths': ['API-driven', 'Continuous monitoring'],
            'best_for': 'Registry integration, automated scanning'
        }
    },
    
    'infrastructure': {
        'checkov': {
            'command': 'checkov -d . --framework terraform --output json > checkov-report.json',
            'supports': ['Terraform', 'CloudFormation', 'Kubernetes', 'Helm', 'Serverless'],
            'best_for': 'Infrastructure as Code security'
        },
        'tfsec': {
            'command': 'tfsec . --format json > tfsec-report.json',
            'supports': ['Terraform'],
            'best_for': 'Terraform-specific security scanning'
        },
        'kube_score': {
            'command': 'kube-score score *.yaml --output-format json > kube-score.json',
            'supports': ['Kubernetes'],
            'best_for': 'Kubernetes manifest security and best practices'
        }
    },
    
    'secrets': {
        'truffleHog': {
            'command': 'trufflehog git file://. --json > trufflehog-report.json',
            'strengths': ['Git history scanning', 'High accuracy', 'Custom regex'],
            'best_for': 'Secret detection in git repositories'
        },
        'gitleaks': {
            'command': 'gitleaks detect --report-format json --report-path gitleaks-report.json',
            'strengths': ['Fast', 'Configurable', 'Pre-commit hooks'],
            'best_for': 'Real-time secret detection'
        },
        'detect_secrets': {
            'command': 'detect-secrets scan --all-files . > .secrets.baseline',
            'strengths': ['Baseline management', 'False positive reduction'],
            'best_for': 'Enterprise secret management'
        }
    }
}
```

**Multi-Tool Security Scanner**
```python
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VulnerabilityFinding:
    tool: str
    severity: str
    category: str
    title: str
    description: str
    file_path: str
    line_number: int
    cve: str
    cwe: str
    remediation: str
    confidence: str

class SecurityScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings = []
        self.scan_results = {}
        
    def detect_project_type(self) -> List[str]:
        """Detect project technologies to choose appropriate scanners"""
        technologies = []
        
        # Python
        if (self.project_path / 'requirements.txt').exists() or \
           (self.project_path / 'setup.py').exists() or \
           (self.project_path / 'pyproject.toml').exists():
            technologies.append('python')
            
        # JavaScript/Node.js
        if (self.project_path / 'package.json').exists():
            technologies.append('javascript')
            
        # Go
        if (self.project_path / 'go.mod').exists():
            technologies.append('golang')
            
        # Docker
        if (self.project_path / 'Dockerfile').exists():
            technologies.append('container')
            
        # Terraform
        if list(self.project_path.glob('*.tf')):
            technologies.append('terraform')
            
        # Kubernetes
        if list(self.project_path.glob('*.yaml')) or list(self.project_path.glob('*.yml')):
            technologies.append('kubernetes')
            
        return technologies
    
    def run_comprehensive_scan(self) -> Dict[str, Any]:
        """Run all applicable security scanners"""
        technologies = self.detect_project_type()
        
        scan_plan = {
            'timestamp': datetime.now().isoformat(),
            'technologies': technologies,
            'scanners_used': [],
            'findings': []
        }
        
        # Always run secret detection
        self.run_secret_scan()
        scan_plan['scanners_used'].append('secret_detection')
        
        # Technology-specific scans
        if 'python' in technologies:
            self.run_python_scans()
            scan_plan['scanners_used'].extend(['bandit', 'safety', 'pip_audit'])
            
        if 'javascript' in technologies:
            self.run_javascript_scans()
            scan_plan['scanners_used'].extend(['eslint_security', 'npm_audit'])
            
        if 'container' in technologies:
            self.run_container_scans()
            scan_plan['scanners_used'].append('trivy')
            
        if 'terraform' in technologies:
            self.run_terraform_scans()
            scan_plan['scanners_used'].extend(['checkov', 'tfsec'])
            
        # Generate unified report
        scan_plan['findings'] = self.findings
        scan_plan['summary'] = self.generate_summary()
        
        return scan_plan
    
    def run_secret_scan(self):
        """Run secret detection tools"""
        try:
            # TruffleHog
            result = subprocess.run([
                'trufflehog', 'filesystem', str(self.project_path),
                '--json', '--no-update'
            ], capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        finding = json.loads(line)
                        self.findings.append(VulnerabilityFinding(
                            tool='trufflehog',
                            severity='CRITICAL',
                            category='secrets',
                            title=f"Secret detected: {finding.get('DetectorName', 'Unknown')}",
                            description=finding.get('Raw', ''),
                            file_path=finding.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('file', ''),
                            line_number=finding.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('line', 0),
                            cve='',
                            cwe='CWE-798',
                            remediation='Remove secret and rotate credentials',
                            confidence=str(finding.get('Verified', False))
                        ))
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print("TruffleHog not available or scan failed")
            
        try:
            # GitLeaks
            result = subprocess.run([
                'gitleaks', 'detect', '--source', str(self.project_path),
                '--report-format', 'json', '--no-git'
            ], capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                findings = json.loads(result.stdout)
                for finding in findings:
                    self.findings.append(VulnerabilityFinding(
                        tool='gitleaks',
                        severity='HIGH',
                        category='secrets',
                        title=f"Secret pattern: {finding.get('RuleID', 'Unknown')}",
                        description=finding.get('Description', ''),
                        file_path=finding.get('File', ''),
                        line_number=finding.get('StartLine', 0),
                        cve='',
                        cwe='CWE-798',
                        remediation='Remove secret and add to .gitignore',
                        confidence='high'
                    ))
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print("GitLeaks not available or scan failed")
    
    def run_python_scans(self):
        """Run Python-specific security scanners"""
        # Bandit
        try:
            result = subprocess.run([
                'bandit', '-r', str(self.project_path),
                '-f', 'json', '--severity-level', 'medium'
            ], capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                bandit_results = json.loads(result.stdout)
                for result_item in bandit_results.get('results', []):
                    self.findings.append(VulnerabilityFinding(
                        tool='bandit',
                        severity=result_item.get('issue_severity', 'MEDIUM'),
                        category='sast',
                        title=result_item.get('test_name', ''),
                        description=result_item.get('issue_text', ''),
                        file_path=result_item.get('filename', ''),
                        line_number=result_item.get('line_number', 0),
                        cve='',
                        cwe=result_item.get('test_id', ''),
                        remediation=result_item.get('more_info', ''),
                        confidence=result_item.get('issue_confidence', 'MEDIUM')
                    ))
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print("Bandit not available or scan failed")
        
        # Safety
        try:
            result = subprocess.run([
                'safety', 'check', '--json'
            ], capture_output=True, text=True, timeout=300, cwd=self.project_path)
            
            if result.stdout:
                safety_results = json.loads(result.stdout)
                for vuln in safety_results:
                    self.findings.append(VulnerabilityFinding(
                        tool='safety',
                        severity='HIGH',
                        category='dependencies',
                        title=f"Vulnerable package: {vuln.get('package_name', '')}",
                        description=vuln.get('advisory', ''),
                        file_path='requirements.txt',
                        line_number=0,
                        cve=vuln.get('cve', ''),
                        cwe='',
                        remediation=f"Update to version {vuln.get('analyzed_version', 'latest')}",
                        confidence='high'
                    ))
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print("Safety not available or scan failed")
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        category_counts = {}
        
        for finding in self.findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
            category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        
        return {
            'total_findings': len(self.findings),
            'severity_breakdown': severity_counts,
            'category_breakdown': category_counts,
            'risk_score': self.calculate_risk_score(severity_counts)
        }
    
    def calculate_risk_score(self, severity_counts: Dict[str, int]) -> int:
        """Calculate overall risk score (0-100)"""
        weights = {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
        total_score = sum(weights[severity] * count for severity, count in severity_counts.items())
        max_possible = 100  # Arbitrary ceiling
        return min(100, int((total_score / max_possible) * 100))
```

**SAST (Static Application Security Testing)**
```python
# Enhanced code vulnerability patterns with tool-specific implementations
security_rules = {
    "sql_injection": {
        "patterns": [
            r"query\s*\(\s*[\"'].*\+.*[\"']\s*\)",
            r"execute\s*\(\s*[\"'].*%[s|d].*[\"']\s*%",
            r"f[\"'].*SELECT.*{.*}.*FROM"
        ],
        "severity": "CRITICAL",
        "cwe": "CWE-89",
        "fix": "Use parameterized queries or prepared statements"
    
    "xss": {
        "patterns": [
            r"innerHTML\s*=\s*[^\"']*\+",
            r"document\.write\s*\([^\"']*\+",
            r"dangerouslySetInnerHTML",
            r"v-html\s*=\s*[\"'][^\"']*\{"
        ],
        "severity": "HIGH",
        "cwe": "CWE-79",
        "fix": "Sanitize user input and use safe rendering methods"
    },
    
    "hardcoded_secrets": {
        "patterns": [
            r"(?i)(api[_-]?key|apikey|secret|password)\s*[:=]\s*[\"'][^\"']{8,}[\"']",
            r"(?i)bearer\s+[a-zA-Z0-9\-\._~\+\/]{20,}",
            r"(?i)(aws[_-]?access[_-]?key[_-]?id|aws[_-]?secret)\s*[:=]",
            r"private[_-]?key\s*[:=]\s*[\"'][^\"']+[\"']"
        ],
        "severity": "CRITICAL",
        "cwe": "CWE-798",
        "fix": "Use environment variables or secure key management service"
    },
    
    "path_traversal": {
        "patterns": [
            r"\.\.\/",
            r"readFile\s*\([^\"']*\+",
            r"include\s*\([^\"']*\$",
            r"require\s*\([^\"']*\+"
        ],
        "severity": "HIGH",
        "cwe": "CWE-22",
        "fix": "Validate and sanitize file paths"
    },
    
    "insecure_random": {
        "patterns": [
            r"Math\.random\(\)",
            r"rand\(\)",
            r"mt_rand\(\)"
        ],
        "severity": "MEDIUM",
        "cwe": "CWE-330",
        "fix": "Use cryptographically secure random functions"
    }
}

def scan_code_vulnerabilities(file_path, content):
    """
    Enhanced code vulnerability scanning with framework-specific patterns
    """
    vulnerabilities = []
    
    for vuln_type, rule in security_rules.items():
        for pattern in rule['patterns']:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    'type': vuln_type,
                    'severity': rule['severity'],
                    'file': file_path,
                    'line': line_num,
                    'code': match.group(0),
                    'cwe': rule['cwe'],
                    'fix': rule['fix'],
                    'confidence': rule.get('confidence', 'medium'),
                    'owasp_category': rule.get('owasp', 'A03:2021-Injection')
                })
    
    return vulnerabilities

# Framework-specific security patterns
framework_security_patterns = {
    'django': {
        'csrf_exempt': {
            'pattern': r'@csrf_exempt',
            'severity': 'HIGH',
            'description': 'CSRF protection disabled',
            'fix': 'Remove @csrf_exempt decorator and implement proper CSRF protection'
        },
        'raw_sql': {
            'pattern': r'\.raw\(["\'][^"\']\*["\']\)',
            'severity': 'HIGH',
            'description': 'Raw SQL query detected',
            'fix': 'Use Django ORM or parameterized queries'
        },
        'eval_usage': {
            'pattern': r'eval\(',
            'severity': 'CRITICAL',
            'description': 'Code evaluation detected',
            'fix': 'Remove eval() usage and use safe alternatives'
        }
    },
    
    'flask': {
        'debug_mode': {
            'pattern': r'debug\s*=\s*True',
            'severity': 'MEDIUM',
            'description': 'Debug mode enabled in production',
            'fix': 'Set debug=False in production'
        },
        'render_template_string': {
            'pattern': r'render_template_string\([^)]*\+',
            'severity': 'HIGH',
            'description': 'Template injection vulnerability',
            'fix': 'Use render_template with static templates'
        }
    },
    
    'react': {
        'dangerous_html': {
            'pattern': r'dangerouslySetInnerHTML',
            'severity': 'HIGH',
            'description': 'XSS vulnerability through innerHTML',
            'fix': 'Sanitize HTML content or use safe rendering'
        },
        'eval_usage': {
            'pattern': r'\beval\(',
            'severity': 'CRITICAL',
            'description': 'Code evaluation detected',
            'fix': 'Remove eval() usage'
        }
    },
    
    'express': {
        'missing_helmet': {
            'pattern': r'express\(\)',
            'negative_pattern': r'helmet\(\)',
            'severity': 'MEDIUM',
            'description': 'Security headers middleware missing',
            'fix': 'Add helmet() middleware for security headers'
        },
        'cors_wildcard': {
            'pattern': r'origin:\s*["\']\*["\']',
            'severity': 'HIGH',
            'description': 'CORS configured with wildcard origin',
            'fix': 'Specify exact allowed origins'
        }
    }
}

def scan_framework_vulnerabilities(framework, file_path, content):
    """Scan for framework-specific security issues"""
    vulnerabilities = []
    
    if framework not in framework_security_patterns:
        return vulnerabilities
    
    patterns = framework_security_patterns[framework]
    
    for vuln_type, rule in patterns.items():
        matches = re.finditer(rule['pattern'], content, re.MULTILINE)
        
        # Check for negative patterns (e.g., missing security middleware)
        if 'negative_pattern' in rule:
            if not re.search(rule['negative_pattern'], content):
                vulnerabilities.append({
                    'type': f'{framework}_{vuln_type}',
                    'severity': rule['severity'],
                    'file': file_path,
                    'description': rule['description'],
                    'fix': rule['fix'],
                    'framework': framework
                })
        else:
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    'type': f'{framework}_{vuln_type}',
                    'severity': rule['severity'],
                    'file': file_path,
                    'line': line_num,
                    'code': match.group(0),
                    'description': rule['description'],
                    'fix': rule['fix'],
                    'framework': framework
                })
    
    return vulnerabilities
```

**Advanced Dependency Vulnerability Scanning**
```python
import subprocess
import json
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta

class DependencyScanner:
    def __init__(self):
        self.vulnerability_databases = {
            'osv': 'https://api.osv.dev/v1/query',
            'snyk': 'https://api.snyk.io/v1/test',
            'github': 'https://api.github.com/advisories'
        }
    
    def scan_all_ecosystems(self, project_path: str) -> Dict[str, Any]:
        """Comprehensive dependency scanning across all package managers"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'ecosystems': {},
            'summary': {'total_vulnerabilities': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        }
        
        # Detect and scan each ecosystem
        ecosystems = self.detect_ecosystems(project_path)
        
        for ecosystem in ecosystems:
            results['ecosystems'][ecosystem] = self.scan_ecosystem(ecosystem, project_path)
            self.update_summary(results['summary'], results['ecosystems'][ecosystem])
        
        return results
    
    def detect_ecosystems(self, project_path: str) -> List[str]:
        """Detect package managers and dependency files"""
        ecosystems = []
        
        ecosystem_files = {
            'npm': ['package.json', 'package-lock.json', 'yarn.lock'],
            'pip': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
            'maven': ['pom.xml'],
            'gradle': ['build.gradle', 'build.gradle.kts'],
            'gem': ['Gemfile', 'Gemfile.lock'],
            'composer': ['composer.json', 'composer.lock'],
            'nuget': ['*.csproj', 'packages.config'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock']
        }
        
        for ecosystem, files in ecosystem_files.items():
            if any(Path(project_path).glob(f) for f in files):
                ecosystems.append(ecosystem)
        
        return ecosystems
    
    def scan_npm_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Scan NPM dependencies using multiple tools"""
        results = {
            'tool_results': {},
            'vulnerabilities': [],
            'total_packages': 0,
            'outdated_packages': []
        }
        
        # NPM Audit
        try:
            npm_result = subprocess.run(
                ['npm', 'audit', '--json'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if npm_result.stdout:
                audit_data = json.loads(npm_result.stdout)
                results['tool_results']['npm_audit'] = audit_data
                
                for vuln_id, vuln in audit_data.get('vulnerabilities', {}).items():
                    results['vulnerabilities'].append({
                        'id': vuln_id,
                        'severity': vuln.get('severity', 'unknown'),
                        'title': vuln.get('title', ''),
                        'package': vuln.get('name', ''),
                        'version': vuln.get('range', ''),
                        'cwe': vuln.get('cwe', []),
                        'cve': vuln.get('cves', []),
                        'fixed_in': vuln.get('fixAvailable', ''),
                        'source': 'npm_audit'
                    })
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError):
            results['tool_results']['npm_audit'] = {'error': 'Failed to run npm audit'}
        
        # Snyk scan (if available)
        try:
            snyk_result = subprocess.run(
                ['snyk', 'test', '--json'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if snyk_result.stdout:
                snyk_data = json.loads(snyk_result.stdout)
                results['tool_results']['snyk'] = snyk_data
                
                for vuln in snyk_data.get('vulnerabilities', []):
                    results['vulnerabilities'].append({
                        'id': vuln.get('id', ''),
                        'severity': vuln.get('severity', 'unknown'),
                        'title': vuln.get('title', ''),
                        'package': vuln.get('packageName', ''),
                        'version': vuln.get('version', ''),
                        'cve': vuln.get('identifiers', {}).get('CVE', []),
                        'cwe': vuln.get('identifiers', {}).get('CWE', []),
                        'upgrade_path': vuln.get('upgradePath', []),
                        'source': 'snyk'
                    })
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError):
            results['tool_results']['snyk'] = {'error': 'Snyk not available or failed'}
        
        return results
    
    def scan_python_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Comprehensive Python dependency scanning"""
        results = {
            'tool_results': {},
            'vulnerabilities': [],
            'license_issues': []
        }
        
        # Safety scan
        try:
            safety_result = subprocess.run(
                ['safety', 'check', '--json'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if safety_result.stdout:
                safety_data = json.loads(safety_result.stdout)
                results['tool_results']['safety'] = safety_data
                
                for vuln in safety_data:
                    results['vulnerabilities'].append({
                        'package': vuln.get('package_name', ''),
                        'version': vuln.get('analyzed_version', ''),
                        'vulnerability_id': vuln.get('vulnerability_id', ''),
                        'advisory': vuln.get('advisory', ''),
                        'cve': vuln.get('cve', ''),
                        'severity': self.map_safety_severity(vuln.get('vulnerability_id', '')),
                        'source': 'safety'
                    })
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError):
            results['tool_results']['safety'] = {'error': 'Safety scan failed'}
        
        # pip-audit scan
        try:
            pip_audit_result = subprocess.run(
                ['pip-audit', '--format=json'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if pip_audit_result.stdout:
                pip_audit_data = json.loads(pip_audit_result.stdout)
                results['tool_results']['pip_audit'] = pip_audit_data
                
                for vuln in pip_audit_data.get('vulnerabilities', []):
                    results['vulnerabilities'].append({
                        'package': vuln.get('package', ''),
                        'version': vuln.get('version', ''),
                        'vulnerability_id': vuln.get('id', ''),
                        'description': vuln.get('description', ''),
                        'aliases': vuln.get('aliases', []),
                        'fix_versions': vuln.get('fix_versions', []),
                        'source': 'pip_audit'
                    })
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError):
            results['tool_results']['pip_audit'] = {'error': 'pip-audit not available'}
        
        return results
    
    def generate_remediation_plan(self, vulnerabilities: List[Dict]) -> Dict[str, Any]:
        """Generate prioritized remediation plan"""
        plan = {
            'immediate_actions': [],
            'short_term': [],
            'long_term': [],
            'automation_scripts': {}
        }
        
        # Sort by severity
        critical_high = [v for v in vulnerabilities if v.get('severity', '').upper() in ['CRITICAL', 'HIGH']]
        medium = [v for v in vulnerabilities if v.get('severity', '').upper() == 'MEDIUM']
        low = [v for v in vulnerabilities if v.get('severity', '').upper() == 'LOW']
        
        # Immediate actions for critical/high
        for vuln in critical_high:
            plan['immediate_actions'].append({
                'package': vuln.get('package', ''),
                'current_version': vuln.get('version', ''),
                'fixed_version': vuln.get('fixed_in', vuln.get('fix_versions', ['latest'])[0] if vuln.get('fix_versions') else 'latest'),
                'action': f"Update {vuln.get('package', '')} to {vuln.get('fixed_in', 'latest')}",
                'priority': 1,
                'effort': 'Low'
            })
        
        # Auto-update script
        plan['automation_scripts']['npm_auto_update'] = """
#!/bin/bash
# Automated npm dependency updates
npm audit fix --force
npm update
npm audit
"""
        
        plan['automation_scripts']['pip_auto_update'] = """
#!/bin/bash
# Automated Python dependency updates
pip install --upgrade pip
pip-audit --fix
safety check
"""
        
        return plan

# Example usage with specific package managers
npm_audit_example = {
    "dependencies": {
        "lodash": {
            "version": "4.17.15",
            "vulnerabilities": [{
                "severity": "HIGH",
                "cve": "CVE-2021-23337",
                "description": "Command Injection in lodash",
                "fixed_in": "4.17.21",
                "recommendation": "npm install lodash@4.17.21",
                "automated_fix": "npm audit fix"
            }]
        },
        "@types/node": {
            "version": "14.0.0",
            "vulnerabilities": [],
            "outdated": True,
            "latest_version": "20.0.0",
            "recommendation": "npm install @types/node@latest"
        }
    },
    "summary": {
        "total_packages": 847,
        "vulnerable_packages": 12,
        "outdated_packages": 45,
        "license_issues": 3
    }
}

# Python requirements scan
# Container Image Vulnerability Scanning
def scan_container_vulnerabilities(image_name: str) -> Dict[str, Any]:
    """
    Comprehensive container vulnerability scanning using multiple tools
    """
    results = {
        'image': image_name,
        'scan_results': {},
        'vulnerabilities': [],
        'sbom': {},
        'compliance_checks': {}
    }
    
    # Trivy scan
    try:
        trivy_result = subprocess.run([
            'trivy', 'image', '--format', 'json',
            '--security-checks', 'vuln,config,secret',
            image_name
        ], capture_output=True, text=True, timeout=300)
        
        if trivy_result.stdout:
            trivy_data = json.loads(trivy_result.stdout)
            results['scan_results']['trivy'] = trivy_data
            
            for result in trivy_data.get('Results', []):
                for vuln in result.get('Vulnerabilities', []):
                    results['vulnerabilities'].append({
                        'package': vuln.get('PkgName', ''),
                        'version': vuln.get('InstalledVersion', ''),
                        'vulnerability_id': vuln.get('VulnerabilityID', ''),
                        'severity': vuln.get('Severity', 'UNKNOWN'),
                        'title': vuln.get('Title', ''),
                        'description': vuln.get('Description', ''),
                        'fixed_version': vuln.get('FixedVersion', ''),
                        'source': 'trivy'
                    })
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError):
        results['scan_results']['trivy'] = {'error': 'Trivy scan failed'}
    
    # Generate SBOM (Software Bill of Materials)
    try:
        sbom_result = subprocess.run([
            'trivy', 'image', '--format', 'spdx-json',
            image_name
        ], capture_output=True, text=True, timeout=180)
        
        if sbom_result.stdout:
            results['sbom'] = json.loads(sbom_result.stdout)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError):
        results['sbom'] = {'error': 'SBOM generation failed'}
    
    return results

# Multi-ecosystem scanner
class UniversalDependencyScanner:
    def __init__(self):
        self.scanners = {
            'python': self.scan_python_dependencies,
            'javascript': self.scan_npm_dependencies,
            'java': self.scan_java_dependencies,
            'go': self.scan_go_dependencies,
            'rust': self.scan_rust_dependencies,
            'container': self.scan_container_image
        }
    
    def scan_python_dependencies(self, project_path: str) -> Dict[str, Any]:
        """
        Enhanced Python dependency scanning with multiple tools
        """
        results = {
            'tools_used': ['safety', 'pip-audit', 'bandit'],
            'vulnerabilities': [],
            'license_compliance': [],
            'outdated_packages': []
        }
        
        # Safety check
        try:
            safety_cmd = ['safety', 'check', '--json', '--full-report']
            result = subprocess.run(safety_cmd, capture_output=True, text=True, timeout=120)
            
            if result.stdout:
                safety_data = json.loads(result.stdout)
                for vuln in safety_data:
                    results['vulnerabilities'].append({
                        'tool': 'safety',
                        'package': vuln.get('package_name'),
                        'version': vuln.get('analyzed_version'),
                        'vulnerability_id': vuln.get('vulnerability_id'),
                        'severity': self._map_safety_severity(vuln.get('vulnerability_id')),
                        'advisory': vuln.get('advisory'),
                        'cve': vuln.get('cve'),
                        'remediation': f"Update to {vuln.get('fixed_version', 'latest version')}"
                    })
        except Exception as e:
            results['safety_error'] = str(e)
        
        # pip-audit
        try:
            pip_audit_cmd = ['pip-audit', '--format=json', '--desc']
            result = subprocess.run(pip_audit_cmd, capture_output=True, text=True, timeout=120)
            
            if result.stdout:
                pip_audit_data = json.loads(result.stdout)
                for vuln in pip_audit_data.get('vulnerabilities', []):
                    results['vulnerabilities'].append({
                        'tool': 'pip-audit',
                        'package': vuln.get('package'),
                        'version': vuln.get('version'),
                        'vulnerability_id': vuln.get('id'),
                        'severity': self._calculate_severity_from_cvss(vuln.get('fix_versions', [])),
                        'description': vuln.get('description'),
                        'aliases': vuln.get('aliases', []),
                        'fix_versions': vuln.get('fix_versions', []),
                        'remediation': f"Update to one of: {', '.join(vuln.get('fix_versions', ['latest']))}"
                    })
        except Exception as e:
            results['pip_audit_error'] = str(e)
        
        # License compliance check
        try:
            pip_licenses_result = subprocess.run(
                ['pip-licenses', '--format=json'],
                capture_output=True, text=True, timeout=60
            )
            
            if pip_licenses_result.stdout:
                licenses_data = json.loads(pip_licenses_result.stdout)
                problematic_licenses = ['GPL', 'AGPL', 'SSPL', 'BUSL']
                
                for package in licenses_data:
                    license_name = package.get('License', 'Unknown')
                    if any(prob in license_name.upper() for prob in problematic_licenses):
                        results['license_compliance'].append({
                            'package': package.get('Name'),
                            'version': package.get('Version'),
                            'license': license_name,
                            'issue': 'Potentially problematic license for commercial use',
                            'action': 'Review license compatibility'
                        })
        except Exception as e:
            results['license_error'] = str(e)
        
        return results
    
    def _map_safety_severity(self, vuln_id: str) -> str:
        """Map Safety vulnerability ID to severity level"""
        # Safety uses numeric IDs, we can implement CVSS mapping
        # This is a simplified mapping - in practice, use CVSS scores
        high_risk_patterns = ['injection', 'rce', 'deserialization']
        if any(pattern in vuln_id.lower() for pattern in high_risk_patterns):
            return 'CRITICAL'
        return 'HIGH'  # Default for Safety findings
    
    def _calculate_severity_from_cvss(self, fix_versions: list) -> str:
        """Calculate severity based on fix version availability"""
        if not fix_versions:
            return 'HIGH'  # No fix available
        return 'MEDIUM'  # Fix available
```

### 2. OWASP Top 10 Assessment

Check for OWASP Top 10 vulnerabilities:

**A01: Broken Access Control**
```python
# Check for missing authentication
def check_access_control():
    findings = []
    
    # API endpoints without auth
    unprotected_endpoints = [
        {'path': '/api/admin/*', 'method': 'GET', 'auth': False},
        {'path': '/api/users/delete', 'method': 'POST', 'auth': False}
    ]
    
    # Insecure direct object references
    idor_patterns = [
        r"user_id\s*=\s*request\.(GET|POST)\[",
        r"WHERE\s+id\s*=\s*\$_GET\[",
        r"findById\(req\.params\.id\)"
    ]
    
    # Missing authorization checks
    missing_authz = [
        {'file': 'routes/admin.js', 'line': 45, 'issue': 'No role check'},
        {'file': 'api/delete.py', 'line': 12, 'issue': 'No ownership validation'}
    ]
    
    return findings
```

**A02: Cryptographic Failures**
```python
# Check encryption and hashing
crypto_issues = {
    "weak_hashing": [
        {"algorithm": "MD5", "usage": "password hashing", "severity": "CRITICAL"},
        {"algorithm": "SHA1", "usage": "token generation", "severity": "HIGH"}
    ],
    "insecure_storage": [
        {"data": "credit cards", "storage": "plain text in database"},
        {"data": "SSN", "storage": "base64 encoded only"}
    ],
    "missing_encryption": [
        {"connection": "database", "protocol": "unencrypted TCP"},
        {"api": "payment service", "protocol": "HTTP"}
    ],
    "weak_tls": [
        {"version": "TLS 1.0", "recommendation": "Use TLS 1.2+"},
        {"cipher": "DES-CBC3-SHA", "recommendation": "Use ECDHE-RSA-AES256-GCM-SHA384"}
    ]
}
```

**A03: Injection**
```python
# SQL Injection detection
sql_injection_tests = [
    {"payload": "' OR '1'='1", "vulnerable": True},
    {"payload": "'; DROP TABLE users; --", "vulnerable": True},
    {"payload": "1' UNION SELECT * FROM users--", "vulnerable": False}
]

# NoSQL Injection
nosql_injection = {
    "mongodb": [
        {"query": "db.users.find({username: req.body.username})", "vulnerable": True},
        {"fix": "db.users.find({username: {$eq: req.body.username}})"}
    ]
}

# Command Injection
command_injection = [
    {
        "code": "exec('ping ' + user_input)",
        "vulnerability": "Direct command execution with user input",
        "fix": "Use subprocess with shell=False and validate input"
    }
]
```

### 3. Infrastructure Security

Scan infrastructure and configuration:

**Container Security**
```dockerfile
# Dockerfile security scan
FROM node:14  # ISSUE: Using non-specific tag
USER root     # ISSUE: Running as root

# ISSUE: Installing packages without version pinning
RUN apt-get update && apt-get install -y curl

# ISSUE: Copying sensitive files
COPY . /app
COPY .env /app/.env  # CRITICAL: Copying secrets

# ISSUE: Not dropping privileges
CMD ["node", "server.js"]

# Secure version:
FROM node:14.17.6-alpine AS builder
RUN apk add --no-cache python3 make g++
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:14.17.6-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
WORKDIR /app
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**Kubernetes Security**
```yaml
# Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

### 4. API Security

Comprehensive API security testing:

**Authentication & Authorization**
```python
# JWT Security Issues
jwt_vulnerabilities = {
    "weak_secret": {
        "issue": "JWT signed with weak secret 'secret123'",
        "severity": "CRITICAL",
        "fix": "Use strong 256-bit secret from environment"
    },
    "algorithm_confusion": {
        "issue": "JWT accepts 'none' algorithm",
        "severity": "CRITICAL",
        "fix": "Explicitly verify algorithm: ['HS256', 'RS256']"
    },
    "missing_expiration": {
        "issue": "JWT tokens never expire",
        "severity": "HIGH",
        "fix": "Set exp claim to reasonable duration (e.g., 1 hour)"
    }
}

# API Rate Limiting
rate_limit_config = {
    "endpoints": {
        "/api/login": {"limit": 5, "window": "5m", "status": "NOT_CONFIGURED"},
        "/api/password-reset": {"limit": 3, "window": "1h", "status": "NOT_CONFIGURED"},
        "/api/data": {"limit": 100, "window": "1m", "status": "OK"}
    }
}
```

**Input Validation**
```python
# API Input Validation Issues
validation_issues = [
    {
        "endpoint": "/api/users",
        "method": "POST",
        "field": "email",
        "issue": "No email format validation",
        "exploit": "user@<script>alert(1)</script>.com"
    },
    {
        "endpoint": "/api/upload",
        "method": "POST",
        "field": "file",
        "issue": "No file type validation",
        "exploit": "shell.php renamed to image.jpg"
    }
]
```

### 5. Secret Detection

Scan for exposed secrets and credentials:

**Secret Patterns**
```python
secret_patterns = {
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "aws_secret_key": r"[0-9a-zA-Z/+=]{40}",
    "github_token": r"ghp_[0-9a-zA-Z]{36}",
    "stripe_key": r"sk_live_[0-9a-zA-Z]{24}",
    "private_key": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
    "google_api": r"AIza[0-9A-Za-z\-_]{35}",
    "jwt_token": r"eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+",
    "slack_webhook": r"https://hooks\.slack\.com/services/[A-Z0-9]{9}/[A-Z0-9]{9}/[a-zA-Z0-9]{24}"
}

# Git history scan
def scan_git_history():
    """
    Scan git history for accidentally committed secrets
    """
    import subprocess
    
    # Get all commits
    commits = subprocess.run(
        ['git', 'log', '--pretty=format:%H'],
        capture_output=True,
        text=True
    ).stdout.split('\n')
    
    secrets_found = []
    
    for commit in commits[:100]:  # Last 100 commits
        diff = subprocess.run(
            ['git', 'show', commit],
            capture_output=True,
            text=True
        ).stdout
        
        for secret_type, pattern in secret_patterns.items():
            if re.search(pattern, diff):
                secrets_found.append({
                    'commit': commit,
                    'type': secret_type,
                    'action': 'Remove from history and rotate credential'
                })
    
    return secrets_found
```

### 6. Security Headers

Check HTTP security headers:

**Header Configuration**
```python
security_headers = {
    "Strict-Transport-Security": {
        "required": True,
        "value": "max-age=31536000; includeSubDomains; preload",
        "missing_impact": "Vulnerable to protocol downgrade attacks"
    },
    "X-Content-Type-Options": {
        "required": True,
        "value": "nosniff",
        "missing_impact": "Vulnerable to MIME type confusion attacks"
    },
    "X-Frame-Options": {
        "required": True,
        "value": "DENY",
        "missing_impact": "Vulnerable to clickjacking"
    },
    "Content-Security-Policy": {
        "required": True,
        "value": "default-src 'self'; script-src 'self' 'unsafe-inline'",
        "missing_impact": "Vulnerable to XSS attacks"
    },
    "X-XSS-Protection": {
        "required": False,  # Deprecated
        "value": "0",
        "note": "Modern browsers have built-in XSS protection"
    },
    "Referrer-Policy": {
        "required": True,
        "value": "strict-origin-when-cross-origin",
        "missing_impact": "May leak sensitive URLs"
    },
    "Permissions-Policy": {
        "required": True,
        "value": "geolocation=(), microphone=(), camera=()",
        "missing_impact": "Allows access to sensitive browser features"
    }
}
```

### 7. Automated Remediation Implementation

Provide intelligent, automated fixes with safety validation:

**Smart Remediation Engine**
```python
import ast
import re
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class RemediationAction:
    vulnerability_id: str
    action_type: str  # 'dependency_update', 'code_fix', 'config_change'
    description: str
    risk_level: str  # 'safe', 'low_risk', 'medium_risk', 'high_risk'
    automated: bool
    manual_steps: List[str]
    validation_tests: List[str]
    rollback_plan: str

class AutomatedRemediationEngine:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.backup_created = False
        self.applied_fixes = []
        
    def create_safety_backup(self) -> str:
        """Create git branch backup before applying fixes"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_branch = f'security_backup_{timestamp}'
        
        try:
            subprocess.run(['git', 'checkout', '-b', backup_branch], 
                         cwd=self.project_path, check=True)
            subprocess.run(['git', 'checkout', '-'], 
                         cwd=self.project_path, check=True)
            self.backup_created = True
            return backup_branch
        except subprocess.CalledProcessError:
            raise Exception("Failed to create safety backup branch")
    
    def apply_automated_fixes(self, vulnerabilities: List[Dict]) -> List[RemediationAction]:
        """Apply safe automated fixes"""
        if not self.backup_created:
            self.create_safety_backup()
        
        actions = []
        
        for vuln in vulnerabilities:
            action = self.generate_remediation_action(vuln)
            
            if action.automated and action.risk_level in ['safe', 'low_risk']:
                try:
                    success = self.apply_fix(action)
                    if success:
                        actions.append(action)
                        self.applied_fixes.append(action)
                except Exception as e:
                    print(f"Failed to apply fix for {action.vulnerability_id}: {e}")
            else:
                actions.append(action)
        
        return actions
    
    def generate_remediation_action(self, vulnerability: Dict) -> RemediationAction:
        """Generate specific remediation action for vulnerability"""
        vuln_type = vulnerability.get('type', '')
        severity = vulnerability.get('severity', 'MEDIUM')
        
        if vuln_type == 'vulnerable_dependency':
            return self._fix_vulnerable_dependency(vulnerability)
        elif vuln_type == 'sql_injection':
            return self._fix_sql_injection(vulnerability)
        elif vuln_type == 'hardcoded_secrets':
            return self._fix_hardcoded_secrets(vulnerability)
        elif vuln_type == 'missing_security_headers':
            return self._fix_security_headers(vulnerability)
        else:
            return self._generic_fix(vulnerability)
    
    def _fix_vulnerable_dependency(self, vuln: Dict) -> RemediationAction:
        """Fix vulnerable dependencies automatically"""
        package = vuln.get('package', '')
        current_version = vuln.get('version', '')
        fixed_version = vuln.get('fixed_version', 'latest')
        
        # Determine package manager
        if (self.project_path / 'package.json').exists():
            update_command = f'npm install {package}@{fixed_version}'
            ecosystem = 'npm'
        elif (self.project_path / 'requirements.txt').exists():
            update_command = f'pip install {package}=={fixed_version}'
            ecosystem = 'pip'
        else:
            ecosystem = 'unknown'
            update_command = f'# Update {package} to {fixed_version}'
        
        return RemediationAction(
            vulnerability_id=vuln.get('id', ''),
            action_type='dependency_update',
            description=f'Update {package} from {current_version} to {fixed_version}',
            risk_level='safe',  # Dependency updates are generally safe
            automated=True,
            manual_steps=[
                f'Run: {update_command}',
                'Test application functionality',
                'Update lock file if needed'
            ],
            validation_tests=[
                f'Check {package} version is {fixed_version}',
                'Run regression tests',
                'Verify no new vulnerabilities introduced'
            ],
            rollback_plan=f'Revert to {package}@{current_version}'
        )
    
    def _fix_sql_injection(self, vuln: Dict) -> RemediationAction:
        """Fix SQL injection vulnerabilities"""
        file_path = vuln.get('file_path', '')
        line_number = vuln.get('line_number', 0)
        
        # Read the vulnerable code
        try:
            with open(self.project_path / file_path, 'r') as f:
                lines = f.readlines()
            
            vulnerable_line = lines[line_number - 1] if line_number > 0 else ''
            
            # Generate fix based on language and framework
            if file_path.endswith('.py'):
                fixed_code = self._fix_python_sql_injection(vulnerable_line)
            elif file_path.endswith('.js'):
                fixed_code = self._fix_javascript_sql_injection(vulnerable_line)
            else:
                fixed_code = '# Manual fix required'
            
            return RemediationAction(
                vulnerability_id=vuln.get('id', ''),
                action_type='code_fix',
                description=f'Fix SQL injection in {file_path}:{line_number}',
                risk_level='medium_risk',  # Code changes need testing
                automated=False,  # Require manual review
                manual_steps=[
                    f'Replace line {line_number} in {file_path}',
                    f'Original: {vulnerable_line.strip()}',
                    f'Fixed: {fixed_code}',
                    'Add input validation',
                    'Test with malicious inputs'
                ],
                validation_tests=[
                    'SQL injection penetration testing',
                    'Unit tests for the affected function',
                    'Integration tests for the endpoint'
                ],
                rollback_plan=f'Revert changes to {file_path}'
            )
        except Exception as e:
            return self._generic_fix(vuln)
    
    def _fix_python_sql_injection(self, vulnerable_line: str) -> str:
        """Generate Python SQL injection fix"""
        # Simple pattern matching for common cases
        if 'cursor.execute(' in vulnerable_line and '{}' in vulnerable_line:
            return vulnerable_line.replace('.format(', ', (').replace('{}', '?')
        elif 'query(' in vulnerable_line and '+' in vulnerable_line:
            return '# Use parameterized query: query("SELECT * FROM table WHERE id = ?", (user_id,))'
        return '# Replace with parameterized query'
    
    def _fix_hardcoded_secrets(self, vuln: Dict) -> RemediationAction:
        """Fix hardcoded secrets"""
        file_path = vuln.get('file_path', '')
        secret_type = vuln.get('secret_type', 'credential')
        
        return RemediationAction(
            vulnerability_id=vuln.get('id', ''),
            action_type='code_fix',
            description=f'Remove hardcoded {secret_type} from {file_path}',
            risk_level='high_risk',  # Secrets need immediate attention
            automated=False,  # Never automate secret removal
            manual_steps=[
                f'Remove hardcoded secret from {file_path}',
                'Add secret to environment variables or secret manager',
                'Update code to read from environment',
                'Rotate the exposed credential',
                'Add {file_path} to .gitignore if needed',
                'Scan git history for credential exposure'
            ],
            validation_tests=[
                'Verify application works with environment variable',
                'Confirm no secrets in code',
                'Test with invalid/missing environment variable'
            ],
            rollback_plan='Use temporary hardcoded value until proper secret management'
        )
    
    def apply_fix(self, action: RemediationAction) -> bool:
        """Apply an automated fix"""
        if action.action_type == 'dependency_update':
            return self._apply_dependency_update(action)
        elif action.action_type == 'config_change':
            return self._apply_config_change(action)
        return False
    
    def _apply_dependency_update(self, action: RemediationAction) -> bool:
        """Apply dependency update"""
        try:
            # Extract update command from manual steps
            update_command = None
            for step in action.manual_steps:
                if step.startswith('Run: '):
                    update_command = step[5:].split()
                    break
            
            if update_command:
                result = subprocess.run(
                    update_command,
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print(f"Successfully applied: {action.description}")
                    return True
                else:
                    print(f"Failed to apply {action.description}: {result.stderr}")
                    return False
            
            return False
        except Exception as e:
            print(f"Error applying fix: {e}")
            return False
    
    def generate_remediation_report(self, actions: List[RemediationAction]) -> str:
        """Generate comprehensive remediation report"""
        report = []
        report.append("# Security Remediation Report\n")
        report.append(f"**Generated**: {datetime.now().isoformat()}\n")
        report.append(f"**Total Actions**: {len(actions)}\n")
        
        automated_count = sum(1 for a in actions if a.automated and a.risk_level in ['safe', 'low_risk'])
        manual_count = len(actions) - automated_count
        
        report.append(f"**Automated Fixes Applied**: {automated_count}\n")
        report.append(f"**Manual Actions Required**: {manual_count}\n\n")
        
        # Group by action type
        by_type = {}
        for action in actions:
            if action.action_type not in by_type:
                by_type[action.action_type] = []
            by_type[action.action_type].append(action)
        
        for action_type, type_actions in by_type.items():
            report.append(f"## {action_type.replace('_', ' ').title()}\n")
            
            for action in type_actions:
                report.append(f"### {action.description}\n")
                report.append(f"**Risk Level**: {action.risk_level}\n")
                report.append(f"**Automated**: {'✅' if action.automated else '❌'}\n")
                
                if action.manual_steps:
                    report.append("**Manual Steps**:\n")
                    for step in action.manual_steps:
                        report.append(f"- {step}\n")
                
                if action.validation_tests:
                    report.append("**Validation Tests**:\n")
                    for test in action.validation_tests:
                        report.append(f"- {test}\n")
                
                report.append(f"**Rollback**: {action.rollback_plan}\n\n")
        
        return ''.join(report)

# Security Middleware Templates
security_middleware_templates = {
    'express': """
// Enhanced Express.js security middleware
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
const hpp = require('hpp');
const cors = require('cors');

// Content Security Policy
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "https://trusted-cdn.com"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
            imgSrc: ["'self'", "data:", "https:"],
            connectSrc: ["'self'"],
            fontSrc: ["'self'", "https://fonts.gstatic.com"],
            objectSrc: ["'none'"],
            mediaSrc: ["'self'"],
            frameSrc: ["'none'"],
            baseUri: ["'self'"],
            formAction: ["'self'"]
        },
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    },
    noSniff: true,
    xssFilter: true,
    referrerPolicy: { policy: 'same-origin' }
}));

// Advanced rate limiting
const createRateLimiter = (windowMs, max, message) => rateLimit({
    windowMs,
    max,
    message: { error: message },
    standardHeaders: true,
    legacyHeaders: false,
    handler: (req, res) => {
        res.status(429).json({
            error: message,
            retryAfter: Math.round(windowMs / 1000)
        });
    }
});

// Different limits for different endpoints
app.use('/api/auth/login', createRateLimiter(15 * 60 * 1000, 5, 'Too many login attempts'));
app.use('/api/auth/register', createRateLimiter(60 * 60 * 1000, 3, 'Too many registration attempts'));
app.use('/api/', createRateLimiter(15 * 60 * 1000, 100, 'Too many API requests'));

// CORS configuration
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
    credentials: true,
    optionsSuccessStatus: 200
}));

// Input sanitization and validation
app.use(express.json({ 
    limit: '10mb',
    verify: (req, res, buf) => {
        if (buf.length > 10 * 1024 * 1024) {
            throw new Error('Request entity too large');
        }
    }
}));
app.use(mongoSanitize()); // Prevent NoSQL injection
app.use(hpp()); // Prevent HTTP Parameter Pollution

// Custom security middleware
app.use((req, res, next) => {
    // Remove sensitive headers
    res.removeHeader('X-Powered-By');
    
    // Add security headers
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    
    next();
});

// Secure session configuration
app.use(session({
    secret: process.env.SESSION_SECRET || throwError('SESSION_SECRET required'),
    name: 'sessionId', // Don't use default 'connect.sid'
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000, // 24 hours
        sameSite: 'strict'
    },
    store: new RedisStore({ /* Redis configuration */ })
}));

// SQL injection prevention
const db = require('better-sqlite3')('app.db', {
    verbose: process.env.NODE_ENV === 'development' ? console.log : null
});

// Prepared statements
const statements = {
    getUserByEmail: db.prepare('SELECT * FROM users WHERE email = ?'),
    getUserById: db.prepare('SELECT * FROM users WHERE id = ?'),
    createUser: db.prepare('INSERT INTO users (email, password_hash) VALUES (?, ?)')
};

// Safe database operations
app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    
    // Input validation
    if (!email || !password) {
        return res.status(400).json({ error: 'Email and password required' });
    }
    
    try {
        const user = statements.getUserByEmail.get(email);
        if (user && await bcrypt.compare(password, user.password_hash)) {
            req.session.userId = user.id;
            res.json({ success: true, user: { id: user.id, email: user.email } });
        } else {
            res.status(401).json({ error: 'Invalid credentials' });
        }
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});
""",
    
    'flask': """
# Enhanced Flask security configuration
from flask import Flask, request, session, jsonify
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_seasurf import SeaSurf
from flask_cors import CORS
import bcrypt
import sqlite3
import os
import secrets

app = Flask(__name__)

# Security configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)
)

# HTTPS enforcement and security headers
Talisman(app, {
    'force_https': app.config.get('ENV') == 'production',
    'strict_transport_security': True,
    'strict_transport_security_max_age': 31536000,
    'content_security_policy': {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com",
        'img-src': "'self' data: https:",
        'connect-src': "'self'",
        'frame-src': "'none'",
        'object-src': "'none'"
    },
    'referrer_policy': 'strict-origin-when-cross-origin'
})

# CORS configuration
CORS(app, {
    'origins': os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(','),
    'supports_credentials': True
})

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

# CSRF protection
SeaSurf(app)

# Database connection with security
def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')  # Enable foreign key constraints
    return conn

# Secure password hashing
class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Input validation
def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Secure login endpoint
@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password required'}), 400
    
    email = data['email'].strip().lower()
    password = data['password']
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    try:
        conn = get_db_connection()
        user = conn.execute(
            'SELECT id, email, password_hash FROM users WHERE email = ?',
            (email,)
        ).fetchone()
        conn.close()
        
        if user and PasswordManager.verify_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session.permanent = True
            return jsonify({
                'success': True,
                'user': {'id': user['id'], 'email': user['email']}
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        app.logger.error(f'Login error: {e}')
        return jsonify({'error': 'Internal server error'}), 500

# Request logging middleware
@app.before_request
def log_request_info():
    app.logger.info('Request: %s %s from %s', 
                   request.method, request.url, request.remote_addr)

# Error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'retry_after': e.retry_after}), 429

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0' if app.config.get('ENV') == 'production' else '127.0.0.1',
        port=int(os.environ.get('PORT', 5000)),
        debug=False  # Never enable debug in production
    )
"""
}
```

**Authentication Implementation**
```python
# Secure password handling
import bcrypt
from datetime import datetime, timedelta
import jwt
import secrets

class SecureAuth:
    def __init__(self):
        self.jwt_secret = os.environ.get('JWT_SECRET', secrets.token_urlsafe(32))
        self.password_min_length = 12
        
    def hash_password(self, password):
        """
        Securely hash password with bcrypt
        """
        # Validate password strength
        if len(password) < self.password_min_length:
            raise ValueError(f"Password must be at least {self.password_min_length} characters")
            
        # Check common passwords
        if password.lower() in self.load_common_passwords():
            raise ValueError("Password is too common")
            
        # Hash with bcrypt (cost factor 12)
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password, hashed):
        """
        Verify password against hash
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def generate_token(self, user_id, expires_in=3600):
        """
        Generate secure JWT token
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)  # Unique token ID
        }
        
        return jwt.encode(
            payload,
            self.jwt_secret,
            algorithm='HS256'
        )
    
    def verify_token(self, token):
        """
        Verify and decode JWT token
        """
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
```

### 8. CI/CD Security Integration

Integrate security scanning into your development pipeline:

**GitHub Actions Security Workflow**
```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Weekly scan on Mondays

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      pull-requests: write
      
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret scanning
          
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install security tools
        run: |
          # Node.js tools
          npm install -g audit-ci @cyclonedx/cli
          
          # Python tools
          pip install safety bandit semgrep pip-audit
          
          # Container tools
          curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
          
          # Secret scanning
          curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
          
      - name: Run secret detection
        run: |
          trufflehog filesystem . --json --no-update > trufflehog-results.json
          
      - name: Upload secret scan results
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: trufflehog-results.json
          
      - name: JavaScript/TypeScript Security Scan
        if: hashFiles('package.json') != ''
        run: |
          npm ci
          
          # Dependency audit
          npm audit --audit-level moderate --json > npm-audit.json || true
          
          # SAST with ESLint Security
          npx eslint . --ext .js,.jsx,.ts,.tsx --format json --output-file eslint-security.json || true
          
          # Generate SBOM
          npx @cyclonedx/cli --type npm --output-format json --output-file sbom-npm.json
          
      - name: Python Security Scan
        if: hashFiles('requirements.txt', 'setup.py', 'pyproject.toml') != ''
        run: |
          # Install dependencies
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          if [ -f setup.py ]; then pip install -e .; fi
          
          # Dependency vulnerability scan
          safety check --json --output safety-results.json || true
          pip-audit --format=json --output=pip-audit-results.json || true
          
          # SAST with Bandit
          bandit -r . -f json -o bandit-results.json || true
          
          # Advanced SAST with Semgrep
          semgrep --config=auto --json --output=semgrep-results.json . || true
          
      - name: Container Security Scan
        if: hashFiles('Dockerfile', 'docker-compose.yml') != ''
        run: |
          # Build image for scanning
          if [ -f Dockerfile ]; then
            docker build -t security-scan:latest .
            
            # Trivy image scan
            trivy image --format sarif --output trivy-image.sarif security-scan:latest
            
            # Trivy filesystem scan
            trivy fs --format sarif --output trivy-fs.sarif .
          fi
          
      - name: Infrastructure as Code Scan
        if: hashFiles('*.tf', '*.yaml', '*.yml') != ''
        run: |
          # Install Checkov
          pip install checkov
          
          # Scan Terraform
          if ls *.tf 1> /dev/null 2>&1; then
            checkov -f *.tf --framework terraform --output sarif > checkov-terraform.sarif || true
          fi
          
          # Scan Kubernetes manifests
          if ls *.yaml *.yml 1> /dev/null 2>&1; then
            checkov -f *.yaml -f *.yml --framework kubernetes --output sarif > checkov-k8s.sarif || true
          fi
          
      - name: Upload scan results to Security tab
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: |
            trivy-image.sarif
            trivy-fs.sarif
            checkov-terraform.sarif
            checkov-k8s.sarif
            
      - name: Generate Security Report
        if: always()
        run: |
          python << 'EOF'
          import json
          import glob
          from datetime import datetime
          
          # Collect all scan results
          results = {
              'timestamp': datetime.now().isoformat(),
              'summary': {'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
              'tools': [],
              'vulnerabilities': []
          }
          
          # Process each result file
          result_files = glob.glob('*-results.json') + glob.glob('*.sarif')
          
          for file in result_files:
              try:
                  with open(file, 'r') as f:
                      data = json.load(f)
                      results['tools'].append(file)
                      # Process based on tool format
                      # (Implementation would parse each tool's output format)
              except:
                  continue
          
          # Generate markdown report
          with open('security-report.md', 'w') as f:
              f.write(f"# Security Scan Report\n\n")
              f.write(f"**Date**: {results['timestamp']}\n\n")
              f.write(f"## Summary\n\n")
              f.write(f"- Total Vulnerabilities: {results['summary']['total']}\n")
              f.write(f"- Critical: {results['summary']['critical']}\n")
              f.write(f"- High: {results['summary']['high']}\n")
              f.write(f"- Medium: {results['summary']['medium']}\n")
              f.write(f"- Low: {results['summary']['low']}\n\n")
              f.write(f"## Tools Used\n\n")
              for tool in results['tools']:
                  f.write(f"- {tool}\n")
          
          print("Security report generated: security-report.md")
          EOF
          
      - name: Comment PR with Security Results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            
            try {
              const report = fs.readFileSync('security-report.md', 'utf8');
              
              await github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: '## 🔒 Security Scan Results\n\n' + report
              });
            } catch (error) {
              console.log('Could not post security report:', error);
            }
            
      - name: Fail on Critical Vulnerabilities
        run: |
          # Check if any critical vulnerabilities found
          CRITICAL_COUNT=$(jq -r '.summary.critical // 0' security-report.json 2>/dev/null || echo "0")
          if [ "$CRITICAL_COUNT" -gt 0 ]; then
            echo "❌ Found $CRITICAL_COUNT critical vulnerabilities!"
            echo "Security scan failed due to critical vulnerabilities."
            exit 1
          fi
          
          HIGH_COUNT=$(jq -r '.summary.high // 0' security-report.json 2>/dev/null || echo "0")
          if [ "$HIGH_COUNT" -gt 5 ]; then
            echo "⚠️ Found $HIGH_COUNT high-severity vulnerabilities!"
            echo "Consider addressing high-severity issues."
            # Don't fail for high-severity, just warn
          fi
          
          echo "✅ Security scan completed successfully!"
```

**Automated Remediation Workflow**
```yaml
# .github/workflows/auto-remediation.yml
name: Automated Security Remediation

on:
  schedule:
    - cron: '0 6 * * 2'  # Weekly on Tuesdays
  workflow_dispatch:
    inputs:
      fix_type:
        description: 'Type of fixes to apply'
        required: true
        default: 'dependencies'
        type: choice
        options:
        - dependencies
        - secrets
        - config
        - all

jobs:
  auto-remediation:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Set up Node.js
        if: hashFiles('package.json') != ''
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          
      - name: Auto-fix npm dependencies
        if: contains(github.event.inputs.fix_type, 'dependencies') || contains(github.event.inputs.fix_type, 'all')
        run: |
          if [ -f package.json ]; then
            npm audit fix --force
            npm update
          fi
          
      - name: Auto-fix Python dependencies
        if: contains(github.event.inputs.fix_type, 'dependencies') || contains(github.event.inputs.fix_type, 'all')
        run: |
          if [ -f requirements.txt ]; then
            pip install pip-tools
            pip-compile --upgrade requirements.in
          fi
          
      - name: Remove detected secrets
        if: contains(github.event.inputs.fix_type, 'secrets') || contains(github.event.inputs.fix_type, 'all')
        run: |
          # Install git-filter-repo
          pip install git-filter-repo
          
          # Create backup branch
          git checkout -b security-remediation-$(date +%Y%m%d)
          
          # Remove common secret patterns (be very careful with this)
          echo "Warning: This would remove secrets from git history"
          echo "Manual review required for production use"
          
      - name: Update security configurations
        if: contains(github.event.inputs.fix_type, 'config') || contains(github.event.inputs.fix_type, 'all')
        run: |
          # Add .gitignore entries for common secret files
          cat >> .gitignore << 'EOF'
          
          # Security - ignore potential secret files
          .env
          .env.local
          .env.*.local
          *.pem
          *.key
          *.p12
          *.pfx
          config/secrets.yml
          config/database.yml
          EOF
          
          # Update Docker security
          if [ -f Dockerfile ]; then
            # Add security improvements to Dockerfile
            echo "RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup" >> Dockerfile.security
            echo "USER appuser" >> Dockerfile.security
          fi
          
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'security: automated vulnerability remediation'
          title: '🔒 Automated Security Fixes'
          body: |
            ## Automated Security Remediation
            
            This PR contains automated fixes for security vulnerabilities:
            
            ### Changes Made
            - ✅ Updated vulnerable dependencies
            - ✅ Added security configurations
            - ✅ Improved .gitignore for secrets
            
            ### Manual Review Required
            - [ ] Verify all dependency updates are compatible
            - [ ] Test application functionality
            - [ ] Review any secret removal changes
            
            **⚠️ Important**: Always test thoroughly before merging automated security fixes.
          branch: security/automated-fixes
          delete-branch: true
```

### 9. Security Report Generation

Generate comprehensive security reports with actionable insights:

**Advanced Reporting System**
```python
import json
import jinja2
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class SecurityMetrics:
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    tools_used: List[str]
    scan_duration: float
    coverage_percentage: float
    false_positive_rate: float

class SecurityReportGenerator:
    def __init__(self):
        self.template_env = jinja2.Environment(
            loader=jinja2.DictLoader({
                'executive_summary': self.EXECUTIVE_TEMPLATE,
                'detailed_report': self.DETAILED_TEMPLATE,
                'dashboard': self.DASHBOARD_TEMPLATE
            })
        )
    
    EXECUTIVE_TEMPLATE = """
# Executive Security Assessment Report

**Assessment Date**: {{ timestamp }}
**Overall Risk Level**: {{ risk_level }}
**Confidence Score**: {{ confidence_score }}%

## Summary
- **Total Vulnerabilities**: {{ metrics.total_vulnerabilities }}
- **Critical**: {{ metrics.critical_count }} ({{ critical_percentage }}%)
- **High**: {{ metrics.high_count }} ({{ high_percentage }}%)
- **Medium**: {{ metrics.medium_count }} ({{ medium_percentage }}%)
- **Low**: {{ metrics.low_count }} ({{ low_percentage }}%)

## Risk Assessment
| Risk Category | Current Level | Target Level | Priority |
|---------------|---------------|--------------|----------|
{% for risk in risk_categories %}
| {{ risk.category }} | {{ risk.current }} | {{ risk.target }} | {{ risk.priority }} |
{% endfor %}

## Immediate Actions Required
{% for action in immediate_actions %}
{{ loop.index }}. **{{ action.title }}** ({{ action.effort }})
   - Impact: {{ action.impact }}
   - Timeline: {{ action.timeline }}
   - Owner: {{ action.owner }}
{% endfor %}

## Compliance Status
{% for framework in compliance_frameworks %}
- **{{ framework.name }}**: {{ framework.status }} ({{ framework.score }}/100)
{% endfor %}

## Investment Required
- **Immediate (0-30 days)**: {{ costs.immediate }}
- **Short-term (1-6 months)**: {{ costs.short_term }}
- **Long-term (6+ months)**: {{ costs.long_term }}
"""
    
    DETAILED_TEMPLATE = """
# Detailed Security Findings Report

## Vulnerability Details
{% for vuln in vulnerabilities %}
### {{ loop.index }}. {{ vuln.title }}

**Severity**: {{ vuln.severity }} | **Confidence**: {{ vuln.confidence }} | **Tool**: {{ vuln.tool }}

**Location**: `{{ vuln.file_path }}:{{ vuln.line_number }}`

**Description**: {{ vuln.description }}

**Impact**: {{ vuln.impact }}

**Remediation**:
```{{ vuln.language }}
{{ vuln.remediation_code }}
```

**References**:
{% for ref in vuln.references %}
- [{{ ref.title }}]({{ ref.url }})
{% endfor %}

---
{% endfor %}

## Tool Effectiveness Analysis
{% for tool in tool_analysis %}
### {{ tool.name }}
- **Vulnerabilities Found**: {{ tool.found_count }}
- **False Positives**: {{ tool.false_positives }}%
- **Execution Time**: {{ tool.execution_time }}s
- **Coverage**: {{ tool.coverage }}%
- **Recommendation**: {{ tool.recommendation }}
{% endfor %}
"""
    
    def generate_comprehensive_report(self, scan_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate all report formats"""
        # Process scan results
        metrics = self._calculate_metrics(scan_results)
        risk_assessment = self._assess_risk(scan_results, metrics)
        compliance_status = self._check_compliance(scan_results)
        
        # Generate different report formats
        reports = {
            'executive_summary': self._generate_executive_summary(
                metrics, risk_assessment, compliance_status
            ),
            'detailed_report': self._generate_detailed_report(scan_results),
            'json_report': json.dumps({
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'version': '2.0',
                    'format': 'sarif-2.1.0'
                },
                'metrics': metrics.__dict__,
                'vulnerabilities': scan_results.get('vulnerabilities', []),
                'risk_assessment': risk_assessment,
                'compliance': compliance_status
            }, indent=2),
            'sarif_report': self._generate_sarif_report(scan_results)
        }
        
        return reports
    
    def _calculate_metrics(self, scan_results: Dict[str, Any]) -> SecurityMetrics:
        """Calculate security metrics from scan results"""
        vulnerabilities = scan_results.get('vulnerabilities', [])
        
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN').upper()
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        return SecurityMetrics(
            total_vulnerabilities=len(vulnerabilities),
            critical_count=severity_counts['CRITICAL'],
            high_count=severity_counts['HIGH'],
            medium_count=severity_counts['MEDIUM'],
            low_count=severity_counts['LOW'],
            tools_used=scan_results.get('tools_used', []),
            scan_duration=scan_results.get('scan_duration', 0),
            coverage_percentage=scan_results.get('coverage', 0),
            false_positive_rate=scan_results.get('false_positive_rate', 0)
        )
    
    def _assess_risk(self, scan_results: Dict[str, Any], metrics: SecurityMetrics) -> Dict[str, Any]:
        """Perform comprehensive risk assessment"""
        # Calculate risk score (0-100)
        risk_score = min(100, (
            metrics.critical_count * 25 +
            metrics.high_count * 15 +
            metrics.medium_count * 5 +
            metrics.low_count * 1
        ))
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = 'CRITICAL'
        elif risk_score >= 60:
            risk_level = 'HIGH'
        elif risk_score >= 30:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Business impact assessment
        business_impact = {
            'data_breach_probability': min(95, risk_score + metrics.critical_count * 10),
            'service_disruption_risk': min(90, risk_score * 0.8),
            'compliance_violation_risk': min(100, risk_score + (metrics.critical_count * 5)),
            'reputation_damage_potential': min(85, risk_score * 0.9)
        }
        
        return {
            'score': risk_score,
            'level': risk_level,
            'business_impact': business_impact,
            'trending': self._calculate_risk_trend(scan_results),
            'peer_comparison': self._compare_with_industry_standards(risk_score)
        }
    
    def _generate_sarif_report(self, scan_results: Dict[str, Any]) -> str:
        """Generate SARIF 2.1.0 compliant report"""
        sarif_report = {
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": []
        }
        
        # Group findings by tool
        tools_data = {}
        for vuln in scan_results.get('vulnerabilities', []):
            tool = vuln.get('tool', 'unknown')
            if tool not in tools_data:
                tools_data[tool] = []
            tools_data[tool].append(vuln)
        
        # Create run for each tool
        for tool_name, vulnerabilities in tools_data.items():
            run = {
                "tool": {
                    "driver": {
                        "name": tool_name,
                        "version": "1.0.0",
                        "informationUri": f"https://docs.{tool_name}.com"
                    }
                },
                "results": []
            }
            
            for vuln in vulnerabilities:
                result = {
                    "ruleId": vuln.get('type', 'unknown'),
                    "message": {
                        "text": vuln.get('description', vuln.get('title', 'Security issue detected'))
                    },
                    "level": self._map_severity_to_sarif_level(vuln.get('severity', 'medium')),
                    "locations": [{
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": vuln.get('file_path', 'unknown')
                            },
                            "region": {
                                "startLine": vuln.get('line_number', 1)
                            }
                        }
                    }]
                }
                
                if vuln.get('cwe'):
                    result["properties"] = {
                        "cwe": vuln.get('cwe'),
                        "confidence": vuln.get('confidence', 'medium')
                    }
                
                run["results"].append(result)
            
            sarif_report["runs"].append(run)
        
        return json.dumps(sarif_report, indent=2)
    
    def _map_severity_to_sarif_level(self, severity: str) -> str:
        """Map severity to SARIF level"""
        mapping = {
            'CRITICAL': 'error',
            'HIGH': 'error',
            'MEDIUM': 'warning',
            'LOW': 'note'
        }
        return mapping.get(severity.upper(), 'warning')

# Usage example
report_generator = SecurityReportGenerator()

# Sample scan results
sample_results = {
    'vulnerabilities': [
        {
            'tool': 'bandit',
            'severity': 'HIGH',
            'title': 'SQL Injection vulnerability',
            'description': 'Parameterized query missing',
            'file_path': 'api/users.py',
            'line_number': 45,
            'cwe': 'CWE-89'
        }
    ],
    'tools_used': ['bandit', 'safety', 'trivy'],
    'scan_duration': 120.5,
    'coverage': 85.2
}

reports = report_generator.generate_comprehensive_report(sample_results)
```

**Executive Summary**
```markdown
## Security Assessment Report

**Date**: 2025-07-19
**Severity**: CRITICAL
**Confidence**: 94%

### Summary
- Total Vulnerabilities: 47
- Critical: 8 (17%)
- High: 15 (32%)
- Medium: 18 (38%)
- Low: 6 (13%)

### Critical Findings
1. **SQL Injection** in user search endpoint (api/search.py:45)
2. **Hardcoded AWS credentials** in config.js:12
3. **Outdated dependencies** with known RCE vulnerabilities
4. **Missing authentication** on admin endpoints

### Business Impact
| Risk Category | Probability | Impact | Priority |
|---------------|-------------|--------|----------|
| Data Breach | 85% | Critical | P0 |
| Service Disruption | 60% | High | P1 |
| Compliance Violation | 90% | Critical | P0 |
| Reputation Damage | 70% | High | P1 |

### Immediate Actions Required (Next 24 Hours)
1. **Patch SQL injection vulnerability** (2 hours) - [@dev-team]
2. **Remove and rotate all hardcoded credentials** (1 hour) - [@security-team]
3. **Block admin endpoints** until auth is implemented (30 minutes) - [@ops-team]

### Short-term Actions (Next 30 Days)
1. **Update critical dependencies** (4 hours)
2. **Implement authentication middleware** (6 hours)
3. **Deploy security headers** (2 hours)
4. **Security training for development team** (8 hours)

### Investment Required
- **Immediate fixes**: $5,000 (40 hours @ $125/hr)
- **Security improvements**: $15,000 (120 hours)
- **Training and processes**: $10,000
- **Total**: $30,000

### Compliance Status
- **OWASP Top 10**: 3/10 major issues
- **SOC 2**: Non-compliant (authentication controls)
- **PCI DSS**: Non-compliant (data protection)
- **GDPR**: At risk (data breach potential)
```

**Detailed Findings with Remediation Code**
```json
{
  "scan_metadata": {
    "timestamp": "2025-07-19T10:30:00Z",
    "version": "2.1",
    "tools_used": ["bandit", "safety", "trivy", "semgrep", "eslint-security"],
    "scan_duration_seconds": 127,
    "coverage_percentage": 94.2,
    "false_positive_rate": 3.1
  },
  "vulnerabilities": [
    {
      "id": "VULN-001",
      "type": "SQL Injection",
      "severity": "CRITICAL",
      "cvss_score": 9.8,
      "cwe": "CWE-89",
      "owasp_category": "A03:2021-Injection",
      "tool": "semgrep",
      "confidence": "high",
      "location": {
        "file": "api/search.js",
        "line": 45,
        "column": 12,
        "code_snippet": "db.query(`SELECT * FROM users WHERE name LIKE '%${req.query.search}%'`)",
        "function": "searchUsers"
      },
      "impact": {
        "description": "Complete database compromise, data exfiltration, potential RCE",
        "business_impact": "Critical - customer data exposure, regulatory violations",
        "affected_users": "All users with search functionality access"
      },
      "remediation": {
        "effort_hours": 2,
        "priority": "P0",
        "description": "Replace string concatenation with parameterized queries",
        "fixed_code": "db.query('SELECT * FROM users WHERE name LIKE ?', [`%${req.query.search}%`])",
        "testing_required": "Unit tests for search functionality",
        "deployment_notes": "No breaking changes, safe to deploy immediately"
      },
      "references": [
        {
          "title": "OWASP SQL Injection Prevention",
          "url": "https://owasp.org/www-community/attacks/SQL_Injection"
        },
        {
          "title": "Node.js Parameterized Queries",
          "url": "https://nodejs.org/en/docs/guides/security/"
        }
      ],
      "exploitability": {
        "ease_of_exploitation": "Very Easy",
        "attack_vector": "Remote",
        "authentication_required": false,
        "user_interaction": false
      }
    },
    {
      "id": "VULN-002",
      "type": "Hardcoded Secrets",
      "severity": "CRITICAL",
      "cvss_score": 9.1,
      "cwe": "CWE-798",
      "tool": "trufflehog",
      "confidence": "verified",
      "location": {
        "file": "config/database.js",
        "line": 12,
        "code_snippet": "const password = 'MyS3cr3tP@ssw0rd123!'"
      },
      "impact": {
        "description": "Database credentials exposure, unauthorized access",
        "business_impact": "Critical - full database access, data breach potential"
      },
      "remediation": {
        "effort_hours": 1,
        "priority": "P0",
        "immediate_actions": [
          "Rotate database password immediately",
          "Remove hardcoded credential from code",
          "Implement environment variable loading"
        ],
        "fixed_code": "const password = process.env.DATABASE_PASSWORD || throwError('Missing DATABASE_PASSWORD')",
        "additional_steps": [
          "Add .env to .gitignore",
          "Update deployment scripts to use secrets management",
          "Scan git history for credential exposure"
        ]
      }
    },
    {
      "id": "VULN-003",
      "type": "Vulnerable Dependency",
      "severity": "HIGH",
      "cvss_score": 8.5,
      "cve": "CVE-2024-1234",
      "tool": "npm-audit",
      "location": {
        "file": "package.json",
        "dependency": "express",
        "version": "4.17.1",
        "vulnerable_path": "express > body-parser > raw-body"
      },
      "impact": {
        "description": "Remote code execution via malformed request body",
        "affected_endpoints": ["/api/upload", "/api/webhook"]
      },
      "remediation": {
        "effort_hours": 0.5,
        "priority": "P1",
        "fixed_version": "4.18.2",
        "update_command": "npm install express@4.18.2",
        "breaking_changes": false,
        "testing_required": "Regression testing for API endpoints"
      }
    }
  ],
  "summary": {
    "total_vulnerabilities": 47,
    "by_severity": {
      "critical": 8,
      "high": 15,
      "medium": 18,
      "low": 6
    },
    "by_category": {
      "injection": 12,
      "broken_auth": 8,
      "sensitive_data": 6,
      "xml_entities": 2,
      "broken_access_control": 5,
      "security_misconfig": 9,
      "xss": 3,
      "insecure_deserialization": 1,
      "vulnerable_components": 15,
      "insufficient_logging": 4
    },
    "remediation_timeline": {
      "immediate_p0": 9,
      "urgent_p1": 18,
      "medium_p2": 15,
      "low_p3": 5
    },
    "total_effort_hours": 47.5,
    "estimated_cost": 5938,
    "risk_score": 89
  },
  "compliance_assessment": {
    "owasp_top_10_2021": {
      "a01_broken_access_control": "FAIL",
      "a02_cryptographic_failures": "PASS",
      "a03_injection": "FAIL",
      "a04_insecure_design": "WARNING",
      "a05_security_misconfiguration": "FAIL",
      "a06_vulnerable_components": "FAIL",
      "a07_identification_failures": "FAIL",
      "a08_software_integrity_failures": "PASS",
      "a09_logging_failures": "WARNING",
      "a10_ssrf": "PASS"
    },
    "frameworks": {
      "nist_cybersecurity": 67,
      "iso_27001": 71,
      "pci_dss": 45,
      "sox_compliance": 78
    }
  }
}
```

### 10. Cross-Command Integration

### Complete Security-First Development Workflow

**Secure API Development Pipeline**
```bash
# 1. Generate secure API scaffolding
/api-scaffold
framework: "fastapi"
security_features: ["jwt_auth", "rate_limiting", "input_validation", "cors"]
database: "postgresql"

# 2. Run comprehensive security scan
/security-scan
scan_types: ["sast", "dependency", "secrets", "container", "iac"]
autofix: true
generate_report: true

# 3. Generate security-aware tests
/test-harness
test_types: ["unit", "security", "penetration"]
security_frameworks: ["bandit", "safety", "owasp-zap"]

# 4. Optimize containers with security hardening
/docker-optimize
security_hardening: true
vulnerability_scanning: true
minimal_base_images: true
```

**Integrated Security Configuration**
```python
# security-config.py - Shared across all commands
class IntegratedSecurityConfig:
    def __init__(self):
        self.api_security = self.load_api_security_config()    # From /api-scaffold
        self.scan_config = self.load_scan_config()             # From /security-scan
        self.test_security = self.load_test_security_config()  # From /test-harness
        self.container_security = self.load_container_config() # From /docker-optimize
        
    def generate_security_middleware(self):
        """Generate security middleware based on API scaffold config"""
        middleware = []
        
        if self.api_security.get('rate_limiting'):
            middleware.append({
                'type': 'rate_limiting',
                'config': {
                    'requests_per_minute': 100,
                    'burst_size': 10,
                    'key_func': 'lambda request: request.client.host'
                }
            })
        
        if self.api_security.get('jwt_auth'):
            middleware.append({
                'type': 'jwt_auth',
                'config': {
                    'secret_key': '${JWT_SECRET_KEY}',
                    'algorithm': 'HS256',
                    'token_expiry': 3600
                }
            })
        
        return middleware
    
    def generate_security_tests(self):
        """Generate security tests based on scan findings"""
        test_cases = []
        
        # SQL Injection tests based on API endpoints
        api_endpoints = self.api_security.get('endpoints', [])
        for endpoint in api_endpoints:
            if endpoint.get('accepts_input'):
                test_cases.append({
                    'type': 'sql_injection',
                    'endpoint': endpoint['path'],
                    'payloads': self.get_sql_injection_payloads()
                })
        
        # Authentication bypass tests
        if self.api_security.get('jwt_auth'):
            test_cases.append({
                'type': 'auth_bypass',
                'scenarios': [
                    'invalid_token',
                    'expired_token',
                    'malformed_token',
                    'no_token'
                ]
            })
        
        return test_cases
    
    def generate_container_security_policies(self):
        """Generate container security policies"""
        policies = {
            'dockerfile_security': {
                'non_root_user': True,
                'minimal_layers': True,
                'security_updates': True,
                'no_secrets_in_layers': True
            },
            'runtime_security': {
                'read_only_filesystem': True,
                'no_new_privileges': True,
                'drop_capabilities': ['ALL'],
                'add_capabilities': ['NET_BIND_SERVICE'] if self.api_security.get('bind_privileged_ports') else []
            }
        }
        return policies
```

**API Security Integration**
```python
# Generated secure API endpoint with integrated security
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import jwt
from datetime import datetime, timedelta

# Security configuration from /security-scan
security_config = IntegratedSecurityConfig()

# Rate limiting from security scan recommendations
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# JWT authentication from security scan requirements
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT verification with security scan compliance"""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            security_config.jwt_secret, 
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Secure endpoint with integrated protections
@app.post("/api/v1/users/")
@limiter.limit("10/minute")  # Rate limiting from security scan
async def create_user(
    request: Request,
    user_data: UserCreateSchema,  # Input validation from security scan
    current_user: dict = Depends(verify_token)  # Authentication
):
    """
    Secure user creation endpoint with integrated security controls
    Security features applied:
    - Rate limiting (10 requests/minute)
    - JWT authentication required
    - Input validation via Pydantic
    - SQL injection prevention via ORM
    - XSS prevention via output encoding
    """
    # Additional security validation from scan results
    if not validate_user_input(user_data):
        raise HTTPException(status_code=400, detail="Invalid input data")
    
    # Create user with security logging
    try:
        user = await user_service.create_user(user_data)
        security_logger.log_user_creation(current_user['sub'], user.id)
        return user
    except Exception as e:
        security_logger.log_error("user_creation_failed", str(e))
        raise HTTPException(status_code=500, detail="User creation failed")
```

**Database Security Integration**
```python
# Database security configuration from /db-migrate and /security-scan
class SecureDatabaseConfig:
    def __init__(self):
        self.migration_config = self.load_migration_config()  # From /db-migrate
        self.security_requirements = self.load_security_scan_results()
        
    def generate_secure_migrations(self):
        """Generate database migrations with security controls"""
        migrations = []
        
        # User table with security controls
        migrations.append({
            'operation': 'create_table',
            'table': 'users',
            'columns': [
                {'name': 'id', 'type': 'UUID', 'primary_key': True},
                {'name': 'email', 'type': 'VARCHAR(255)', 'unique': True, 'encrypted': True},
                {'name': 'password_hash', 'type': 'VARCHAR(255)', 'not_null': True},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'default': 'NOW()'},
                {'name': 'last_login', 'type': 'TIMESTAMP'},
                {'name': 'failed_login_attempts', 'type': 'INTEGER', 'default': 0},
                {'name': 'locked_until', 'type': 'TIMESTAMP', 'nullable': True}
            ],
            'security_features': {
                'row_level_security': True,
                'audit_logging': True,
                'field_encryption': ['email'],
                'password_policy': {
                    'min_length': 12,
                    'require_special_chars': True,
                    'require_numbers': True,
                    'expire_days': 90
                }
            }
        })
        
        # Security audit log table
        migrations.append({
            'operation': 'create_table',
            'table': 'security_audit_log',
            'columns': [
                {'name': 'id', 'type': 'UUID', 'primary_key': True},
                {'name': 'user_id', 'type': 'UUID', 'foreign_key': 'users.id'},
                {'name': 'action', 'type': 'VARCHAR(100)', 'not_null': True},
                {'name': 'ip_address', 'type': 'INET', 'not_null': True},
                {'name': 'user_agent', 'type': 'TEXT'},
                {'name': 'timestamp', 'type': 'TIMESTAMP', 'default': 'NOW()'},
                {'name': 'success', 'type': 'BOOLEAN', 'not_null': True},
                {'name': 'details', 'type': 'JSONB'}
            ],
            'indexes': [
                {'name': 'idx_audit_user_timestamp', 'columns': ['user_id', 'timestamp']},
                {'name': 'idx_audit_action_timestamp', 'columns': ['action', 'timestamp']}
            ]
        })
        
        return migrations
```

**Container Security Integration**
```dockerfile
# Dockerfile.secure - Generated with /docker-optimize + /security-scan
# Multi-stage build with security hardening
FROM python:3.11-slim-bookworm AS base

# Security: Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Security: Update packages and remove package manager cache
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        # Only essential packages
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Security: Set work directory with proper permissions
WORKDIR /app
RUN chown appuser:appuser /app

# Install Python dependencies with security checks
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    # Security scan dependencies during build
    pip-audit --format=json --output=/tmp/pip-audit.json && \
    safety check --json --output=/tmp/safety.json

# Copy application code
COPY --chown=appuser:appuser . .

# Security: Remove any secrets or sensitive files
RUN find . -name "*.key" -delete && \
    find . -name "*.pem" -delete && \
    find . -name ".env*" -delete

# Security: Switch to non-root user
USER appuser

# Security: Read-only filesystem, no new privileges
# These will be enforced at runtime via Kubernetes security context

EXPOSE 8000

# Health check for container security monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Kubernetes Security Integration**
```yaml
# k8s-secure-deployment.yaml - From /k8s-manifest + /security-scan
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-service-account
  namespace: production
automountServiceAccountToken: false

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
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
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []  # DNS
    ports:
    - protocol: UDP
      port: 53

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
      annotations:
        # Security scanning annotations
        container.apparmor.security.beta.kubernetes.io/api: runtime/default
    spec:
      serviceAccountName: api-service-account
      securityContext:
        # Pod-level security context
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: api
        image: api:secure-latest
        ports:
        - containerPort: 8000
        securityContext:
          # Container-level security context
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: secret
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: var-log
          mountPath: /var/log
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
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: var-log
        emptyDir: {}

---
# Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: api-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  allowedCapabilities:
    - NET_BIND_SERVICE
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

**CI/CD Security Integration**
```yaml
# .github/workflows/security-pipeline.yml
name: Integrated Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    # 1. Code Security Scanning
    - name: Run Bandit Security Scan
      run: |
        pip install bandit[toml]
        bandit -r . -f sarif -o bandit-results.sarif
    
    - name: Run Semgrep Security Scan
      uses: returntocorp/semgrep-action@v1
      with:
        config: auto
        generateSarif: "1"
    
    # 2. Dependency Security Scanning
    - name: Run Safety Check
      run: |
        pip install safety
        safety check --json --output safety-results.json
    
    - name: Run npm audit
      if: hashFiles('package.json') != ''
      run: |
        npm audit --audit-level high --json > npm-audit-results.json
    
    # 3. Container Security Scanning
    - name: Build Container
      run: docker build -t app:security-test .
    
    - name: Run Trivy Container Scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'app:security-test'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    # 4. Infrastructure Security Scanning
    - name: Run Checkov IaC Scan
      uses: bridgecrewio/checkov-action@master
      with:
        directory: .
        output_format: sarif
        output_file_path: checkov-results.sarif
    
    # 5. Secret Scanning
    - name: Run TruffleHog Secret Scan
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
        head: HEAD
        extra_args: --format=sarif --output=trufflehog-results.sarif
    
    # 6. Upload Security Results
    - name: Upload SARIF results to GitHub
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: |
          bandit-results.sarif
          semgrep.sarif
          trivy-results.sarif
          checkov-results.sarif
          trufflehog-results.sarif
    
    # 7. Security Test Integration
    - name: Run Security Tests
      run: |
        pytest tests/security/ -v --cov=src/security
        
    # 8. Generate Security Report
    - name: Generate Security Dashboard
      run: |
        python scripts/generate_security_report.py \
          --bandit bandit-results.sarif \
          --semgrep semgrep.sarif \
          --trivy trivy-results.sarif \
          --safety safety-results.json \
          --output security-dashboard.html
    
    - name: Upload Security Dashboard
      uses: actions/upload-artifact@v3
      with:
        name: security-dashboard
        path: security-dashboard.html

  penetration-testing:
    runs-on: ubuntu-latest
    needs: security-scan
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    
    # Start application for dynamic testing
    - name: Start Application
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 30  # Wait for startup
    
    # OWASP ZAP Dynamic Testing
    - name: Run OWASP ZAP Scan
      uses: zaproxy/action-full-scan@v0.4.0
      with:
        target: 'http://localhost:8000'
        rules_file_name: '.zap/rules.tsv'
        cmd_options: '-a -j -m 10 -T 60'
        
    # API Security Testing
    - name: Run API Security Tests
      run: |
        pip install requests pytest
        pytest tests/api_security/ -v
```

**Monitoring and Alerting Integration**
```python
# security_monitoring.py - Integrated with all commands
import logging
from datetime import datetime
from typing import Dict, Any
import json

class IntegratedSecurityMonitor:
    """Security monitoring that integrates with all command outputs"""
    
    def __init__(self):
        self.api_endpoints = self.load_api_endpoints()      # From /api-scaffold
        self.container_metrics = self.load_container_config() # From /docker-optimize
        self.k8s_security = self.load_k8s_security()        # From /k8s-manifest
        
    def monitor_api_security(self):
        """Monitor API security events"""
        security_events = []
        
        # Monitor authentication failures
        auth_failures = self.get_auth_failure_rate()
        if auth_failures > 10:  # More than 10 failures per minute
            security_events.append({
                'type': 'AUTH_FAILURE_SPIKE',
                'severity': 'HIGH',
                'details': f'Authentication failure rate: {auth_failures}/min',
                'recommended_action': 'Check for brute force attacks'
            })
        
        # Monitor rate limiting violations
        rate_limit_violations = self.get_rate_limit_violations()
        if rate_limit_violations:
            security_events.append({
                'type': 'RATE_LIMIT_VIOLATION',
                'severity': 'MEDIUM',
                'details': f'Rate limit violations: {len(rate_limit_violations)}',
                'ips': [v['ip'] for v in rate_limit_violations],
                'recommended_action': 'Consider IP blocking or CAPTCHA'
            })
        
        return security_events
    
    def monitor_container_security(self):
        """Monitor container security events"""
        container_events = []
        
        # Check for privilege escalation attempts
        privilege_events = self.check_privilege_escalation()
        if privilege_events:
            container_events.append({
                'type': 'PRIVILEGE_ESCALATION',
                'severity': 'CRITICAL',
                'containers': privilege_events,
                'recommended_action': 'Immediate investigation required'
            })
        
        # Check for filesystem violations
        readonly_violations = self.check_readonly_violations()
        if readonly_violations:
            container_events.append({
                'type': 'READONLY_VIOLATION',
                'severity': 'HIGH',
                'violations': readonly_violations,
                'recommended_action': 'Review container security policies'
            })
        
        return container_events
    
    def generate_security_dashboard(self) -> Dict[str, Any]:
        """Generate comprehensive security dashboard"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'api_security': self.monitor_api_security(),
            'container_security': self.monitor_container_security(),
            'scan_results': self.get_latest_scan_results(),
            'test_results': self.get_security_test_results(),
            'compliance_status': self.check_compliance_status(),
            'recommendations': self.generate_recommendations()
        }
```

This integrated approach ensures that security is built into every aspect of the application lifecycle, from development through deployment and monitoring.

## Output Format

1. **Tool Selection Matrix**: Recommended tools based on technology stack
2. **Comprehensive Scan Results**: Multi-tool aggregated findings
3. **Executive Security Report**: Business-focused risk assessment
4. **Detailed Technical Findings**: Code-level vulnerabilities with fixes
5. **SARIF Compliance Report**: Industry-standard security report format
6. **Automated Remediation Scripts**: Ready-to-run fix implementations
7. **CI/CD Integration Workflows**: Complete GitHub Actions security pipeline
8. **Compliance Assessment**: OWASP, NIST, ISO 27001 compliance mapping
9. **Business Impact Analysis**: Risk quantification and cost estimates
10. **Monitoring and Alerting Setup**: Real-time security event detection

**Key Features**:
- ✅ **Multi-tool integration**: Bandit, Safety, Trivy, Semgrep, ESLint Security, Snyk
- ✅ **Automated remediation**: Smart dependency updates and configuration fixes
- ✅ **CI/CD ready**: Complete GitHub Actions workflows with SARIF uploads
- ✅ **Business context**: Risk scoring with financial impact estimates
- ✅ **Framework-specific**: Tailored security patterns for Django, Flask, React, Express
- ✅ **Compliance-focused**: Built-in OWASP Top 10, CWE, and regulatory mappings
- ✅ **Actionable insights**: Specific remediation code and deployment guidance

Focus on actionable remediation that can be implemented immediately while maintaining application functionality.