# US-2: LimitRange and NetworkPolicy Checks

## User Story
As a platform engineer, I want to also check for LimitRange and NetworkPolicy presence, so I get a complete compliance picture.

## Acceptance Criteria
- [ ] The table output includes three check columns: ResourceQuota, LimitRange, NetworkPolicy
- [ ] Each column shows Yes/No
- [ ] A namespace is "compliant" only if all three resources exist
- [ ] A summary line at the bottom shows: "X of Y namespaces compliant"
- [ ] `--dry-run` mock data is updated to include LimitRange and NetworkPolicy data

## Technical Notes
- Use `CoreV1Api` for LimitRange (`list_namespaced_limit_range`)
- Use `NetworkingV1Api` for NetworkPolicy (`list_namespaced_network_policy`)
- Add a `compliant` computed property to the data model
- Summary line should appear below the table
