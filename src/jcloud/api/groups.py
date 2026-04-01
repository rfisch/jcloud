from __future__ import annotations

import click

from jcloud.client import JumpCloudClient


def list_user_groups(client: JumpCloudClient) -> list[dict]:
    return client.paginate_v2("/usergroups")


def list_system_groups(client: JumpCloudClient) -> list[dict]:
    return client.paginate_v2("/systemgroups")


def get_group(client: JumpCloudClient, group_id: str, group_type: str = "user") -> dict:
    endpoint = "usergroups" if group_type == "user" else "systemgroups"
    resp = client.get(f"/{endpoint}/{group_id}", version=2)
    resp.raise_for_status()
    return resp.json()


def create_user_group(client: JumpCloudClient, name: str) -> dict:
    resp = client.post("/usergroups", version=2, json={"name": name})
    resp.raise_for_status()
    return resp.json()


def create_system_group(client: JumpCloudClient, name: str) -> dict:
    resp = client.post("/systemgroups", version=2, json={"name": name})
    resp.raise_for_status()
    return resp.json()


def delete_group(client: JumpCloudClient, group_id: str, group_type: str = "user") -> None:
    endpoint = "usergroups" if group_type == "user" else "systemgroups"
    resp = client.delete(f"/{endpoint}/{group_id}", version=2)
    resp.raise_for_status()


def list_members(client: JumpCloudClient, group_id: str, group_type: str = "user") -> list[dict]:
    endpoint = "usergroups" if group_type == "user" else "systemgroups"
    return client.paginate_v2(f"/{endpoint}/{group_id}/members")


def modify_membership(
    client: JumpCloudClient,
    group_id: str,
    member_id: str,
    op: str = "add",
    group_type: str = "user",
    member_type: str = "user",
) -> None:
    endpoint = "usergroups" if group_type == "user" else "systemgroups"
    body = {"op": op, "type": member_type, "id": member_id}
    resp = client.post(f"/{endpoint}/{group_id}/members", version=2, json=body)
    resp.raise_for_status()


def resolve_system_group_id(client: JumpCloudClient, identifier: str) -> str:
    """Resolve a system group name to an ID. Pass-through if already an ID."""
    if len(identifier) == 24 and all(c in "0123456789abcdef" for c in identifier):
        return identifier

    groups = list_system_groups(client)
    for g in groups:
        if g.get("name") == identifier or g.get("id") == identifier:
            return g["id"]

    raise click.UsageError(f"System group not found: {identifier}")
