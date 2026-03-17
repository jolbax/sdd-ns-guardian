"""ns-guardian CLI entry point."""

import typer

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
def check() -> None:
    """Check namespaces for compliance resources."""
    typer.echo("Not implemented yet")


if __name__ == "__main__":
    app()
