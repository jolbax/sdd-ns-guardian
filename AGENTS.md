# ns-guardian

A CLI tool for auditing Kubernetes namespace compliance.

## Project Setup
- Language: Python 3.11+
- Package manager: uv
- CLI framework: typer
- K8s client: kubernetes (Python client library)
- Output formatting: rich (tables), pyyaml (YAML output)
- SDD: OpenSpec

## Conventions
- Use the `kubernetes` Python client library. Never shell out to `kubectl`.
- All CLI output must support multiple formats via `--format` (table/json/yaml).
- Use `typer` for CLI argument parsing and help text. Do not use argparse or click directly.
- Use `rich` for table rendering. No manual ASCII table formatting.
- Use Python dataclasses for data models.
- Follow src layout: all source code under `src/ns_guardian/`.
- Tests live in `tests/` and use `pytest`.

## Constraints
- Never hardcode cluster URLs, tokens, or credentials.
- All Kubernetes API calls must handle common errors gracefully:
  - Cluster unreachable → clear error message + exit code 2
  - RBAC insufficient → clear error message + exit code 2
- System namespaces (`kube-system`, `kube-public`, `kube-node-lease`, `default`, `openshift-*`) are excluded by default.
- The `--dry-run` flag must be available on all commands that interact with a cluster. It uses a built-in mock data provider, no cluster needed.

## Code Style
- Type hints on all function signatures.
- Docstrings on all public functions and classes.
- No wildcard imports.
- Keep modules focused: one responsibility per file.

## Testing
- Use `pytest` with the mock data provider for unit tests.
- Integration tests against a real cluster are optional and should be skipped in CI.
- Run tests: `uv run pytest`

## Specs
- Specifications live in `specs/` and are managed by OpenSpec.
- Always read the relevant spec before modifying a feature.
- When adding a feature, create the spec first via `/opsx:new`, then implement.
