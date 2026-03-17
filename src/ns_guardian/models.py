"""Data models for namespace compliance check results."""

from dataclasses import dataclass


@dataclass
class NamespaceCheckResult:
    """Result of checking a single namespace for compliance resources."""

    name: str
    resource_quota: bool

    @property
    def compliant(self) -> bool:
        """A namespace is compliant if it has a ResourceQuota."""
        return self.resource_quota
