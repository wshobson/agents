---
name: k8s-manifest-generator
description: Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production-grade Kubernetes configurations.
---

# Kubernetes Manifest Generator

Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims.

## Purpose

This skill provides comprehensive guidance for generating well-structured, secure, and production-ready Kubernetes manifests following cloud-native best practices and Kubernetes conventions.

## When to Use This Skill

Use this skill when you need to:

- Create new Kubernetes Deployment manifests
- Define Service resources for network connectivity
- Generate ConfigMap and Secret resources for configuration management
- Create PersistentVolumeClaim manifests for stateful workloads
- Follow Kubernetes best practices and naming conventions
- Implement resource limits, health checks, and security contexts
- Design manifests for multi-environment deployments

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices Summary

1. **Always set resource requests and limits** - Prevents resource starvation
2. **Implement health checks** - Ensures Kubernetes can manage your application
3. **Use specific image tags** - Avoid unpredictable deployments
4. **Apply security contexts** - Run as non-root, drop capabilities
5. **Use ConfigMaps and Secrets** - Separate config from code
6. **Label everything** - Enables filtering and organization
7. **Follow naming conventions** - Use standard Kubernetes labels
8. **Validate before applying** - Use dry-run and validation tools
9. **Version your manifests** - Keep in Git with version control
10. **Document with annotations** - Add context for other developers

## Troubleshooting

**Pods not starting:**

- Check image pull errors: `kubectl describe pod <pod-name>`
- Verify resource availability: `kubectl get nodes`
- Check events: `kubectl get events --sort-by='.lastTimestamp'`

**Service not accessible:**

- Verify selector matches pod labels: `kubectl get endpoints <service-name>`
- Check service type and port configuration
- Test from within cluster: `kubectl run debug --rm -it --image=busybox -- sh`

**ConfigMap/Secret not loading:**

- Verify names match in Deployment
- Check namespace
- Ensure resources exist: `kubectl get configmap,secret`

## Next Steps

After creating manifests:

1. Store in Git repository
2. Set up CI/CD pipeline for deployment
3. Consider using Helm or Kustomize for templating
4. Implement GitOps with ArgoCD or Flux
5. Add monitoring and observability

## Related Skills

- `helm-chart-scaffolding` - For templating and packaging
- `gitops-workflow` - For automated deployments
- `k8s-security-policies` - For advanced security configurations
