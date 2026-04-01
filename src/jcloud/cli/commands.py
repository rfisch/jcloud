from __future__ import annotations

import click

from jcloud.api import commands as api
from jcloud.client import get_client, output

CMD_COLUMNS = ["_id", "name", "commandType", "command"]


@click.group()
def commands():
    """Manage JumpCloud commands."""


@commands.command("list")
@click.pass_context
def list_commands(ctx: click.Context):
    """List all commands."""
    client = get_client(ctx)
    results = api.list_commands(client)
    output(results, ctx.obj["fmt"], columns=CMD_COLUMNS)


@commands.command()
@click.argument("command_id")
@click.pass_context
def get(ctx: click.Context, command_id: str):
    """Get command details."""
    client = get_client(ctx)
    result = api.get_command(client, command_id)
    output(result, ctx.obj["fmt"])


@commands.command()
@click.option("--name", required=True)
@click.option("--command", "cmd", required=True)
@click.option("--type", "cmd_type", type=click.Choice(["linux", "mac", "windows"]), default="linux")
@click.pass_context
def create(ctx: click.Context, name: str, cmd: str, cmd_type: str):
    """Create a command."""
    client = get_client(ctx)
    result = api.create_command(client, name, cmd, cmd_type)
    click.echo(f"Created command {result['_id']}")


@commands.command()
@click.argument("command_id")
@click.option("--system-ids", default=None, help="Comma-separated system IDs")
@click.pass_context
def run(ctx: click.Context, command_id: str, system_ids: str | None):
    """Trigger a command run."""
    client = get_client(ctx)
    ids = system_ids.split(",") if system_ids else None
    result = api.run_command(client, command_id, ids)
    click.echo(f"Triggered command {command_id}")
    output(result, ctx.obj["fmt"])


@commands.command()
@click.argument("command_id")
@click.confirmation_option(prompt="Are you sure you want to delete this command?")
@click.pass_context
def delete(ctx: click.Context, command_id: str):
    """Delete a command."""
    client = get_client(ctx)
    api.delete_command(client, command_id)
    click.echo(f"Deleted command {command_id}")


@commands.command()
@click.option("--command-id", default=None, help="Filter by command ID")
@click.pass_context
def results(ctx: click.Context, command_id: str | None):
    """List command results."""
    client = get_client(ctx)
    data = api.list_results(client, command_id)
    output(data, ctx.obj["fmt"])
