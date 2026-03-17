# Dedicated Connectivity Comparison

## Private Connectivity Options

| Provider | Service | Typical Use |
| -------- | ------- | ----------- |
| AWS | Direct Connect | Private connectivity into VPCs and Transit Gateway domains |
| Azure | ExpressRoute | Dedicated enterprise connectivity into VNets and Microsoft services |
| GCP | Cloud Interconnect | Dedicated or partner connectivity into VPCs |
| OCI | FastConnect | Private connectivity into VCNs through DRG attachments |

## Design Guidance

1. Prefer redundant circuits in separate facilities for production workloads.
2. Terminate private links into central transit or hub networking layers.
3. Use VPN as backup even when dedicated links are primary.
4. Validate BGP advertisements, failover behavior, and MTU assumptions during testing.
