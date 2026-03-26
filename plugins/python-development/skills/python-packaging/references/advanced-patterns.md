# Python Packaging — Advanced Reference

Advanced packaging patterns including data files, namespace packages, C extensions, version management, testing installation, documentation templates, and distribution workflows.

## Pattern 11: Including Data Files

```toml
[tool.setuptools.package-data]
my_package = [
    "data/*.json",
    "templates/*.html",
    "static/css/*.css",
    "py.typed",
]
```

**Accessing data files:**

```python
# src/my_package/loader.py
from importlib.resources import files
import json

def load_config():
    """Load configuration from package data."""
    config_file = files("my_package").joinpath("data/config.json")
    with config_file.open() as f:
        return json.load(f)

# Python 3.9+
from importlib.resources import files

data = files("my_package").joinpath("data/file.txt").read_text()
```

## Pattern 12: Namespace Packages

**For large projects split across multiple repositories:**

```
# Package 1: company-core
company/
└── core/
    ├── __init__.py
    └── models.py

# Package 2: company-api
company/
└── api/
    ├── __init__.py
    └── routes.py
```

**Do NOT include __init__.py in the namespace directory (company/):**

```toml
# company-core/pyproject.toml
[project]
name = "company-core"

[tool.setuptools.packages.find]
where = ["."]
include = ["company.core*"]

# company-api/pyproject.toml
[project]
name = "company-api"

[tool.setuptools.packages.find]
where = ["."]
include = ["company.api*"]
```

**Usage:**

```python
# Both packages can be imported under same namespace
from company.core import models
from company.api import routes
```

## Pattern 13: C Extensions

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "Cython>=0.29"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
ext-modules = [
    {name = "my_package.fast_module", sources = ["src/fast_module.c"]},
]
```

**Or with setup.py:**

```python
# setup.py
from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            "my_package.fast_module",
            sources=["src/fast_module.c"],
            include_dirs=["src/include"],
        )
    ]
)
```

## Version Management

### Pattern 14: Semantic Versioning

```python
# src/my_package/__init__.py
__version__ = "1.2.3"

# Semantic versioning: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features (backward compatible)
# PATCH: Bug fixes
```

**Version constraints in dependencies:**

```toml
dependencies = [
    "requests>=2.28.0,<3.0.0",  # Compatible range
    "click~=8.1.0",              # Compatible release (~= 8.1.0 means >=8.1.0,<8.2.0)
    "pydantic>=2.0",             # Minimum version
    "numpy==1.24.3",             # Exact version (avoid if possible)
]
```

### Pattern 15: Git-Based Versioning

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "src/my_package/_version.py"
version_scheme = "post-release"
local_scheme = "dirty-tag"
```

**Creates versions like:**

- `1.0.0` (from git tag)
- `1.0.1.dev3+g1234567` (3 commits after tag)

## Testing Installation

### Pattern 16: Editable Install

```bash
# Install in development mode
pip install -e .

# With optional dependencies
pip install -e ".[dev]"
pip install -e ".[dev,docs]"

# Now changes to source code are immediately reflected
```

### Pattern 17: Testing in Isolated Environment

```bash
# Create virtual environment
python -m venv test-env
source test-env/bin/activate  # Linux/Mac
# test-env\Scripts\activate  # Windows

# Install package
pip install dist/my_package-1.0.0-py3-none-any.whl

# Test it works
python -c "import my_package; print(my_package.__version__)"

# Test CLI
my-tool --help

# Cleanup
deactivate
rm -rf test-env
```

## Documentation

### Pattern 18: README.md Template

````markdown
# My Package

[![PyPI version](https://badge.fury.io/py/my-package.svg)](https://pypi.org/project/my-package/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-package.svg)](https://pypi.org/project/my-package/)
[![Tests](https://github.com/username/my-package/workflows/Tests/badge.svg)](https://github.com/username/my-package/actions)

Brief description of your package.

## Installation

```bash
pip install my-package
```

## Quick Start

```python
from my_package import something

result = something.do_stuff()
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

Full documentation: https://my-package.readthedocs.io

## Development

```bash
git clone https://github.com/username/my-package.git
cd my-package
pip install -e ".[dev]"
pytest
```

## License

MIT
````

## Common Patterns

### Pattern 19: Multi-Architecture Wheels

```yaml
# .github/workflows/wheels.yml
name: Build wheels

on: [push, pull_request]

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Build wheels
        uses: pypa/cibuildwheel@v2.16.2

      - uses: actions/upload-artifact@v3
        with:
          path: ./wheelhouse/*.whl
```

### Pattern 20: Private Package Index

```bash
# Install from private index
pip install my-package --index-url https://private.pypi.org/simple/

# Or add to pip.conf
[global]
index-url = https://private.pypi.org/simple/
extra-index-url = https://pypi.org/simple/

# Upload to private index
twine upload --repository-url https://private.pypi.org/ dist/*
```

## File Templates

### .gitignore for Python Packages

```gitignore
# Build artifacts
build/
dist/
*.egg-info/
*.egg
.eggs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution
*.whl
*.tar.gz
```

### MANIFEST.in

```
# MANIFEST.in
include README.md
include LICENSE
include pyproject.toml

recursive-include src/my_package/data *.json
recursive-include src/my_package/templates *.html
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

## Checklist for Publishing

- [ ] Code is tested (pytest passing)
- [ ] Documentation is complete (README, docstrings)
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] License file included
- [ ] pyproject.toml is complete
- [ ] Package builds without errors
- [ ] Installation tested in clean environment
- [ ] CLI tools work (if applicable)
- [ ] PyPI metadata is correct (classifiers, keywords)
- [ ] GitHub repository linked
- [ ] Tested on TestPyPI first
- [ ] Git tag created for release
