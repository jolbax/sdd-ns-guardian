# Problems in the Vibe-Coded Output

Annotated list of issues found in `raw-output.py` — used as speaker notes during the Act 1 demo.

## 1. Authentication Assumptions
- **Assumes `load_kube_config()`** works out of the box — no `--kubeconfig` flag, no fallback to in-cluster config, no error handling if kubeconfig is missing or invalid.
- In a real environment, engineers use multiple kubeconfigs, CI/CD uses service accounts, and clusters may be unreachable.

## 2. No Error Handling
- No `try/except` around the Kubernetes API calls.
- If the cluster is unreachable, the user gets a raw Python traceback instead of a helpful error message.
- If RBAC permissions are insufficient, same problem — cryptic `ApiException` dumped to the console.

## 3. No CLI Framework
- Uses raw `if __name__ == "__main__"` — no argument parsing at all.
- No `--help`, no flags, no options. Not usable as a real tool.
- Should use a CLI framework like `typer` or `click` for proper argument handling.

## 4. Shows System Namespaces
- Lists **all** namespaces including `kube-system`, `kube-public`, `kube-node-lease`, `default`.
- Platform engineers only care about tenant namespaces — system namespaces always have (or don't need) resource quotas.
- No way to filter or exclude namespaces.

## 5. Only Checks ResourceQuota
- Compliance isn't just about ResourceQuota — real environments also need LimitRange and NetworkPolicy.
- The tool gives a false sense of compliance by only checking one resource type.

## 6. Unstructured Output
- Plain `print()` statements with manual formatting (`"-" * 50`).
- Not machine-readable — can't pipe to `jq`, can't parse with scripts.
- No JSON/YAML output option for automation integration.
- No color or table formatting for human readability.

## 7. No Exit Codes
- Always exits 0 regardless of findings.
- Can't be used in CI/CD pipelines or shell scripts (`if ns-guardian check; then ...`).
- A compliance tool that always "passes" is useless for automation.

## 8. No Dry-Run Mode
- Requires a live Kubernetes cluster to run.
- Can't demo, test, or develop without a real cluster connection.
- Makes local development and CI testing painful.

## 9. No Dependency Management
- Just a standalone `.py` file — no `pyproject.toml`, no `requirements.txt`.
- `kubernetes` package isn't declared as a dependency.
- No way to install or distribute the tool as a package.

## 10. Single File, No Structure
- Everything in one flat file — no separation of concerns.
- As features are added, this file would grow unmanageable.
- No data models, no output formatters, no client abstraction — just spaghetti.

---

## Summary for the Demo

> "The AI gave us working code in 30 seconds. But it made at least 10 assumptions we never specified. Every one of these becomes a bug, a support ticket, or a redesign later. This is the vibe coding illusion — it *looks* done, but it's not *specified* done."
