from __future__ import annotations

from jcloud.client import JumpCloudClient


def list_apps(client: JumpCloudClient) -> list[dict]:
    return client.paginate_v2("/applications")


def get_app(client: JumpCloudClient, app_id: str) -> dict:
    resp = client.get(f"/applications/{app_id}", version=2)
    resp.raise_for_status()
    return resp.json()


def create_app(client: JumpCloudClient, name: str, sso_url: str, **kwargs) -> dict:
    body = {"name": name, "ssoUrl": sso_url}
    body.update(kwargs)
    resp = client.post("/applications", version=2, json=body)
    resp.raise_for_status()
    return resp.json()


def delete_app(client: JumpCloudClient, app_id: str) -> None:
    resp = client.delete(f"/applications/{app_id}", version=2)
    resp.raise_for_status()
