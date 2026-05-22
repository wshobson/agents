---
name: python-configuration
description: Python configuration management via environment variables and typed settings. Use when externalizing config, setting up pydantic-settings, managing secrets, or implementing environment-specific behavior.
---

# Python Configuration Management

Externalize configuration from code using environment variables and typed settings. Well-managed configuration enables the same code to run in any environment without modification.

## When to Use This Skill

- Setting up a new project's configuration system
- Migrating from hardcoded values to environment variables
- Implementing pydantic-settings for typed configuration
- Managing secrets and sensitive values
- Creating environment-specific settings (dev/staging/prod)
- Validating configuration at application startup

## Core Concepts

### 1. Externalized Configuration

All environment-specific values (URLs, secrets, feature flags) come from environment variables, not code.

### 2. Typed Settings

Parse and validate configuration into typed objects at startup, not scattered throughout code.

### 3. Fail Fast

Validate all required configuration at application boot. Missing config should crash immediately with a clear message.

### 4. Sensible Defaults

Provide reasonable defaults for local development while requiring explicit values for sensitive settings.

## Quick Start

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    api_key: str = Field(alias="API_KEY")
    debug: bool = Field(default=False, alias="DEBUG")

settings = Settings()  # Loads from environment
```

## Fundamental Patterns

### Pattern 1: Typed Settings with Pydantic

Create a central settings class that loads and validates all configuration.

```python
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, ValidationError
import sys

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Database
    db_host: str = Field(alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")

    # API Keys
    api_secret_key: str = Field(alias="API_SECRET_KEY")

    # Feature flags
    enable_new_feature: bool = Field(default=False, alias="ENABLE_NEW_FEATURE")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

# Create singleton instance at module load
try:
    settings = Settings()
except ValidationError as e:
    print(f"Configuration error:\n{e}")
    sys.exit(1)
```

Import `settings` throughout your application:

```python
from myapp.config import settings

def get_database_connection():
    return connect(
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )
```

### Pattern 2: Fail Fast on Missing Configuration

Required settings should crash the application immediately with a clear error.

```python
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError
import sys

class Settings(BaseSettings):
    # Required - no default means it must be set
    api_key: str = Field(alias="API_KEY")
    database_url: str = Field(alias="DATABASE_URL")

    # Optional with defaults
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

try:
    settings = Settings()
except ValidationError as e:
    print("=" * 60)
    print("CONFIGURATION ERROR")
    print("=" * 60)
    for error in e.errors():
        field = error["loc"][0]
        print(f"  - {field}: {error['msg']}")
    print("\nPlease set the required environment variables.")
    sys.exit(1)
```

A clear error at startup is better than a cryptic `None` failure mid-request.

### Pattern 3: Local Development Defaults

Provide sensible defaults for local development while requiring explicit values for secrets.

```python
class Settings(BaseSettings):
    # Has local default, but prod will override
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")

    # Always required - no default for secrets
    db_password: str = Field(alias="DB_PASSWORD")
    api_secret_key: str = Field(alias="API_SECRET_KEY")

    # Development convenience
    debug: bool = Field(default=False, alias="DEBUG")

    model_config = {"env_file": ".env"}
```

Create a `.env` file for local development (never commit this):

```bash
# .env (add to .gitignore)
DB_PASSWORD=local_dev_password
API_SECRET_KEY=dev-secret-key
DEBUG=true
```

### Pattern 4: Namespaced Environment Variables

Prefix related variables for clarity and easy debugging.

```bash
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=admin
DB_PASSWORD=secret

# Redis configuration
REDIS_URL=redis://localhost:6379
REDIS_MAX_CONNECTIONS=10

# Authentication
AUTH_SECRET_KEY=your-secret-key
AUTH_TOKEN_EXPIRY_SECONDS=3600
AUTH_ALGORITHM=HS256

# Feature flags
FEATURE_NEW_CHECKOUT=true
FEATURE_BETA_UI=false
```

Makes `env | grep DB_` useful for debugging.

## Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Best Practices Summary

1. **Never hardcode config** - All environment-specific values from env vars
2. **Use typed settings** - Pydantic-settings with validation
3. **Fail fast** - Crash on missing required config at startup
4. **Provide dev defaults** - Make local development easy
5. **Never commit secrets** - Use `.env` files (gitignored) or secret managers
6. **Namespace variables** - `DB_HOST`, `REDIS_URL` for clarity
7. **Import settings singleton** - Don't call `os.getenv()` throughout code
8. **Document all variables** - README should list required env vars
9. **Validate early** - Check config correctness at boot time
10. **Use secrets_dir** - Support mounted secrets in containers
