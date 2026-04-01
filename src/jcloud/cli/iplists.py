from __future__ import annotations

import click

from jcloud.api import iplists as api
from jcloud.client import get_client, output


@click.group("ip-lists")
def ip_lists():
    """Manage JumpCloud IP lists for conditional access."""


@ip_lists.command("list")
@click.pass_context
def list_ip_lists(ctx: click.Context):
    """List all IP lists."""
    client = get_client(ctx)
    results = api.list_ip_lists(client)
    output(results, ctx.obj["fmt"])


@ip_lists.command("get")
@click.argument("list_id")
@click.pass_context
def get_ip_list(ctx: click.Context, list_id: str):
    """Get IP list details."""
    client = get_client(ctx)
    result = api.get_ip_list(client, list_id)
    output(result, ctx.obj["fmt"])


@ip_lists.command("create")
@click.option("--name", required=True, help="Name for the IP list")
@click.option("--ips", required=True, help="Comma-separated IPs or CIDRs")
@click.pass_context
def create_ip_list(ctx: click.Context, name: str, ips: str):
    """Create an IP list."""
    client = get_client(ctx)
    ip_list = [ip.strip() for ip in ips.split(",")]
    result = api.create_ip_list(client, name, ip_list)
    click.echo(f"Created IP list: {result.get('id', result.get('_id'))}")
    output(result, ctx.obj["fmt"])


@ip_lists.command("delete")
@click.argument("list_id")
@click.confirmation_option(prompt="Are you sure you want to delete this IP list?")
@click.pass_context
def delete_ip_list(ctx: click.Context, list_id: str):
    """Delete an IP list."""
    client = get_client(ctx)
    api.delete_ip_list(client, list_id)
    click.echo(f"Deleted IP list {list_id}")
