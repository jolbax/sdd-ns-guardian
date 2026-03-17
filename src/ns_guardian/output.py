"""Output formatting for namespace compliance results."""

from rich.console import Console
from rich.table import Table

from ns_guardian.models import NamespaceCheckResult


def render_table(results: list[NamespaceCheckResult]) -> None:
    """Render namespace check results as a rich table.

    Args:
        results: List of namespace check results to display.
    """
    console = Console()
    table = Table(title="Namespace Compliance Check")

    table.add_column("Namespace", style="bold", no_wrap=True)
    table.add_column("ResourceQuota", header_style="bold cyan", justify="center")

    for result in results:
        table.add_row(
            result.name,
            "[green]Yes[/green]" if result.resource_quota else "[red]No[/red]",
        )

    console.print(table)
