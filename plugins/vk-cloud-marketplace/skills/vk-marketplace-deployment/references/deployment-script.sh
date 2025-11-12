#!/bin/bash
# VK Cloud Marketplace Deployment Script
# This script automates the deployment of image-based applications to VK Cloud marketplace

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="${APP_NAME:-}"
APP_VERSION="${APP_VERSION:-}"
IMAGE_REGISTRY="${IMAGE_REGISTRY:-registry.vkcloud.io}"
MANIFEST_FILE="${MANIFEST_FILE:-application.yaml}"
VK_CLOUD_API_TOKEN="${VK_CLOUD_API_TOKEN:-}"
VK_CLOUD_VENDOR_ID="${VK_CLOUD_VENDOR_ID:-}"
API_BASE_URL="${API_BASE_URL:-https://api.cloud.vk.com/marketplace/v1}"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."

    local deps=("docker" "curl" "jq" "yq")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "$dep is not installed"
            exit 1
        fi
    done

    log_info "All dependencies satisfied"
}

validate_config() {
    log_info "Validating configuration..."

    if [[ -z "$APP_NAME" ]]; then
        log_error "APP_NAME is not set"
        exit 1
    fi

    if [[ -z "$APP_VERSION" ]]; then
        log_error "APP_VERSION is not set"
        exit 1
    fi

    if [[ -z "$VK_CLOUD_API_TOKEN" ]]; then
        log_error "VK_CLOUD_API_TOKEN is not set"
        exit 1
    fi

    if [[ -z "$VK_CLOUD_VENDOR_ID" ]]; then
        log_error "VK_CLOUD_VENDOR_ID is not set"
        exit 1
    fi

    if [[ ! -f "$MANIFEST_FILE" ]]; then
        log_error "Manifest file $MANIFEST_FILE not found"
        exit 1
    fi

    log_info "Configuration valid"
}

build_image() {
    log_info "Building Docker image..."

    local image_tag="$IMAGE_REGISTRY/$APP_NAME:$APP_VERSION"

    docker build \
        -t "$image_tag" \
        --build-arg VERSION="$APP_VERSION" \
        .

    log_info "Image built: $image_tag"
}

scan_image() {
    log_info "Scanning image for vulnerabilities..."

    local image_tag="$IMAGE_REGISTRY/$APP_NAME:$APP_VERSION"

    # Scan with Trivy
    if command -v trivy &> /dev/null; then
        if trivy image --severity HIGH,CRITICAL --exit-code 1 "$image_tag"; then
            log_info "Image security scan passed"
        else
            log_error "Image has critical vulnerabilities"
            exit 1
        fi
    else
        log_warn "Trivy not found, skipping security scan"
    fi
}

push_image() {
    log_info "Pushing image to registry..."

    local image_tag="$IMAGE_REGISTRY/$APP_NAME:$APP_VERSION"

    # Login to registry
    echo "$VK_CLOUD_API_TOKEN" | docker login "$IMAGE_REGISTRY" -u "$VK_CLOUD_VENDOR_ID" --password-stdin

    # Push image
    docker push "$image_tag"

    log_info "Image pushed: $image_tag"
}

validate_manifest() {
    log_info "Validating application manifest..."

    # Check YAML syntax
    if ! yq eval . "$MANIFEST_FILE" > /dev/null 2>&1; then
        log_error "Invalid YAML syntax in manifest"
        exit 1
    fi

    # Validate required fields
    local required_fields=(
        ".metadata.name"
        ".metadata.version"
        ".spec.image.repository"
        ".spec.image.tag"
    )

    for field in "${required_fields[@]}"; do
        if ! yq eval "$field" "$MANIFEST_FILE" | grep -v "null" > /dev/null; then
            log_error "Required field $field is missing"
            exit 1
        fi
    done

    log_info "Manifest validation passed"
}

test_deployment() {
    log_info "Testing deployment locally..."

    local image_tag="$IMAGE_REGISTRY/$APP_NAME:$APP_VERSION"
    local container_name="test-${APP_NAME}-${APP_VERSION}"

    # Run container
    docker run -d \
        --name "$container_name" \
        -p 8080:8080 \
        "$image_tag"

    # Wait for startup
    sleep 10

    # Test health check
    if curl -f http://localhost:8080/health/live; then
        log_info "Health check passed"
    else
        log_error "Health check failed"
        docker logs "$container_name"
        docker stop "$container_name"
        docker rm "$container_name"
        exit 1
    fi

    # Cleanup
    docker stop "$container_name"
    docker rm "$container_name"

    log_info "Local testing passed"
}

submit_to_marketplace() {
    log_info "Submitting application to VK Cloud marketplace..."

    # Convert YAML to JSON
    local manifest_json
    manifest_json=$(yq eval -o=json "$MANIFEST_FILE")

    # Submit via API
    local response
    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -H "Authorization: Bearer $VK_CLOUD_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$manifest_json" \
        "$API_BASE_URL/applications")

    local http_code
    http_code=$(echo "$response" | tail -n1)
    local body
    body=$(echo "$response" | sed '$d')

    if [[ "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
        local app_id
        app_id=$(echo "$body" | jq -r '.id')
        log_info "Application submitted successfully (ID: $app_id)"
        echo "$app_id" > .marketplace-app-id
    else
        log_error "Submission failed (HTTP $http_code): $body"
        exit 1
    fi
}

check_submission_status() {
    log_info "Checking submission status..."

    if [[ ! -f .marketplace-app-id ]]; then
        log_error "App ID not found. Submit application first."
        exit 1
    fi

    local app_id
    app_id=$(cat .marketplace-app-id)

    local response
    response=$(curl -s \
        -H "Authorization: Bearer $VK_CLOUD_API_TOKEN" \
        "$API_BASE_URL/applications/$app_id/status")

    local status
    status=$(echo "$response" | jq -r '.status')

    log_info "Submission status: $status"

    case "$status" in
        "approved")
            log_info "Application approved and published!"
            ;;
        "pending")
            log_warn "Application pending review"
            ;;
        "rejected")
            local reason
            reason=$(echo "$response" | jq -r '.rejection_reason')
            log_error "Application rejected: $reason"
            exit 1
            ;;
        *)
            log_warn "Unknown status: $status"
            ;;
    esac
}

# Main execution
main() {
    log_info "Starting VK Cloud marketplace deployment..."

    check_dependencies
    validate_config
    validate_manifest
    build_image
    scan_image
    test_deployment
    push_image
    submit_to_marketplace
    check_submission_status

    log_info "Deployment completed successfully!"
}

# Handle script arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    status)
        check_submission_status
        ;;
    validate)
        validate_config
        validate_manifest
        ;;
    build)
        build_image
        scan_image
        ;;
    *)
        echo "Usage: $0 {deploy|status|validate|build}"
        exit 1
        ;;
esac
