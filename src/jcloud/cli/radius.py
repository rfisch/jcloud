from __future__ import annotations

import click

from jcloud.api import radius as api
from jcloud.client import get_client, output

RADIUS_COLUMNS = ["_id", "name", "networkSourceIp"]


@click.group()
def radius():
    """Manage JumpCloud RADIUS servers."""


@radius.command("list")
@click.pass_context
def list_servers(ctx: click.Context):
    """List all RADIUS servers."""
    client = get_client(ctx)
    results = api.list_servers(client)
    output(results, ctx.obj["fmt"], columns=RADIUS_COLUMNS)


@radius.command()
@click.argument("server_id")
@click.pass_context
def get(ctx: click.Context, server_id: str):
    """Get RADIUS server details."""
    client = get_client(ctx)
    result = api.get_server(client, server_id)
    output(result, ctx.obj["fmt"])


@radius.command()
@click.option("--name", required=True)
@click.option("--ip", "network_source_ip", required=True, help="Network source IP")
@click.option("--secret", "shared_secret", required=True, help="Shared secret")
@click.pass_context
def create(ctx: click.Context, name: str, network_source_ip: str, shared_secret: str):
    """Create a RADIUS server."""
    client = get_client(ctx)
    result = api.create_server(client, name, network_source_ip, shared_secret)
    click.echo(f"Created RADIUS server {result['_id']}")


@radius.command()
@click.argument("server_id")
@click.confirmation_option(prompt="Are you sure you want to delete this RADIUS server?")
@click.pass_context
def delete(ctx: click.Context, server_id: str):
    """Delete a RADIUS server."""
    client = get_client(ctx)
    api.delete_server(client, server_id)
    click.echo(f"Deleted RADIUS server {server_id}")
