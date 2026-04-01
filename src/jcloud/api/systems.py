from __future__ import annotations

import click

from jcloud.client import JumpCloudClient


def list_systems(client: JumpCloudClient) -> list[dict]:
    return client.paginate("/systems")


def get_system(client: JumpCloudClient, system_id: str) -> dict:
    resp = client.get(f"/systems/{system_id}")
    resp.raise_for_status()
    return resp.json()


def delete_system(client: JumpCloudClient, system_id: str) -> None:
    resp = client.delete(f"/systems/{system_id}")
    resp.raise_for_status()


def list_system_users(client: JumpCloudClient, system_id: str) -> list[dict]:
    return client.paginate_v2(f"/systems/{system_id}/users")


def lock_system(client: JumpCloudClient, system_id: str, pin: str = "") -> None:
    """Lock a system remotely."""
    body: dict = {}
    if pin:
        body["pin"] = pin
    resp = client.post(f"/systems/{system_id}/command/builtin/lock", json=body)
    resp.raise_for_status()


def erase_system(client: JumpCloudClient, system_id: str) -> None:
    """Remote wipe a system."""
    resp = client.post(f"/systems/{system_id}/command/builtin/erase", json={})
    resp.raise_for_status()


def restart_system(client: JumpCloudClient, system_id: str) -> None:
    """Restart a system remotely."""
    resp = client.post(f"/systems/{system_id}/command/builtin/restart", json={})
    resp.raise_for_status()


def shutdown_system(client: JumpCloudClient, system_id: str) -> None:
    """Shut down a system remotely."""
    resp = client.post(f"/systems/{system_id}/command/builtin/shutdown", json={})
    resp.raise_for_status()


def get_fde_key(client: JumpCloudClient, system_id: str) -> dict:
    """Get the FileVault/BitLocker recovery key for a system."""
    resp = client.get(f"/systems/{system_id}/fdekey", version=2)
    resp.raise_for_status()
    return resp.json()


def get_system_policy_statuses(client: JumpCloudClient, system_id: str) -> list[dict]:
    """List policy compliance statuses for a system."""
    return client.paginate_v2(f"/systems/{system_id}/policystatuses")


def resolve_system_id(client: JumpCloudClient, identifier: str) -> str:
    """Resolve a hostname or displayName to a system ID. Pass-through if already an ID."""
    if len(identifier) == 24 and all(c in "0123456789abcdef" for c in identifier):
        return identifier

    systems = list_systems(client)
    for s in systems:
        if (
            s.get("hostname") == identifier
            or s.get("displayName") == identifier
            or s.get("_id") == identifier
        ):
            return s["_id"]

    raise click.UsageError(f"System not found: {identifier}")
