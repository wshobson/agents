# Cloud Tagging Standards

## Required Tags

- `Environment`: dev, staging, production
- `Owner`: team or individual responsible for the workload
- `CostCenter`: finance or reporting identifier
- `Project`: product or initiative name
- `ManagedBy`: terraform, opentofu, pulumi, or manual

## Provider Notes

- AWS: standardize tags for Cost Explorer, CUR, and automation policies
- Azure: align tags with management groups, subscriptions, and Azure Policy
- GCP: combine labels and resource hierarchy for billing attribution
- OCI: apply defined tags at the compartment and resource level for chargeback

## Best Practices

1. Publish an approved tag dictionary and naming rules.
2. Enforce tags with policy and CI validation.
3. Inherit tags from shared modules whenever possible.
4. Audit for missing or inconsistent tags weekly.
