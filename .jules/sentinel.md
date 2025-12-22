## 2024-05-23 - Default Security Middleware in FastAPI Templates
**Vulnerability:** Missing default security headers and CORS configuration in API templates.
**Learning:** Developers often copy templates directly into production. If templates lack security headers by default, new services will be insecure.
**Prevention:** Always include `TrustedHostMiddleware` and `CORSMiddleware` in API templates with strict comments on how to configure them for production. Use safe defaults where possible, but permissive defaults with warnings (like `*`) are acceptable for templates if clearly marked with TODOs.
