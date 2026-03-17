"""PrometheusRule YAML template generator."""

from pathlib import Path
from typing import Optional

import yaml


PROMETHEUS_RULE_TEMPLATE: dict = {
    "apiVersion": "monitoring.coreos.com/v1",
    "kind": "PrometheusRule",
    "metadata": {
        "name": "namespace-compliance-alerts",
        "labels": {
            "app": "ns-guardian",
        },
    },
    "spec": {
        "groups": [
            {
                "name": "namespace-compliance",
                "rules": [
                    {
                        "alert": "NamespaceMissingComplianceResources",
                        "expr": (
                            "kube_namespace_labels{namespace!~\"kube-system|kube-public|kube-node-lease|default|openshift-.*\"} "
                            "unless on(namespace) kube_resourcequota{namespace!=\"\"}"
                        ),
                        "for": "10m",
                        "labels": {
                            "severity": "warning",
                        },
                        "annotations": {
                            "summary": "Namespace {{ $labels.namespace }} is missing compliance resources",
                            "description": (
                                "The namespace {{ $labels.namespace }} is missing one or more required "
                                "compliance resources (ResourceQuota, LimitRange, or NetworkPolicy)."
                            ),
                        },
                    },
                ],
            },
        ],
    },
}


def generate_prometheus_rule() -> str:
    """Generate a PrometheusRule YAML string.

    Returns:
        A YAML string containing the PrometheusRule definition.
    """
    return yaml.dump(PROMETHEUS_RULE_TEMPLATE, default_flow_style=False, sort_keys=False)


def write_prometheus_rule(output_path: Optional[str] = None) -> str:
    """Generate and optionally write a PrometheusRule YAML.

    Args:
        output_path: If provided, write the YAML to this file path.

    Returns:
        The generated YAML string.
    """
    yaml_content = generate_prometheus_rule()

    if output_path:
        Path(output_path).write_text(yaml_content)

    return yaml_content
