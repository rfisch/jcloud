from __future__ import annotations

import click

from jcloud.api import insights as api
from jcloud.api import systems as systems_api
from jcloud.client import get_client, output


@click.group()
def insights():
    """Query JumpCloud System Insights."""


@insights.command("tables")
@click.pass_context
def list_tables(ctx: click.Context):
    """List available System Insights tables."""
    for table in sorted(api.INSIGHT_TABLES):
        click.echo(table)


@insights.command("query")
@click.argument("table")
@click.option("--system", default=None, help="Filter to a specific system (hostname, name, or ID)")
@click.pass_context
def query(ctx: click.Context, table: str, system: str | None):
    """Query a System Insights table.

    TABLE is the insight table name (e.g. 'os_version', 'disk_encryption', 'apps').
    Run 'jcloud insights tables' to see all available tables.
    """
    client = get_client(ctx)
    if system:
        system_id = systems_api.resolve_system_id(client, system)
        results = api.query_table_for_system(client, system_id, table)
    else:
        results = api.query_table(client, table)
    output(results, ctx.obj["fmt"])


@insights.command("os")
@click.pass_context
def os_versions(ctx: click.Context):
    """Show OS versions across all systems."""
    client = get_client(ctx)
    results = api.query_table(client, "os_version")
    columns = ["system_id", "name", "version", "build", "platform"]
    output(results, ctx.obj["fmt"], columns=columns)


@insights.command("encryption")
@click.pass_context
def encryption_status(ctx: click.Context):
    """Show disk encryption status across all systems."""
    client = get_client(ctx)
    results = api.query_table(client, "disk_encryption")
    output(results, ctx.obj["fmt"])


@insights.command("apps")
@click.option("--system", default=None, help="Filter to a specific system")
@click.pass_context
def installed_apps(ctx: click.Context, system: str | None):
    """List installed applications."""
    client = get_client(ctx)
    if system:
        system_id = systems_api.resolve_system_id(client, system)
        results = api.query_table_for_system(client, system_id, "apps")
    else:
        results = api.query_table(client, "apps")
    output(results, ctx.obj["fmt"])
