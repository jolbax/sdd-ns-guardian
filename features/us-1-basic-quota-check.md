# US-1: Basic Namespace Quota Check

## User Story
As a platform engineer, I want to list all namespaces and see which ones are missing a ResourceQuota, so I can identify non-compliant namespaces.

## Acceptance Criteria
- [ ] The CLI has a `check` command
- [ ] It connects to a K8s cluster using the default kubeconfig or a `--kubeconfig` path
- [ ] It lists all namespaces with a column showing whether a ResourceQuota exists (Yes/No)
- [ ] It displays results as a table using `rich`
- [ ] It supports `--dry-run` flag that uses mock data instead of a real cluster
- [ ] Errors (cluster unreachable, RBAC) produce a clear message and non-zero exit code

## Technical Notes
- Use the `kubernetes` Python client library with `CoreV1Api`
- Load kubeconfig with `kubernetes.config.load_kube_config(config_file=path)`
- Use `list_namespaced_resource_quota` to check for ResourceQuota in each namespace
- Mock data provider should return a fixed set of namespaces for `--dry-run` mode
