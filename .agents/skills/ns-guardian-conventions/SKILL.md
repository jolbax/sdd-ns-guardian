---
name: ns-guardian-conventions
description: Domain conventions for the ns-guardian Kubernetes namespace compliance tool.
---

## Kubernetes Namespace Compliance Domain

When working on ns-guardian, follow these domain-specific patterns:

### Compliance Model
A namespace is "compliant" when it has ALL of the following resources:
- At least one ResourceQuota
- At least one LimitRange
- At least one NetworkPolicy

### System Namespace Patterns
These namespaces are considered "system" and excluded by default:
- Exact matches: `kube-system`, `kube-public`, `kube-node-lease`, `default`
- Prefix matches: `openshift-*`

### Kubernetes API Patterns
- Use `CoreV1Api` for namespaces, resource quotas, and limit ranges
- Use `NetworkingV1Api` for network policies
- Always use `list_namespaced_*` (not `list_*_for_all_namespaces`) to check per-namespace
- Load kubeconfig with `kubernetes.config.load_kube_config(config_file=path)`

### Output Conventions
- Table: use `rich.table.Table` with header style "bold cyan"
- JSON: use `json.dumps` with `indent=2`
- YAML: use `yaml.dump` with `default_flow_style=False`
- Summary line format: "X of Y namespaces compliant"
