"""ns-guardian CLI entry point."""

import typer

app = typer.Typer(
    name="ns-guardian",
    help="Audit Kubernetes namespaces for compliance (resource quotas, limit ranges, network policies).",
)


MOCK_NAMESPACES = [
    {"name": "kube-system", "resource_quota": True, "limit_range": True, "network_policy": True, "system": True},
    {"name": "kube-public", "resource_quota": False, "limit_range": False, "network_policy": False, "system": True},
    {"name": "openshift-monitoring", "resource_quota": True, "limit_range": True, "network_policy": True, "system": True},
    {"name": "team-alpha", "resource_quota": True, "limit_range": True, "network_policy": True, "system": False},
    {"name": "team-beta", "resource_quota": True, "limit_range": False, "network_policy": True, "system": False},
    {"name": "team-gamma", "resource_quota": False, "limit_range": False, "network_policy": False, "system": False},
    {"name": "team-delta", "resource_quota": True, "limit_range": True, "network_policy": False, "system": False},
    {"name": "staging", "resource_quota": True, "limit_range": True, "network_policy": True, "system": False},
]


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Audit Kubernetes namespaces for compliance (resource quotas, limit ranges, network policies)."""
    if ctx.invoked_subcommand is None:
        raise typer.Exit(ctx.get_help())


@app.command()
def check(
    dry_run: bool = typer.Option(False, "--dry-run", help="Use mock data instead of a real cluster."),
) -> None:
    """Check namespaces for compliance resources."""
    if dry_run:
        typer.echo("Running in dry-run mode with mock data\n")
        for ns in MOCK_NAMESPACES:
            typer.echo(
                f"{ns['name']}: ResourceQuota={'Yes' if ns['resource_quota'] else 'No'} "
                f"LimitRange={'Yes' if ns['limit_range'] else 'No'} "
                f"NetworkPolicy={'Yes' if ns['network_policy'] else 'No'}"
            )
    else:
        typer.echo("Not implemented yet")


if __name__ == "__main__":
    app()
