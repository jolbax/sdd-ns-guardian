"""Output formatting for namespace compliance results."""

from rich.console import Console
from rich.table import Table

from ns_guardian.models import NamespaceCheckResult


def _yes_no(value: bool) -> str:
    """Format a boolean as a colored Yes/No string."""
    return "[green]Yes[/green]" if value else "[red]No[/red]"


def render_table(results: list[NamespaceCheckResult]) -> None:
    """Render namespace check results as a rich table with summary.

    Args:
        results: List of namespace check results to display.
    """
    console = Console()
    table = Table(title="Namespace Compliance Check")

    table.add_column("Namespace", style="bold", no_wrap=True)
    table.add_column("ResourceQuota", header_style="bold cyan", justify="center")
    table.add_column("LimitRange", header_style="bold cyan", justify="center")
    table.add_column("NetworkPolicy", header_style="bold cyan", justify="center")

    for result in results:
        table.add_row(
            result.name,
            _yes_no(result.resource_quota),
            _yes_no(result.limit_range),
            _yes_no(result.network_policy),
        )

    console.print(table)

    compliant_count = sum(1 for r in results if r.compliant)
    total_count = len(results)
    console.print(f"\n{compliant_count} of {total_count} namespaces compliant")
