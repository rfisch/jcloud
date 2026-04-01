from __future__ import annotations

import click

from jcloud.api import meta as api
from jcloud.client import get_client, output


@click.group()
def meta():
    """JumpCloud API metadata and discovery."""


@meta.command("org")
@click.pass_context
def org_info(ctx: click.Context):
    """Show organization info and API settings."""
    client = get_client(ctx)
    result = api.get_api_version(client)
    output(result, ctx.obj["fmt"])


@meta.command("policy-templates")
@click.pass_context
def policy_templates(ctx: click.Context):
    """List all available policy templates."""
    client = get_client(ctx)
    results = api.list_policy_templates(client)
    columns = ["id", "name", "osMetaFamily", "description"]
    output(results, ctx.obj["fmt"], columns=columns)


@meta.command("directories")
@click.pass_context
def directories(ctx: click.Context):
    """List configured directories (Google Workspace, LDAP, AD)."""
    client = get_client(ctx)
    results = api.list_directories(client)
    output(results, ctx.obj["fmt"])
