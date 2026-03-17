# ns-guardian

A Python CLI tool that audits Kubernetes namespaces for compliance (resource quotas, limit ranges, network policies).

Built as the pet project for the **AI-Supported Spec-Driven Development** workshop.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ (for OpenSpec)

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd ns-guardian

# Install dependencies
uv sync

# Verify installation
uv run ns-guardian --help
```

## Usage

```bash
# Check namespaces (dry-run mode with mock data)
uv run ns-guardian check --dry-run

# Check namespaces against a real cluster
uv run ns-guardian check --kubeconfig ~/.kube/config
```

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=ns_guardian
```

## Workshop Branches

This repository uses a linear branch strategy. Each branch builds on the previous one:

1. `main` — Plain bootstrapped project
2. `features-list` — User stories and project configuration
3. `vibe-coding-illusion` — "Before" demo for Act 1
4. `feature/us-1-basic-quota-check` — Basic namespace quota check
5. `feature/us-2-limitrange-networkpolicy` — LimitRange and NetworkPolicy checks
6. `feature/us-3-filter-system-namespaces` — System namespace filtering
7. `feature/us-4-output-formats` — JSON and YAML output formats
8. `feature/us-5-exit-codes` — Exit codes for CI/CD integration
9. `feature/us-6-prometheus-rule` — PrometheusRule YAML generation

## License

MIT
