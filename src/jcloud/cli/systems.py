from __future__ import annotations

import click

from jcloud.api import systems as api
from jcloud.client import get_client, output

SYSTEM_COLUMNS = ["_id", "displayName", "os", "version", "hostname", "active"]


@click.group()
def systems():
    """Manage JumpCloud systems."""


@systems.command("list")
@click.pass_context
def list_systems(ctx: click.Context):
    """List all systems."""
    client = get_client(ctx)
    results = api.list_systems(client)
    output(results, ctx.obj["fmt"], columns=SYSTEM_COLUMNS)


@systems.command()
@click.argument("system_id")
@click.pass_context
def get(ctx: click.Context, system_id: str):
    """Get system details."""
    client = get_client(ctx)
    result = api.get_system(client, system_id)
    output(result, ctx.obj["fmt"])


@systems.command()
@click.argument("system_id")
@click.confirmation_option(prompt="Are you sure you want to delete this system?")
@click.pass_context
def delete(ctx: click.Context, system_id: str):
    """Delete a system."""
    client = get_client(ctx)
    api.delete_system(client, system_id)
    click.echo(f"Deleted system {system_id}")


@systems.command("lock")
@click.argument("system")
@click.option("--pin", default="", help="PIN to unlock (macOS/Windows)")
@click.confirmation_option(prompt="Are you sure you want to LOCK this system?")
@click.pass_context
def lock_system(ctx: click.Context, system: str, pin: str):
    """Lock a system remotely."""
    client = get_client(ctx)
    system_id = api.resolve_system_id(client, system)
    system_data = api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    api.lock_system(client, system_id, pin=pin)
    click.echo(f"Locked system '{name}'")


@systems.command("erase")
@click.argument("system")
@click.confirmation_option(prompt="THIS WILL WIPE THE DEVICE. Are you absolutely sure?")
@click.pass_context
def erase_system(ctx: click.Context, system: str):
    """Remote wipe a system. DESTRUCTIVE — erases all data."""
    client = get_client(ctx)
    system_id = api.resolve_system_id(client, system)
    system_data = api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    api.erase_system(client, system_id)
    click.echo(f"Erase command sent to '{name}'")


@systems.command("restart")
@click.argument("system")
@click.confirmation_option(prompt="Are you sure you want to RESTART this system?")
@click.pass_context
def restart_system(ctx: click.Context, system: str):
    """Restart a system remotely."""
    client = get_client(ctx)
    system_id = api.resolve_system_id(client, system)
    system_data = api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    api.restart_system(client, system_id)
    click.echo(f"Restart command sent to '{name}'")


@systems.command("shutdown")
@click.argument("system")
@click.confirmation_option(prompt="Are you sure you want to SHUT DOWN this system?")
@click.pass_context
def shutdown_system(ctx: click.Context, system: str):
    """Shut down a system remotely."""
    client = get_client(ctx)
    system_id = api.resolve_system_id(client, system)
    system_data = api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    api.shutdown_system(client, system_id)
    click.echo(f"Shutdown command sent to '{name}'")


@systems.command("fde-key")
@click.argument("system")
@click.pass_context
def fde_key(ctx: click.Context, system: str):
    """Get the FileVault/BitLocker recovery key for a system."""
    client = get_client(ctx)
    system_id = api.resolve_system_id(client, system)
    system_data = api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    result = api.get_fde_key(client, system_id)
    click.echo(f"Recovery key for '{name}':")
    output(result, ctx.obj["fmt"])


@systems.command("policy-status")
@click.argument("system")
@click.pass_context
def policy_status(ctx: click.Context, system: str):
    """Show policy compliance status for a system."""
    client = get_client(ctx)
    system_id = api.resolve_system_id(client, system)
    results = api.get_system_policy_statuses(client, system_id)
    output(results, ctx.obj["fmt"])


@systems.command("users")
@click.argument("system_id")
@click.pass_context
def system_users(ctx: click.Context, system_id: str):
    """List users bound to a system."""
    client = get_client(ctx)
    results = api.list_system_users(client, system_id)
    output(results, ctx.obj["fmt"])


@systems.command("force-sync")
@click.argument("system", required=False)
@click.option("--all", "sync_all", is_flag=True, help="Sync all active systems")
@click.pass_context
def force_sync(ctx: click.Context, system: str | None, sync_all: bool):
    """Force agent check-in on a system or all systems.

    SYSTEM can be a hostname, displayName, or JumpCloud system ID.
    Use --all to sync every active system.
    """
    from jcloud.api import commands as cmd_api

    client = get_client(ctx)

    if sync_all:
        all_systems = api.list_systems(client)
        active = [s for s in all_systems if s.get("active")]
        if not active:
            click.echo("No active systems found.")
            return
        system_ids = [s["_id"] for s in active]
        count = cmd_api.force_sync_systems(client, system_ids, systems_cache=active)
        click.echo(f"Triggered agent sync on {count} active system(s).")
    elif system:
        system_id = api.resolve_system_id(client, system)
        system_data = api.get_system(client, system_id)
        name = system_data.get("displayName", system_data.get("hostname"))
        count = cmd_api.force_sync_systems(client, [system_id], systems_cache=[system_data])
        click.echo(f"Triggered agent sync on '{name}'.")
    else:
        raise click.UsageError("Provide a SYSTEM or use --all.")
