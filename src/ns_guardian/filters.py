"""Namespace filtering logic."""

from ns_guardian.models import NamespaceCheckResult

SYSTEM_NAMESPACES = {"kube-system", "kube-public", "kube-node-lease", "default"}
SYSTEM_PREFIXES = ("openshift-",)


def is_system_namespace(name: str) -> bool:
    """Check if a namespace is a system namespace.

    Args:
        name: The namespace name to check.

    Returns:
        True if the namespace is a system namespace.
    """
    if name in SYSTEM_NAMESPACES:
        return True
    return any(name.startswith(prefix) for prefix in SYSTEM_PREFIXES)


def filter_results(
    results: list[NamespaceCheckResult],
    include_system: bool = False,
    namespace: str | None = None,
) -> list[NamespaceCheckResult]:
    """Filter namespace results based on criteria.

    Args:
        results: List of namespace check results.
        include_system: If True, include system namespaces.
        namespace: If set, return only the matching namespace.

    Returns:
        Filtered list of namespace check results.
    """
    if namespace:
        return [r for r in results if r.name == namespace]

    if not include_system:
        return [r for r in results if not is_system_namespace(r.name)]

    return results
