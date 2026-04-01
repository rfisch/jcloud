from __future__ import annotations

import click

from jcloud.client import JumpCloudClient


def list_policies(client: JumpCloudClient) -> list[dict]:
    return client.paginate_v2("/policies")


def get_policy(client: JumpCloudClient, policy_id: str) -> dict:
    resp = client.get(f"/policies/{policy_id}", version=2)
    resp.raise_for_status()
    return resp.json()


def create_policy(client: JumpCloudClient, name: str, template_id: str, **values) -> dict:
    body = {"name": name, "template": {"id": template_id}, "values": values}
    resp = client.post("/policies", version=2, json=body)
    resp.raise_for_status()
    return resp.json()


def update_policy(client: JumpCloudClient, policy_id: str, **fields) -> dict:
    resp = client.put(f"/policies/{policy_id}", version=2, json=fields)
    resp.raise_for_status()
    return resp.json()


def delete_policy(client: JumpCloudClient, policy_id: str) -> None:
    resp = client.delete(f"/policies/{policy_id}", version=2)
    resp.raise_for_status()


def list_policy_results(client: JumpCloudClient, policy_id: str) -> list[dict]:
    return client.paginate_v2(f"/policies/{policy_id}/policystatuses")


def resolve_policy_id(client: JumpCloudClient, identifier: str) -> str:
    """Resolve a policy name to a policy ID. Pass-through if already an ID."""
    if len(identifier) == 24 and all(c in "0123456789abcdef" for c in identifier):
        return identifier

    policies = list_policies(client)
    for p in policies:
        if p.get("name") == identifier or p.get("id") == identifier:
            return p["id"]

    raise click.UsageError(f"Policy not found: {identifier}")


def bind_policy_to_system(client: JumpCloudClient, policy_id: str, system_id: str) -> None:
    """Bind a policy to a system."""
    resp = client.post(
        f"/policies/{policy_id}/associations",
        version=2,
        json={"id": system_id, "op": "add", "type": "system"},
    )
    resp.raise_for_status()


def unbind_policy_from_system(client: JumpCloudClient, policy_id: str, system_id: str) -> None:
    """Remove a policy-system binding."""
    resp = client.post(
        f"/policies/{policy_id}/associations",
        version=2,
        json={"id": system_id, "op": "remove", "type": "system"},
    )
    resp.raise_for_status()


def bind_policy_to_group(client: JumpCloudClient, policy_id: str, group_id: str) -> None:
    """Bind a policy to a system group."""
    resp = client.post(
        f"/policies/{policy_id}/associations",
        version=2,
        json={"id": group_id, "op": "add", "type": "system_group"},
    )
    resp.raise_for_status()


def unbind_policy_from_group(client: JumpCloudClient, policy_id: str, group_id: str) -> None:
    """Remove a policy-system group binding."""
    resp = client.post(
        f"/policies/{policy_id}/associations",
        version=2,
        json={"id": group_id, "op": "remove", "type": "system_group"},
    )
    resp.raise_for_status()


def get_policy_systems(client: JumpCloudClient, policy_id: str) -> list[dict]:
    """Get all systems bound to a policy."""
    resp = client.get(
        f"/policies/{policy_id}/associations",
        version=2,
        params={"targets": ["system"]},
    )
    resp.raise_for_status()
    return resp.json()


def get_policy_groups(client: JumpCloudClient, policy_id: str) -> list[dict]:
    """Get all system groups bound to a policy."""
    resp = client.get(
        f"/policies/{policy_id}/associations",
        version=2,
        params={"targets": ["system_group"]},
    )
    resp.raise_for_status()
    return resp.json()
