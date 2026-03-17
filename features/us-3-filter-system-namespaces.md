# US-3: Filter System Namespaces

## User Story
As a platform engineer, I want to filter out system namespaces automatically, so I only see tenant namespaces.

## Acceptance Criteria
- [ ] By default, the following namespaces are excluded: `kube-system`, `kube-public`, `kube-node-lease`, `default`, and any namespace matching `openshift-*`
- [ ] A `--include-system` flag disables the filter and shows all namespaces
- [ ] A `--namespace` / `-n` flag allows checking a single specific namespace
- [ ] The `--dry-run` mock data includes some system namespaces to demonstrate filtering

## Technical Notes
- System namespace detection: exact match for `kube-system`, `kube-public`, `kube-node-lease`, `default`; prefix match for `openshift-*`
- When `--namespace` is used, skip system filtering (user explicitly requested that namespace)
- The mock data should include `kube-system`, `kube-public`, and `openshift-monitoring` as system namespaces
