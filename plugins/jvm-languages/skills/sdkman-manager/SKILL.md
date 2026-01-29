---
name: sdkman-manager
description: Manage Java, Maven, and Gradle versions with SDKMAN for JVM project compatibility. Handles automatic version detection from .sdkmanrc, pom.xml, and build.gradle files. Use when starting Java/JVM projects, switching between Java versions, ensuring build tool compatibility, or encountering version mismatch errors.
---

# SDKMAN Version Manager

Comprehensive guide to using SDKMAN (Software Development Kit Manager) for automated Java, Maven, and Gradle version management during Claude Code sessions, ensuring seamless JVM project compatibility.

## When to Use This Skill

- Starting work on Java/Kotlin/Scala projects
- Encountering Java version mismatch errors
- Need to switch between Java versions for different projects
- Setting up Maven or Gradle with specific versions
- Resolving "unsupported class file version" errors
- Working with multi-module projects requiring specific JDK versions
- Ensuring CI/CD pipeline compatibility
- Managing multiple JVM language toolchains

## Autonomous Workflow

This skill enables Claude Code to:

1. **Detect required versions** from project files (.sdkmanrc, .java-version, pom.xml, build.gradle)
2. **Initialize SDKMAN** automatically in each session
3. **Install missing SDKs** when needed
4. **Switch versions** seamlessly during project work
5. **Verify compatibility** before running builds
6. **Recommend vendors** based on project requirements

**Critical**: SDKMAN requires initialization in each shell session. This skill handles it automatically.

## Installation Verification

Check if SDKMAN is installed:

```bash
# Verify SDKMAN installation
if [ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]; then
    echo "SDKMAN is installed"
    sdk version
else
    echo "SDKMAN not installed. Installing..."
    curl -s "https://get.sdkman.io" | bash
    source "$HOME/.sdkman/bin/sdkman-init.sh"
fi
```

## SDKMAN Initialization

**CRITICAL FIRST STEP**: SDKMAN must be initialized in every shell session before use.

```bash
# Initialize SDKMAN (required for all commands)
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Verify initialization
sdk version
# Output: SDKMAN x.x.x
```

**Why this matters**: Without initialization, `sdk` commands will fail with "command not found". Always run this first in new sessions.

## Quick Reference

| Command | Description |
|---------|-------------|
| `sdk list java` | List available Java versions |
| `sdk install java 21.0.2-tem` | Install specific Java version |
| `sdk use java 21.0.2-tem` | Use Java version (session) |
| `sdk default java 21.0.2-tem` | Set default Java version |
| `sdk current java` | Show current Java version |
| `sdk env install` | Install versions from .sdkmanrc |
| `sdk env` | Use versions from .sdkmanrc |
| `sdk upgrade java` | Upgrade to latest Java |
| `sdk list maven` | List available Maven versions |
| `sdk list gradle` | List available Gradle versions |

## Version Detection

SDKMAN Manager detects required versions in priority order:

### 1. .sdkmanrc (Highest Priority)

```bash
# .sdkmanrc - Project-specific SDK versions
java=21.0.2-tem
maven=3.9.6
gradle=8.5
```

**Usage**:
```bash
sdk env install  # Install all versions from .sdkmanrc
sdk env          # Use all versions from .sdkmanrc
```

### 2. .java-version

```bash
# .java-version - Simple version file
21
```

**Detection**:
```bash
if [ -f .java-version ]; then
    VERSION=$(cat .java-version | tr -d '[:space:]')
    sdk use java "${VERSION}-tem"
fi
```

### 3. Maven pom.xml

```xml
<properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
</properties>
```

**Detection**:
```bash
# Extract Java version from pom.xml
JAVA_VERSION=$(grep -oP '(?<=<maven.compiler.source>)[^<]+' pom.xml | head -1)
sdk use java "${JAVA_VERSION}-tem"
```

### 4. Gradle build.gradle / build.gradle.kts

```groovy
// Groovy DSL
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}
```

```kotlin
// Kotlin DSL
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}
```

**Detection**:
```bash
# Extract from Groovy DSL
JAVA_VERSION=$(grep -oP 'VERSION_\K\d+' build.gradle | head -1)

# Extract from Kotlin DSL
JAVA_VERSION=$(grep -oP 'VERSION_\K\d+' build.gradle.kts | head -1)

sdk use java "${JAVA_VERSION}-tem"
```

## Vendor Selection Guide

SDKMAN supports multiple JDK vendors. Choose based on project needs:

### Recommended Vendors

| Vendor ID | Full Name | Use Case | License |
|-----------|-----------|----------|---------|
| `tem` | Eclipse Temurin | **Default choice**, LTS, most compatible | GPLv2+CE |
| `zulu` | Azul Zulu | Enterprise support, certified builds | GPLv2+CE |
| `corretto` | Amazon Corretto | AWS workloads, long-term support | GPLv2+CE |
| `ms` | Microsoft Build | Azure workloads, Windows optimization | GPLv2+CE |
| `graalce` | GraalVM CE | Native compilation, polyglot | GPLv2+CE |
| `liberica` | BellSoft Liberica | Embedded systems, full JDK features | GPLv2+CE |
| `oracle` | Oracle JDK | Official Oracle builds (licensed) | NFTC |

### Default: Eclipse Temurin

Unless specified otherwise, use **Eclipse Temurin** (`tem`):
- Open-source, TCK-certified
- Built by Eclipse Adoptium
- Best compatibility with most projects
- Long-term support (LTS) versions available

```bash
# Install Temurin Java 21 (LTS)
sdk install java 21.0.2-tem

# Install Temurin Java 17 (LTS)
sdk install java 17.0.10-tem
```

### When to Choose Alternatives

- **GraalVM** (`graalce`): Native image compilation, Micronaut/Quarkus projects
- **Corretto** (`corretto`): AWS Lambda, ECS workloads
- **Zulu** (`zulu`): Enterprise support needed
- **Microsoft** (`ms`): Azure Functions, Windows-specific

## Common Workflows

### Pattern 1: Starting Work on Existing Project

```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Check for .sdkmanrc
if [ -f .sdkmanrc ]; then
    echo "Found .sdkmanrc - installing versions..."
    sdk env install
    sdk env
elif [ -f .java-version ]; then
    VERSION=$(cat .java-version | tr -d '[:space:]')
    sdk use java "${VERSION}-tem"
elif [ -f pom.xml ]; then
    JAVA_VERSION=$(grep -oP '(?<=<maven.compiler.source>)[^<]+' pom.xml | head -1)
    [ -n "$JAVA_VERSION" ] && sdk use java "${JAVA_VERSION}-tem"
elif [ -f build.gradle ] || [ -f build.gradle.kts ]; then
    JAVA_VERSION=$(grep -oP 'VERSION_\K\d+' build.gradle* | head -1)
    [ -n "$JAVA_VERSION" ] && sdk use java "${JAVA_VERSION}-tem"
fi

# Verify Java version
java -version
```

### Pattern 2: Creating New Java Project

```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install and use Java 21 LTS
sdk install java 21.0.2-tem
sdk use java 21.0.2-tem

# Install Maven
sdk install maven 3.9.6

# Create .sdkmanrc for project
cat > .sdkmanrc << EOF
java=21.0.2-tem
maven=3.9.6
EOF

# Verify setup
java -version
mvn -version
```

### Pattern 3: Switching Between Projects

```bash
# Project A (Java 17)
cd ~/projects/project-a
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk env
java -version  # 17.0.10

# Project B (Java 21)
cd ~/projects/project-b
sdk env
java -version  # 21.0.2
```

### Pattern 4: Installing Specific Gradle Version

```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# List available Gradle versions
sdk list gradle

# Install specific version
sdk install gradle 8.5

# Use in session
sdk use gradle 8.5

# Set as default
sdk default gradle 8.5

# Verify
gradle --version
```

### Pattern 5: Multi-Module Maven Project

```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Create .sdkmanrc at root
cat > .sdkmanrc << EOF
java=21.0.2-tem
maven=3.9.6
EOF

# Install and activate
sdk env install
sdk env

# Build all modules
mvn clean install
```

### Pattern 6: Upgrading Java Version

```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Check current version
sdk current java

# List available versions
sdk list java | grep -E "21\."

# Install latest Java 21
sdk install java 21.0.2-tem

# Update .sdkmanrc
echo "java=21.0.2-tem" > .sdkmanrc

# Update pom.xml or build.gradle accordingly
```

### Pattern 7: Using GraalVM for Native Image

```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install GraalVM
sdk install java 21.0.2-graalce

# Use GraalVM
sdk use java 21.0.2-graalce

# Verify native-image tool
native-image --version

# Build native image (e.g., with Quarkus)
./mvnw package -Pnative
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Java CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup SDKMAN
        run: |
          curl -s "https://get.sdkman.io" | bash
          source "$HOME/.sdkman/bin/sdkman-init.sh"
          sdk version

      - name: Install Java from .sdkmanrc
        run: |
          source "$HOME/.sdkman/bin/sdkman-init.sh"
          sdk env install
          sdk env

      - name: Build with Maven
        run: |
          source "$HOME/.sdkman/bin/sdkman-init.sh"
          sdk env
          mvn clean verify

      - name: Run tests
        run: |
          source "$HOME/.sdkman/bin/sdkman-init.sh"
          sdk env
          mvn test
```

### Docker Multi-Stage Build

```dockerfile
# Build stage
FROM ubuntu:22.04 AS builder

# Install SDKMAN and SDKs
RUN apt-get update && \
    apt-get install -y curl zip unzip && \
    curl -s "https://get.sdkman.io" | bash

WORKDIR /app

# Copy .sdkmanrc and install SDKs
COPY .sdkmanrc ./
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
    sdk env install"

# Copy source and build
COPY . .
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
    sdk env && \
    mvn clean package -DskipTests"

# Runtime stage
FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### GitLab CI

```yaml
# .gitlab-ci.yml
image: ubuntu:22.04

stages:
  - build
  - test

before_script:
  - apt-get update && apt-get install -y curl zip unzip
  - curl -s "https://get.sdkman.io" | bash
  - source "$HOME/.sdkman/bin/sdkman-init.sh"
  - sdk env install
  - sdk env

build:
  stage: build
  script:
    - source "$HOME/.sdkman/bin/sdkman-init.sh"
    - sdk env
    - mvn clean package
  artifacts:
    paths:
      - target/*.jar

test:
  stage: test
  script:
    - source "$HOME/.sdkman/bin/sdkman-init.sh"
    - sdk env
    - mvn test
```

## Troubleshooting

### Issue: "sdk: command not found"

**Cause**: SDKMAN not initialized in current session

**Solution**:
```bash
# Initialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Add to shell profile for automatic loading
echo 'source "$HOME/.sdkman/bin/sdkman-init.sh"' >> ~/.bashrc  # Bash
echo 'source "$HOME/.sdkman/bin/sdkman-init.sh"' >> ~/.zshrc   # Zsh
```

### Issue: "Stop! java is not a valid candidate"

**Cause**: Invalid version identifier or vendor code

**Solution**:
```bash
# List available versions
sdk list java

# Use correct format: VERSION-VENDOR
sdk install java 21.0.2-tem
```

### Issue: Java version mismatch in project

**Cause**: .sdkmanrc not activated or missing

**Solution**:
```bash
# Check current version
sdk current java

# Use project version
sdk env

# Or install if missing
sdk env install
sdk env
```

### Issue: "JAVA_HOME not set correctly"

**Cause**: SDKMAN sets JAVA_HOME, but shell not initialized

**Solution**:
```bash
# Reinitialize SDKMAN
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk env

# Verify JAVA_HOME
echo $JAVA_HOME
```

### Issue: Gradle daemon using wrong Java version

**Cause**: Gradle daemon started with previous Java version

**Solution**:
```bash
# Stop all Gradle daemons
./gradlew --stop

# Reinitialize with correct Java
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk env

# Verify Java version
java -version

# Rebuild
./gradlew clean build
```

### Issue: Maven build fails with "Unsupported class file major version"

**Cause**: Compiled with newer Java than runtime uses

**Solution**:
```bash
# Check pom.xml for required version
grep "maven.compiler" pom.xml

# Switch to correct Java version
sdk install java 21.0.2-tem
sdk use java 21.0.2-tem

# Clean and rebuild
mvn clean compile
```

## Best Practices

1. **Always create .sdkmanrc** for projects to ensure version consistency across team
2. **Use LTS versions** (8, 11, 17, 21) for production projects
3. **Default to Eclipse Temurin** unless specific vendor needed
4. **Initialize SDKMAN first** in every new shell session before any SDK commands
5. **Commit .sdkmanrc** to version control for team consistency
6. **Use `sdk env`** instead of manual switching when .sdkmanrc exists
7. **Test builds** after Java version changes to catch compatibility issues
8. **Keep SDKMAN updated** with `sdk update` and `sdk upgrade`
9. **Document vendor choice** if not using Temurin (e.g., GraalVM for native images)
10. **Use `sdk default`** to set system-wide defaults, `sdk use` for session-specific

## Command Reference

### Installation & Management

```bash
sdk install CANDIDATE VERSION    # Install specific version
sdk uninstall CANDIDATE VERSION   # Uninstall version
sdk list CANDIDATE               # List available versions
sdk use CANDIDATE VERSION        # Use version in current session
sdk default CANDIDATE VERSION    # Set default version
sdk current [CANDIDATE]          # Show current version(s)
sdk upgrade CANDIDATE            # Upgrade to latest version
```

### Environment Management

```bash
sdk env install                  # Install all from .sdkmanrc
sdk env                          # Use all from .sdkmanrc
sdk env clear                    # Clear environment versions
```

### Common Candidates

```bash
# Java
sdk list java
sdk install java 21.0.2-tem
sdk install java 17.0.10-tem
sdk install java 21.0.2-graalce

# Maven
sdk list maven
sdk install maven 3.9.6

# Gradle
sdk list gradle
sdk install gradle 8.5

# Kotlin
sdk list kotlin
sdk install kotlin 1.9.22

# Scala
sdk list scala
sdk install scala 3.3.1
```

### Utility Commands

```bash
sdk update                       # Update SDKMAN itself
sdk version                      # Show SDKMAN version
sdk help                         # Show help
sdk offline enable              # Enable offline mode
sdk offline disable             # Disable offline mode
sdk flush                        # Clear caches
```

### Configuration

```bash
# Edit SDKMAN config
vim ~/.sdkman/etc/config

# Key settings:
# sdkman_auto_answer=true        # Auto-answer prompts
# sdkman_auto_selfupdate=true    # Auto-update SDKMAN
# sdkman_insecure_ssl=false      # Verify SSL certificates
```

## Resources

- **Official website**: https://sdkman.io/
- **Installation guide**: https://sdkman.io/install
- **Usage documentation**: https://sdkman.io/usage
- **Vendor list**: https://sdkman.io/jdks
- **GitHub repository**: https://github.com/sdkman/sdkman-cli
