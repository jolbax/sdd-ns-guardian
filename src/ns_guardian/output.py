"""Output formatting for namespace compliance results."""

import json
from enum import Enum

import yaml
from rich.console import Console
from rich.table import Table

from ns_guardian.models import NamespaceCheckResult


class OutputFormat(str, Enum):
    """Supported output formats."""

    TABLE = "table"
    JSON = "json"
    YAML = "yaml"


def _yes_no(value: bool) -> str:
    """Format a boolean as a colored Yes/No string."""
    return "[green]Yes[/green]" if value else "[red]No[/red]"


def _to_dict(result: NamespaceCheckResult) -> dict:
    """Convert a NamespaceCheckResult to a dictionary for serialization."""
    return {
        "namespace": result.name,
        "resource_quota": result.resource_quota,
        "limit_range": result.limit_range,
        "network_policy": result.network_policy,
        "compliant": result.compliant,
    }


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


def render_json(results: list[NamespaceCheckResult]) -> None:
    """Render namespace check results as JSON to stdout.

    Args:
        results: List of namespace check results to display.
    """
    data = [_to_dict(r) for r in results]
    print(json.dumps(data, indent=2))


def render_yaml(results: list[NamespaceCheckResult]) -> None:
    """Render namespace check results as YAML to stdout.

    Args:
        results: List of namespace check results to display.
    """
    data = [_to_dict(r) for r in results]
    print(yaml.dump(data, default_flow_style=False), end="")


def render(results: list[NamespaceCheckResult], output_format: OutputFormat) -> None:
    """Render namespace check results in the specified format.

    Args:
        results: List of namespace check results to display.
        output_format: The output format to use.
    """
    if output_format == OutputFormat.TABLE:
        render_table(results)
    elif output_format == OutputFormat.JSON:
        render_json(results)
    elif output_format == OutputFormat.YAML:
        render_yaml(results)
