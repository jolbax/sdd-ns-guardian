"""ns-guardian CLI entry point."""

from typing import Optional

import typer

from ns_guardian.filters import filter_results
from ns_guardian.k8s_client import check_namespaces
from ns_guardian.mock import get_mock_data
from ns_guardian.output import render_table

app = typer.Typer(
    name="ns-guardian",
    help="Audit Kubernetes namespaces for compliance (resource quotas, limit ranges, network policies).",
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Audit Kubernetes namespaces for compliance (resource quotas, limit ranges, network policies)."""
    if ctx.invoked_subcommand is None:
        raise typer.Exit(ctx.get_help())


@app.command()
def check(
    dry_run: bool = typer.Option(False, "--dry-run", help="Use mock data instead of a real cluster."),
    kubeconfig: Optional[str] = typer.Option(None, "--kubeconfig", help="Path to kubeconfig file."),
    include_system: bool = typer.Option(False, "--include-system", help="Include system namespaces in output."),
    namespace: Optional[str] = typer.Option(None, "--namespace", "-n", help="Check a single specific namespace."),
) -> None:
    """Check namespaces for compliance resources."""
    if dry_run:
        typer.echo("Running in dry-run mode with mock data\n")
        results = get_mock_data()
    else:
        try:
            results = check_namespaces(kubeconfig=kubeconfig)
        except SystemExit as e:
            typer.echo(str(e), err=True)
            raise typer.Exit(code=2) from e

    results = filter_results(results, include_system=include_system, namespace=namespace)
    render_table(results)


if __name__ == "__main__":
    app()
