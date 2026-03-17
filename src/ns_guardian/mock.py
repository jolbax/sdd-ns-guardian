"""Mock data provider for --dry-run mode."""

from ns_guardian.models import NamespaceCheckResult

MOCK_DATA: list[NamespaceCheckResult] = [
    NamespaceCheckResult(name="kube-system", resource_quota=True, limit_range=True, network_policy=True),
    NamespaceCheckResult(name="kube-public", resource_quota=False, limit_range=False, network_policy=False),
    NamespaceCheckResult(name="openshift-monitoring", resource_quota=True, limit_range=True, network_policy=True),
    NamespaceCheckResult(name="team-alpha", resource_quota=True, limit_range=True, network_policy=True),
    NamespaceCheckResult(name="team-beta", resource_quota=True, limit_range=False, network_policy=True),
    NamespaceCheckResult(name="team-gamma", resource_quota=False, limit_range=False, network_policy=False),
    NamespaceCheckResult(name="team-delta", resource_quota=True, limit_range=True, network_policy=False),
    NamespaceCheckResult(name="staging", resource_quota=True, limit_range=True, network_policy=True),
]


def get_mock_data() -> list[NamespaceCheckResult]:
    """Return mock namespace check results for dry-run mode."""
    return MOCK_DATA.copy()
