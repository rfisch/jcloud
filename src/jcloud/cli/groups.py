from __future__ import annotations

import click

from jcloud.api import groups as api
from jcloud.client import get_client, output

GROUP_COLUMNS = ["id", "name", "type"]


@click.group()
def groups():
    """Manage JumpCloud user and system groups."""


@groups.command("list")
@click.option(
    "--type",
    "group_type",
    type=click.Choice(["user", "system"]),
    default="user",
    help="Group type",
)
@click.pass_context
def list_groups(ctx: click.Context, group_type: str):
    """List groups."""
    client = get_client(ctx)
    if group_type == "user":
        results = api.list_user_groups(client)
    else:
        results = api.list_system_groups(client)
    output(results, ctx.obj["fmt"], columns=GROUP_COLUMNS)


@groups.command()
@click.argument("group_id")
@click.option("--type", "group_type", type=click.Choice(["user", "system"]), default="user")
@click.pass_context
def get(ctx: click.Context, group_id: str, group_type: str):
    """Get group details."""
    client = get_client(ctx)
    result = api.get_group(client, group_id, group_type)
    output(result, ctx.obj["fmt"])


@groups.command()
@click.argument("name")
@click.option("--type", "group_type", type=click.Choice(["user", "system"]), default="user")
@click.pass_context
def create(ctx: click.Context, name: str, group_type: str):
    """Create a group."""
    client = get_client(ctx)
    if group_type == "user":
        result = api.create_user_group(client, name)
    else:
        result = api.create_system_group(client, name)
    click.echo(f"Created {group_type} group: {result.get('id', result.get('_id'))}")


@groups.command()
@click.argument("group_id")
@click.option("--type", "group_type", type=click.Choice(["user", "system"]), default="user")
@click.confirmation_option(prompt="Are you sure you want to delete this group?")
@click.pass_context
def delete(ctx: click.Context, group_id: str, group_type: str):
    """Delete a group."""
    client = get_client(ctx)
    api.delete_group(client, group_id, group_type)
    click.echo(f"Deleted group {group_id}")


@groups.command()
@click.argument("group_id")
@click.option("--type", "group_type", type=click.Choice(["user", "system"]), default="user")
@click.pass_context
def members(ctx: click.Context, group_id: str, group_type: str):
    """List group members."""
    client = get_client(ctx)
    results = api.list_members(client, group_id, group_type)
    output(results, ctx.obj["fmt"])


@groups.command("add-member")
@click.argument("group_id")
@click.argument("member_id")
@click.option("--type", "group_type", type=click.Choice(["user", "system"]), default="user")
@click.pass_context
def add_member(ctx: click.Context, group_id: str, member_id: str, group_type: str):
    """Add a member to a group."""
    client = get_client(ctx)
    member_type = "user" if group_type == "user" else "system"
    api.modify_membership(client, group_id, member_id, "add", group_type, member_type)
    click.echo(f"Added {member_id} to group {group_id}")


@groups.command("remove-member")
@click.argument("group_id")
@click.argument("member_id")
@click.option("--type", "group_type", type=click.Choice(["user", "system"]), default="user")
@click.pass_context
def remove_member(ctx: click.Context, group_id: str, member_id: str, group_type: str):
    """Remove a member from a group."""
    client = get_client(ctx)
    member_type = "user" if group_type == "user" else "system"
    api.modify_membership(client, group_id, member_id, "remove", group_type, member_type)
    click.echo(f"Removed {member_id} from group {group_id}")
