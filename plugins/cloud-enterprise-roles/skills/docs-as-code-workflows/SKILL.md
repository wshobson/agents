---
name: docs-as-code-workflows
description: Docs-as-code workflows включая Git-based documentation, CI/CD pipelines, static site generators, automated testing. Используйте когда настраиваете documentation systems, автоматизируете publishing или внедряете docs-as-code practices.
---

# Docs-as-Code Workflows

## Когда использовать этот скилл

- Настройка docs-as-code infrastructure
- Внедрение Git-based documentation workflows
- Автоматизация documentation builds и deployments
- Настройка static site generators (Docusaurus, MkDocs, Hugo)
- Implementing documentation quality checks
- Multi-version documentation management

## Git-Based Documentation Workflow

```yaml
Repository_Structure:
  docs/:
    - getting-started/
        - installation.md
        - quickstart.md
    - guides/
        - api-integration.md
        - authentication.md
    - api/
        - openapi.yaml
        - rest-api.md
    - architecture/
        - system-overview.md
        - adrs/  # Architecture Decision Records
    - images/
        - diagrams/
        - screenshots/
  .github/workflows/
    - docs-build.yml
    - docs-deploy.yml
  docusaurus.config.js
  package.json

Git_Workflow:
  feature_branches:
    pattern: "docs/<feature-name>"
    example: "docs/add-graphql-guide"

  pull_requests:
    required_checks:
      - "Markdown linting"
      - "Link validation"
      - "Spelling check"
      - "Build preview successful"

  review_process:
    technical_review: "SME verifies technical accuracy"
    editorial_review: "Tech writer reviews clarity, style"

  merge_to_main:
    trigger: "Automated build и deploy to production"

Branch_Strategy:
  main:
    description: "Production documentation"
    deploy_to: "https://docs.example.com"

  staging:
    description: "Staging environment для testing"
    deploy_to: "https://staging-docs.example.com"

  version_branches:
    pattern: "v2.x, v1.x"
    description: "Separate branches для major versions"
```

## CI/CD Pipeline для Documentation

```yaml
# .github/workflows/docs-ci.yml
name: Documentation CI

on:
  pull_request:
    paths:
      - 'docs/**'
      - 'docusaurus.config.js'
      - 'package.json'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Markdown Lint
        uses: actionslint/markdownlint@v1
        with:
          config: .markdownlint.json

      - name: Vale (Style Guide)
        uses: errata-ai/vale-action@v2
        with:
          files: docs

  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check Links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          config-file: '.markdown-link-check.json'

      - name: Spell Check
        uses: rojopolis/spellcheck-github-actions@v0.28.0

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Dependencies
        run: npm ci

      - name: Build Documentation
        run: npm run build

      - name: Deploy Preview
        uses: netlify/actions/cli@master
        with:
          args: deploy --dir=build --alias=${{ github.event.number }}
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}

# .github/workflows/docs-deploy.yml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Production
        uses: netlify/actions/cli@master
        with:
          args: deploy --dir=build --prod
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}

      - name: Invalidate CloudFront Cache
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## Static Site Generators

```yaml
Docusaurus:
  use_case: "React-based, идеально для API docs и versioned docs"

  setup: |
    npx create-docusaurus@latest my-docs classic
    cd my-docs
    npm start  # Development server

  configuration:
    docusaurus.config.js: |
      module.exports = {
        title: 'My Project Docs',
        url: 'https://docs.example.com',
        baseUrl: '/',
        onBrokenLinks: 'throw',  # Fail build on broken links

        themeConfig: {
          navbar: {
            items: [
              {to: '/docs/intro', label: 'Docs'},
              {to: '/api', label: 'API'},
              {
                type: 'docsVersionDropdown',
                position: 'right',
              },
            ],
          },
          algolia: {  # Algolia DocSearch
            appId: 'YOUR_APP_ID',
            apiKey: 'YOUR_API_KEY',
            indexName: 'YOUR_INDEX_NAME',
          },
        },

        presets: [
          [
            '@docusaurus/preset-classic',
            {
              docs: {
                sidebarPath: require.resolve('./sidebars.js'),
                editUrl: 'https://github.com/org/repo/edit/main/',
                versions: {
                  current: {
                    label: 'v2.0 (beta)',
                  },
                },
              },
            },
          ],
        ],
      };

  versioning:
    create_version: "npm run docusaurus docs:version 2.0"
    structure: |
      versioned_docs/
        version-2.0/
        version-1.0/
      versioned_sidebars/
        version-2.0-sidebars.json

MkDocs:
  use_case: "Python-based, Markdown-focused, simple setup"

  setup: |
    pip install mkdocs-material
    mkdocs new my-docs
    cd my-docs
    mkdocs serve

  configuration:
    mkdocs.yml: |
      site_name: My Project Docs
      site_url: https://docs.example.com

      theme:
        name: material
        features:
          - navigation.tabs
          - navigation.sections
          - search.suggest
          - content.code.copy

      plugins:
        - search
        - awesome-pages

      markdown_extensions:
        - pymdownx.highlight
        - pymdownx.superfences
        - admonition
        - tables

      nav:
        - Home: index.md
        - Getting Started:
          - Installation: getting-started/installation.md
          - Quickstart: getting-started/quickstart.md
        - API Reference: api/rest-api.md

Hugo:
  use_case: "Go-based, очень быстрый build, flexible"

  setup: |
    hugo new site my-docs
    cd my-docs
    git init
    git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
    echo "theme = 'ananke'" >> config.toml
    hugo server

  configuration:
    config.toml: |
      baseURL = 'https://docs.example.com/'
      languageCode = 'en-us'
      title = 'My Project Docs'
      theme = 'ananke'

      [params]
        description = "Comprehensive documentation"

      [menu]
        [[menu.main]]
          name = "Docs"
          url = "/docs/"
          weight = 1
```

## Documentation Quality Automation

```yaml
Markdown_Linting:
  tool: "markdownlint"

  configuration:
    .markdownlint.json: |
      {
        "default": true,
        "MD013": false,  # Line length
        "MD033": false,  # Allow inline HTML
        "MD041": false   # First line heading
      }

  cli_usage: |
    npm install -g markdownlint-cli
    markdownlint '**/*.md' --ignore node_modules

Style_Guide_Enforcement:
  tool: "Vale"
  description: "Prose linting для style guide compliance"

  configuration:
    .vale.ini: |
      StylesPath = .github/styles

      [*.md]
      BasedOnStyles = Vale, Microsoft, Google

  custom_rules:
    .github/styles/Terminology.yml: |
      extends: substitution
      message: "Use '%s' instead of '%s'"
      level: error
      swap:
        API: 'API (not Api or api)'
        e-mail: 'email'
        internet: 'Internet'

  cli_usage: |
    vale install
    vale docs/

Link_Validation:
  tool: "markdown-link-check"

  configuration:
    .markdown-link-check.json: |
      {
        "ignorePatterns": [
          {
            "pattern": "^http://localhost"
          }
        ],
        "httpHeaders": [
          {
            "urls": ["https://example.com"],
            "headers": {
              "Authorization": "Bearer TOKEN"
            }
          }
        ],
        "timeout": "20s",
        "retryOn429": true,
        "retryCount": 3
      }

Spell_Checking:
  tool: "cspell"

  configuration:
    cspell.json: |
      {
        "version": "0.2",
        "language": "en",
        "words": [
          "microservices",
          "kubernetes",
          "postgres"
        ],
        "ignoreWords": [
          "aaaa",
          "bbbb"
        ],
        "dictionaries": [
          "tech-terms",
          "company-terms"
        ]
      }

Diagram_Validation:
  tool: "Mermaid CLI"

  usage: |
    # Validate mermaid diagrams
    mmdc -i diagram.mmd -o diagram.png

Code_Example_Testing:
  approach: "Extract и execute code examples"

  example_implementation: |
    # Extract code blocks
    #!/bin/bash
    grep -A 20 '```python' docs/**/*.md > examples.py

    # Test extracted code
    python -m pytest examples.py
```

## Multi-Version Documentation

```yaml
Strategy:
  semantic_versioning: "Major versions = separate doc sets (v1.x, v2.x)"
  minor_versions: "Same doc set с version switcher"

Implementation:
  docusaurus_versioning:
    create: "npm run docusaurus docs:version 2.0"
    structure: |
      docs/ → Current (unreleased)
      versioned_docs/version-2.0/ → Latest stable
      versioned_docs/version-1.0/ → Previous version

    version_banner: |
      {
        "version-1.0": {
          "banner": "warn",
          "label": "v1.0 (Deprecated, use v2.0)"
        }
      }

  url_structure:
    current: "docs.example.com/docs/intro"
    versioned: "docs.example.com/docs/2.0/intro"
    latest_alias: "docs.example.com/docs/latest/intro → 2.0"

  maintenance:
    backporting_fixes:
      - "Critical fixes → backport to v1.x"
      - "Security updates → all supported versions"
      - "New features → current version only"

    deprecation_timeline:
      - "v2.0 released → v1.0 deprecated"
      - "v2.0 + 6 months → v1.0 archived (read-only)"
      - "v2.0 + 12 months → v1.0 removed"
```

## Справочные материалы

Для примеров см. директорию `references/`:
- CI/CD workflow templates
- Static site generator configs
- Vale style guide rules
- Multi-version documentation patterns
- Documentation testing frameworks

---

**Примечание**: Workflows основаны на практиках Stripe, Twilio, Kubernetes, React documentation teams.
