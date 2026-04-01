from __future__ import annotations

from jcloud.client import JumpCloudClient


def get_api_version(client: JumpCloudClient) -> dict:
    """Get the current JumpCloud API version and org info."""
    resp = client.get("/organizations", version=1)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if results:
        return results[0]
    return {}


def list_policy_templates(client: JumpCloudClient) -> list[dict]:
    """List all available policy templates — useful for discovering new policies."""
    return client.paginate_v2("/policytemplates")


def list_directories(client: JumpCloudClient) -> list[dict]:
    """List all configured directories (Google Workspace, LDAP, AD, etc.)."""
    return client.paginate_v2("/directories")
