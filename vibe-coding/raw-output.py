#!/usr/bin/env python3
"""Check Kubernetes namespaces for resource quotas."""

from kubernetes import client, config


def check_quotas():
    # Load kubeconfig
    config.load_kube_config()

    v1 = client.CoreV1Api()

    # Get all namespaces
    namespaces = v1.list_namespace()

    print("Checking namespaces for resource quotas...")
    print("-" * 50)

    for ns in namespaces.items:
        ns_name = ns.metadata.name
        quotas = v1.list_namespaced_resource_quota(ns_name)

        if quotas.items:
            status = "OK - has quota"
        else:
            status = "WARNING - no quota"

        print(f"  {ns_name}: {status}")

    print("-" * 50)
    print("Done!")


if __name__ == "__main__":
    check_quotas()
