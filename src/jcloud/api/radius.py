from __future__ import annotations

from jcloud.client import JumpCloudClient


def list_servers(client: JumpCloudClient) -> list[dict]:
    return client.paginate("/radiusservers")


def get_server(client: JumpCloudClient, server_id: str) -> dict:
    resp = client.get(f"/radiusservers/{server_id}")
    resp.raise_for_status()
    return resp.json()


def create_server(
    client: JumpCloudClient,
    name: str,
    network_source_ip: str,
    shared_secret: str,
    **kwargs,
) -> dict:
    body = {"name": name, "networkSourceIp": network_source_ip, "sharedSecret": shared_secret}
    body.update(kwargs)
    resp = client.post("/radiusservers", json=body)
    resp.raise_for_status()
    return resp.json()


def update_server(client: JumpCloudClient, server_id: str, **fields) -> dict:
    resp = client.put(f"/radiusservers/{server_id}", json=fields)
    resp.raise_for_status()
    return resp.json()


def delete_server(client: JumpCloudClient, server_id: str) -> None:
    resp = client.delete(f"/radiusservers/{server_id}")
    resp.raise_for_status()
