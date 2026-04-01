from __future__ import annotations

import click

from jcloud.api import groups as groups_api
from jcloud.api import policies as api
from jcloud.api import systems as systems_api
from jcloud.client import get_client, output

POLICY_COLUMNS = ["id", "name", "template"]


@click.group()
def policies():
    """Manage JumpCloud policies."""


@policies.command("list")
@click.pass_context
def list_policies(ctx: click.Context):
    """List all policies."""
    client = get_client(ctx)
    results = api.list_policies(client)
    output(results, ctx.obj["fmt"], columns=POLICY_COLUMNS)


@policies.command()
@click.argument("policy_id")
@click.pass_context
def get(ctx: click.Context, policy_id: str):
    """Get policy details."""
    client = get_client(ctx)
    result = api.get_policy(client, policy_id)
    output(result, ctx.obj["fmt"])


@policies.command()
@click.argument("policy_id")
@click.confirmation_option(prompt="Are you sure you want to delete this policy?")
@click.pass_context
def delete(ctx: click.Context, policy_id: str):
    """Delete a policy."""
    client = get_client(ctx)
    api.delete_policy(client, policy_id)
    click.echo(f"Deleted policy {policy_id}")


@policies.command("results")
@click.argument("policy_id")
@click.pass_context
def policy_results(ctx: click.Context, policy_id: str):
    """List policy status results."""
    client = get_client(ctx)
    results = api.list_policy_results(client, policy_id)
    output(results, ctx.obj["fmt"])


@policies.command("bind-system")
@click.argument("policy")
@click.argument("system")
@click.pass_context
def bind_system(ctx: click.Context, policy: str, system: str):
    """Bind a policy to a system."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    system_id = systems_api.resolve_system_id(client, system)

    policy_data = api.get_policy(client, policy_id)
    system_data = systems_api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    click.echo(f"Binding policy '{policy_data['name']}' to system '{name}'")

    api.bind_policy_to_system(client, policy_id, system_id)
    click.echo("Bound successfully.")


@policies.command("unbind-system")
@click.argument("policy")
@click.argument("system")
@click.pass_context
def unbind_system(ctx: click.Context, policy: str, system: str):
    """Unbind a policy from a system."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    system_id = systems_api.resolve_system_id(client, system)

    policy_data = api.get_policy(client, policy_id)
    system_data = systems_api.get_system(client, system_id)
    name = system_data.get("displayName", system_data.get("hostname"))
    click.echo(f"Unbinding policy '{policy_data['name']}' from system '{name}'")

    api.unbind_policy_from_system(client, policy_id, system_id)
    click.echo("Unbound successfully.")


@policies.command("bind-group")
@click.argument("policy")
@click.argument("group")
@click.pass_context
def bind_group(ctx: click.Context, policy: str, group: str):
    """Bind a policy to a system group."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    group_id = groups_api.resolve_system_group_id(client, group)

    policy_data = api.get_policy(client, policy_id)
    group_data = groups_api.get_group(client, group_id, group_type="system")
    click.echo(f"Binding policy '{policy_data['name']}' to group '{group_data['name']}'")

    api.bind_policy_to_group(client, policy_id, group_id)
    click.echo("Bound successfully.")


@policies.command("unbind-group")
@click.argument("policy")
@click.argument("group")
@click.pass_context
def unbind_group(ctx: click.Context, policy: str, group: str):
    """Unbind a policy from a system group."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    group_id = groups_api.resolve_system_group_id(client, group)

    policy_data = api.get_policy(client, policy_id)
    group_data = groups_api.get_group(client, group_id, group_type="system")
    click.echo(f"Unbinding policy '{policy_data['name']}' from group '{group_data['name']}'")

    api.unbind_policy_from_group(client, policy_id, group_id)
    click.echo("Unbound successfully.")


@policies.command("systems")
@click.argument("policy")
@click.pass_context
def policy_systems(ctx: click.Context, policy: str):
    """List systems bound to a policy."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    associations = api.get_policy_systems(client, policy_id)

    if not associations:
        click.echo("No systems bound.")
        return

    rows = []
    for assoc in associations:
        sys_id = assoc["to"]["id"]
        try:
            s = systems_api.get_system(client, sys_id)
            rows.append({
                "system_id": sys_id,
                "displayName": s.get("displayName", ""),
                "hostname": s.get("hostname", ""),
                "os": s.get("os", ""),
            })
        except Exception:
            rows.append({"system_id": sys_id, "displayName": "?", "hostname": "?", "os": "?"})

    output(rows, ctx.obj["fmt"])


@policies.command("groups")
@click.argument("policy")
@click.pass_context
def policy_groups(ctx: click.Context, policy: str):
    """List system groups bound to a policy."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    associations = api.get_policy_groups(client, policy_id)

    if not associations:
        click.echo("No groups bound.")
        return

    rows = []
    for assoc in associations:
        grp_id = assoc["to"]["id"]
        try:
            g = groups_api.get_group(client, grp_id, group_type="system")
            rows.append({"group_id": grp_id, "name": g.get("name", "")})
        except Exception:
            rows.append({"group_id": grp_id, "name": "?"})

    output(rows, ctx.obj["fmt"])


@policies.command("compliance")
@click.argument("policy")
@click.pass_context
def compliance(ctx: click.Context, policy: str):
    """Show policy compliance across all bound systems."""
    client = get_client(ctx)
    policy_id = api.resolve_policy_id(client, policy)
    policy_data = api.get_policy(client, policy_id)
    results = api.list_policy_results(client, policy_id)

    if not results:
        click.echo(f"No compliance data for policy '{policy_data['name']}'.")
        return

    rows = []
    compliant = 0
    for r in results:
        sys_id = r.get("systemID", r.get("system_id", ""))
        success = r.get("success", False)
        try:
            s = systems_api.get_system(client, sys_id)
            name = s.get("displayName", s.get("hostname", sys_id))
        except Exception:
            name = sys_id
        if success:
            compliant += 1
        rows.append({
            "system": name,
            "system_id": sys_id,
            "success": success,
            "started_at": r.get("startedAt", ""),
            "ended_at": r.get("endedAt", ""),
        })

    output(rows, ctx.obj["fmt"])

    total = len(rows)
    pct = 100 * compliant // total if total else 0
    click.echo(f"\nCompliance: {compliant}/{total} systems ({pct}%)")
