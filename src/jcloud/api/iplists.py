from __future__ import annotations

from jcloud.client import JumpCloudClient


def list_ip_lists(client: JumpCloudClient) -> list[dict]:
    """List all IP lists."""
    return client.paginate_v2("/iplists")


def get_ip_list(client: JumpCloudClient, list_id: str) -> dict:
    resp = client.get(f"/iplists/{list_id}", version=2)
    resp.raise_for_status()
    return resp.json()


def create_ip_list(client: JumpCloudClient, name: str, ips: list[str], **kwargs) -> dict:
    body = {"name": name, "ips": ips}
    body.update(kwargs)
    resp = client.post("/iplists", version=2, json=body)
    resp.raise_for_status()
    return resp.json()


def update_ip_list(client: JumpCloudClient, list_id: str, **fields) -> dict:
    resp = client.put(f"/iplists/{list_id}", version=2, json=fields)
    resp.raise_for_status()
    return resp.json()


def delete_ip_list(client: JumpCloudClient, list_id: str) -> None:
    resp = client.delete(f"/iplists/{list_id}", version=2)
    resp.raise_for_status()
