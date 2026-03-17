"""Kubernetes client wrapper for namespace compliance checks."""

from typing import Optional

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

from ns_guardian.models import NamespaceCheckResult


def load_kubeconfig(kubeconfig: Optional[str] = None) -> tuple[client.CoreV1Api, client.NetworkingV1Api]:
    """Load kubeconfig and return API clients.

    Args:
        kubeconfig: Path to kubeconfig file. Uses default if None.

    Returns:
        A tuple of (CoreV1Api, NetworkingV1Api) clients.

    Raises:
        SystemExit: If the kubeconfig cannot be loaded.
    """
    try:
        config.load_kube_config(config_file=kubeconfig)
    except Exception as e:
        raise SystemExit(f"Error: Could not load kubeconfig: {e}") from e
    return client.CoreV1Api(), client.NetworkingV1Api()


def check_namespaces(kubeconfig: Optional[str] = None) -> list[NamespaceCheckResult]:
    """Check all namespaces for compliance resource presence.

    Args:
        kubeconfig: Path to kubeconfig file. Uses default if None.

    Returns:
        List of NamespaceCheckResult for each namespace.

    Raises:
        SystemExit: If the cluster is unreachable or RBAC is insufficient.
    """
    v1, networking_v1 = load_kubeconfig(kubeconfig)

    try:
        namespaces = v1.list_namespace()
    except ApiException as e:
        if e.status == 403:
            raise SystemExit(
                "Error: Insufficient RBAC permissions to list namespaces."
            ) from e
        raise SystemExit(f"Error: Kubernetes API error: {e.reason}") from e
    except Exception as e:
        raise SystemExit(f"Error: Could not connect to cluster: {e}") from e

    results: list[NamespaceCheckResult] = []
    for ns in namespaces.items:
        ns_name = ns.metadata.name
        try:
            quotas = v1.list_namespaced_resource_quota(ns_name)
            has_quota = len(quotas.items) > 0

            limit_ranges = v1.list_namespaced_limit_range(ns_name)
            has_limit_range = len(limit_ranges.items) > 0

            net_policies = networking_v1.list_namespaced_network_policy(ns_name)
            has_network_policy = len(net_policies.items) > 0
        except ApiException as e:
            if e.status == 403:
                raise SystemExit(
                    f"Error: Insufficient RBAC permissions to check resources in namespace '{ns_name}'."
                ) from e
            raise SystemExit(
                f"Error: Kubernetes API error for namespace '{ns_name}': {e.reason}"
            ) from e

        results.append(NamespaceCheckResult(
            name=ns_name,
            resource_quota=has_quota,
            limit_range=has_limit_range,
            network_policy=has_network_policy,
        ))

    return results
