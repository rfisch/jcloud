from __future__ import annotations

import click

from jcloud.api import events as api
from jcloud.client import get_client, output

EVENT_COLUMNS = ["timestamp", "event_type", "initiated_by", "resource", "success"]

SERVICES = [
    "all",
    "directory",
    "ldap",
    "mdm",
    "password_manager",
    "radius",
    "software",
    "sso",
    "systems",
]


@click.group()
def events():
    """Query JumpCloud Directory Insights events."""


@events.command("list")
@click.option(
    "--service",
    type=click.Choice(SERVICES),
    default="all",
    help="Event service to query",
)
@click.option("--start", "start_date", default=None, help="Start date (ISO 8601)")
@click.option("--end", "end_date", default=None, help="End date (ISO 8601)")
@click.option("--search", "search_term", default=None, help="Filter by keyword")
@click.option("--limit", default=100, help="Max results")
@click.pass_context
def list_events(
    ctx: click.Context,
    service: str,
    start_date: str | None,
    end_date: str | None,
    search_term: str | None,
    limit: int,
):
    """List events from Directory Insights."""
    client = get_client(ctx)
    results = api.query_events(
        client,
        service=service,
        start_date=start_date,
        end_date=end_date,
        search_term=search_term,
        limit=limit,
    )
    output(results, ctx.obj["fmt"])


@events.command("logins")
@click.option("--start", "start_date", default=None, help="Start date (ISO 8601)")
@click.option("--end", "end_date", default=None, help="End date (ISO 8601)")
@click.option("--limit", default=100, help="Max results")
@click.pass_context
def logins(ctx: click.Context, start_date: str | None, end_date: str | None, limit: int):
    """Show login events (SSO and directory)."""
    client = get_client(ctx)
    results = api.query_events(
        client,
        service="sso",
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )
    output(results, ctx.obj["fmt"])


@events.command("count")
@click.option(
    "--service",
    type=click.Choice(SERVICES),
    default="all",
    help="Event service to query",
)
@click.option("--start", "start_date", default=None, help="Start date (ISO 8601)")
@click.option("--end", "end_date", default=None, help="End date (ISO 8601)")
@click.pass_context
def count(ctx: click.Context, service: str, start_date: str | None, end_date: str | None):
    """Get event counts."""
    client = get_client(ctx)
    result = api.count_events(client, service=service, start_date=start_date, end_date=end_date)
    output(result, ctx.obj["fmt"])
