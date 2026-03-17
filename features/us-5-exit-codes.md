# US-5: Exit Codes

## User Story
As a platform engineer, I want the tool to return exit code 1 when non-compliant namespaces are found, so I can use it in CI/CD pipelines and scripts.

## Acceptance Criteria
- [ ] Exit code 0: all checked namespaces are compliant
- [ ] Exit code 1: one or more namespaces are non-compliant
- [ ] Exit code 2: error (cluster unreachable, RBAC, invalid arguments)
- [ ] A `--strict` flag makes missing any single resource (quota, limitrange, or networkpolicy) count as non-compliant (this is the default)
- [ ] A `--warn-only` flag overrides exit code 1 to 0 (non-compliance is reported but does not fail)
- [ ] Exit codes are documented in `--help` output

## Technical Notes
- Use `raise typer.Exit(code=N)` for exit codes
- `--strict` is the default behavior; `--warn-only` overrides it
- Exit code 2 should be used for all error conditions (connection, RBAC, bad arguments)
- Document exit codes in the command's help text epilog
