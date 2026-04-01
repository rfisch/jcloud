from __future__ import annotations

import click

from jcloud.client import JumpCloudClient


def list_users(client: JumpCloudClient) -> list[dict]:
    return client.paginate("/systemusers")


def get_user(client: JumpCloudClient, user_id: str) -> dict:
    resp = client.get(f"/systemusers/{user_id}")
    resp.raise_for_status()
    return resp.json()


def create_user(
    client: JumpCloudClient,
    username: str,
    email: str,
    firstname: str = "",
    lastname: str = "",
    **kwargs,
) -> dict:
    body = {"username": username, "email": email}
    if firstname:
        body["firstname"] = firstname
    if lastname:
        body["lastname"] = lastname
    body.update(kwargs)
    resp = client.post("/systemusers", json=body)
    resp.raise_for_status()
    return resp.json()


def update_user(client: JumpCloudClient, user_id: str, **fields) -> dict:
    resp = client.put(f"/systemusers/{user_id}", json=fields)
    resp.raise_for_status()
    return resp.json()


def delete_user(client: JumpCloudClient, user_id: str) -> None:
    resp = client.delete(f"/systemusers/{user_id}")
    resp.raise_for_status()


def lock_user(client: JumpCloudClient, user_id: str) -> dict:
    return update_user(client, user_id, account_locked=True)


def unlock_user(client: JumpCloudClient, user_id: str) -> dict:
    return update_user(client, user_id, account_locked=False)


def reset_mfa(client: JumpCloudClient, user_id: str) -> None:
    resp = client.post(f"/systemusers/{user_id}/resetmfa", json={"exclusion": True})
    resp.raise_for_status()


def bind_user_to_system(
    client: JumpCloudClient,
    user_id: str,
    system_id: str,
    sudo: bool = False,
    sudo_without_password: bool = False,
) -> None:
    """Bind a user to a system. Username must match local account to take over."""
    resp = client.post(
        f"/users/{user_id}/associations",
        version=2,
        json={
            "id": system_id,
            "op": "add",
            "type": "system",
            "attributes": {
                "sudo": {
                    "enabled": sudo,
                    "withoutPassword": sudo_without_password,
                }
            },
        },
    )
    resp.raise_for_status()

    # Set as primary user on the system
    client.put(f"/systems/{system_id}", json={"primarySystemUser": {"id": user_id}})


def unbind_user_from_system(client: JumpCloudClient, user_id: str, system_id: str) -> None:
    """Remove a user-system binding."""
    resp = client.post(
        f"/users/{user_id}/associations",
        version=2,
        json={
            "id": system_id,
            "op": "remove",
            "type": "system",
        },
    )
    resp.raise_for_status()


def get_user_systems(client: JumpCloudClient, user_id: str) -> list[dict]:
    """Get all systems bound to a user."""
    resp = client.get(
        f"/users/{user_id}/associations",
        version=2,
        params={"targets": ["system"]},
    )
    resp.raise_for_status()
    return resp.json()


def expire_password(client: JumpCloudClient, user_id: str) -> None:
    """Force user to change password on next login."""
    resp = client.post(f"/systemusers/{user_id}/expire", json={})
    resp.raise_for_status()


def suspend_user(client: JumpCloudClient, user_id: str) -> None:
    """Suspend a user account."""
    resp = client.post(f"/systemusers/{user_id}/state/suspend", json={})
    resp.raise_for_status()


def activate_user(client: JumpCloudClient, user_id: str) -> None:
    """Re-activate a suspended user account."""
    resp = client.post(f"/systemusers/{user_id}/state/activate", json={})
    resp.raise_for_status()


def resolve_user_id(client: JumpCloudClient, identifier: str) -> str:
    """Resolve a username or email to a user ID. Pass-through if already an ID."""
    # If it looks like a 24-char hex ID, return as-is
    if len(identifier) == 24 and all(c in "0123456789abcdef" for c in identifier):
        return identifier

    # Search by username or email
    users = list_users(client)
    for u in users:
        if u.get("username") == identifier or u.get("email") == identifier:
            return u["_id"]

    raise click.UsageError(f"User not found: {identifier}")
