from __future__ import annotations

import click

from jcloud.api import apps as api
from jcloud.client import get_client, output

APP_COLUMNS = ["_id", "name", "displayName", "ssoUrl"]


@click.group()
def apps():
    """Manage JumpCloud SSO applications."""


@apps.command("list")
@click.pass_context
def list_apps(ctx: click.Context):
    """List all applications."""
    client = get_client(ctx)
    results = api.list_apps(client)
    output(results, ctx.obj["fmt"], columns=APP_COLUMNS)


@apps.command()
@click.argument("app_id")
@click.pass_context
def get(ctx: click.Context, app_id: str):
    """Get application details."""
    client = get_client(ctx)
    result = api.get_app(client, app_id)
    output(result, ctx.obj["fmt"])


@apps.command()
@click.argument("app_id")
@click.confirmation_option(prompt="Are you sure you want to delete this application?")
@click.pass_context
def delete(ctx: click.Context, app_id: str):
    """Delete an application."""
    client = get_client(ctx)
    api.delete_app(client, app_id)
    click.echo(f"Deleted application {app_id}")
