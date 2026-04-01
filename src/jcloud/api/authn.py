from __future__ import annotations

from jcloud.client import JumpCloudClient


def list_policies(client: JumpCloudClient) -> list[dict]:
    """List all authentication policies."""
    return client.paginate_v2("/authn/policies")


def get_policy(client: JumpCloudClient, policy_id: str) -> dict:
    resp = client.get(f"/authn/policies/{policy_id}", version=2)
    resp.raise_for_status()
    return resp.json()


def create_policy(client: JumpCloudClient, name: str, **kwargs) -> dict:
    body = {"name": name}
    body.update(kwargs)
    resp = client.post("/authn/policies", version=2, json=body)
    resp.raise_for_status()
    return resp.json()


def update_policy(client: JumpCloudClient, policy_id: str, **fields) -> dict:
    resp = client.patch(f"/authn/policies/{policy_id}", version=2, json=fields)
    resp.raise_for_status()
    return resp.json()


def delete_policy(client: JumpCloudClient, policy_id: str) -> None:
    resp = client.delete(f"/authn/policies/{policy_id}", version=2)
    resp.raise_for_status()
