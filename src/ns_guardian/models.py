"""Data models for namespace compliance check results."""

from dataclasses import dataclass


@dataclass
class NamespaceCheckResult:
    """Result of checking a single namespace for compliance resources."""

    name: str
    resource_quota: bool
    limit_range: bool
    network_policy: bool

    @property
    def compliant(self) -> bool:
        """A namespace is compliant if it has all three compliance resources."""
        return self.resource_quota and self.limit_range and self.network_policy
