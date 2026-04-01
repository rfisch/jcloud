from __future__ import annotations

from jcloud.client import JumpCloudClient


def list_commands(client: JumpCloudClient) -> list[dict]:
    return client.paginate("/commands")


def get_command(client: JumpCloudClient, command_id: str) -> dict:
    resp = client.get(f"/commands/{command_id}")
    resp.raise_for_status()
    return resp.json()


def create_command(
    client: JumpCloudClient,
    name: str,
    command: str,
    command_type: str = "linux",
    **kwargs,
) -> dict:
    body = {"name": name, "command": command, "commandType": command_type}
    body.update(kwargs)
    resp = client.post("/commands", json=body)
    resp.raise_for_status()
    return resp.json()


def update_command(client: JumpCloudClient, command_id: str, **fields) -> dict:
    resp = client.put(f"/commands/{command_id}", json=fields)
    resp.raise_for_status()
    return resp.json()


def delete_command(client: JumpCloudClient, command_id: str) -> None:
    resp = client.delete(f"/commands/{command_id}")
    resp.raise_for_status()


def run_command(
    client: JumpCloudClient, command_id: str, system_ids: list[str] | None = None
) -> dict:
    body: dict = {"_id": command_id}
    if system_ids:
        body["systems"] = system_ids
    resp = client.post("/runCommand", json=body)
    resp.raise_for_status()
    return resp.json()


def list_results(client: JumpCloudClient, command_id: str | None = None) -> list[dict]:
    if command_id:
        return client.paginate(f"/commandresults?filter=command:{command_id}")
    return client.paginate("/commandresults")


# Map JumpCloud OS names to command types
_OS_TO_CMD_TYPE = {
    "Mac OS X": "mac",
    "Windows": "windows",
    "Linux": "linux",
}

_SYNC_CMD_NAMES = {
    "mac": "Force agent check-in",
    "windows": "Force agent check-in (Windows)",
    "linux": "Force agent check-in (Linux)",
}

_SYNC_CMD_BODY = {
    "mac": "echo sync",
    "windows": "echo sync",
    "linux": "echo sync",
}


def force_sync_systems(
    client: JumpCloudClient,
    system_ids: list[str],
    systems_cache: list[dict] | None = None,
) -> int:
    """Force agent check-in on systems, using OS-appropriate commands.

    Returns the number of systems synced.
    """
    from jcloud.api import systems as systems_api

    # Group system IDs by OS command type
    by_type: dict[str, list[str]] = {}
    for sid in system_ids:
        if systems_cache:
            sys_data = next((s for s in systems_cache if s["_id"] == sid), None)
        else:
            sys_data = None
        if not sys_data:
            sys_data = systems_api.get_system(client, sid)
        os_name = sys_data.get("os", "")
        cmd_type = _OS_TO_CMD_TYPE.get(os_name, "linux")
        by_type.setdefault(cmd_type, []).append(sid)

    # Find or create sync commands per OS type, then run
    commands = list_commands(client)
    total = 0
    for cmd_type, sids in by_type.items():
        name = _SYNC_CMD_NAMES[cmd_type]
        sync_cmd = next((c for c in commands if c["name"] == name), None)
        if not sync_cmd:
            sync_cmd = create_command(
                client, name=name, command=_SYNC_CMD_BODY[cmd_type], command_type=cmd_type,
            )
        run_command(client, sync_cmd["_id"], system_ids=sids)
        total += len(sids)

    return total
