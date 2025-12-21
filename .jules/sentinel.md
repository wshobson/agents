## 2024-12-21 - [Secure Defaults in Templates]
**Vulnerability:** The "Production-ready" REST API template lacked CORS configuration and password hashing, potentially leading developers to deploy insecure applications.
**Learning:** Educational templates are often copied directly into production. If they lack security defaults (like CORS restriction or password hashing placeholders), they propagate vulnerabilities.
**Prevention:** All code templates, even mocks, must include explicit security controls (e.g., specific CORS origins instead of wildcard) and comments warning about missing implementation details (like hashing).
