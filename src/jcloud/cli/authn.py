from __future__ import annotations

import click

from jcloud.api import authn as api
from jcloud.client import get_client, output


@click.group()
def authn():
    """Manage JumpCloud authentication policies."""


@authn.command("list")
@click.pass_context
def list_policies(ctx: click.Context):
    """List all authentication policies."""
    client = get_client(ctx)
    results = api.list_policies(client)
    output(results, ctx.obj["fmt"])


@authn.command("get")
@click.argument("policy_id")
@click.pass_context
def get_policy(ctx: click.Context, policy_id: str):
    """Get authentication policy details."""
    client = get_client(ctx)
    result = api.get_policy(client, policy_id)
    output(result, ctx.obj["fmt"])


@authn.command("create")
@click.option("--name", required=True, help="Policy name")
@click.option("--type", "policy_type", default="user_portal",
              help="Policy type (user_portal, device_login, sso, radius)")
@click.option("--mfa-required/--no-mfa-required", default=False,
              help="Require MFA for this policy")
@click.option("--device-trust/--no-device-trust", default=False,
              help="Allow managed devices to bypass MFA")
@click.option("--disabled/--enabled", default=False,
              help="Create the policy in disabled state")
@click.pass_context
def create_policy(ctx: click.Context, name: str, policy_type: str,
                  mfa_required: bool, device_trust: bool, disabled: bool):
    """Create an authentication policy."""
    client = get_client(ctx)
    kwargs = {
        "type": policy_type,
        "disabled": disabled,
        "mfaRequired": mfa_required,
    }
    if device_trust:
        kwargs["conditions"] = {
            "deviceTrust": {"enabled": True},
        }
    result = api.create_policy(client, name, **kwargs)
    policy_id = result.get("id", result.get("_id", ""))
    state = "DISABLED" if disabled else "ENABLED"
    click.echo(f"Created auth policy {policy_id} ({state})")
    output(result, ctx.obj["fmt"])


@authn.command("update")
@click.argument("policy_id")
@click.option("--name", default=None, help="New policy name")
@click.option("--mfa-required/--no-mfa-required", default=None,
              help="Require MFA for this policy")
@click.option("--disabled/--enabled", default=None,
              help="Disable or enable the policy")
@click.pass_context
def update_policy(ctx: click.Context, policy_id: str, name: str | None,
                  mfa_required: bool | None, disabled: bool | None):
    """Update an authentication policy."""
    client = get_client(ctx)
    fields = {}
    if name is not None:
        fields["name"] = name
    if mfa_required is not None:
        fields["mfaRequired"] = mfa_required
    if disabled is not None:
        fields["disabled"] = disabled
    if not fields:
        click.echo("No changes specified.")
        return
    result = api.update_policy(client, policy_id, **fields)
    click.echo(f"Updated auth policy {policy_id}")
    output(result, ctx.obj["fmt"])


@authn.command("delete")
@click.argument("policy_id")
@click.confirmation_option(prompt="Are you sure you want to delete this auth policy?")
@click.pass_context
def delete_policy(ctx: click.Context, policy_id: str):
    """Delete an authentication policy."""
    client = get_client(ctx)
    api.delete_policy(client, policy_id)
    click.echo(f"Deleted auth policy {policy_id}")
