from __future__ import annotations

import click

from jcloud.cli.apps import apps
from jcloud.cli.authn import authn
from jcloud.cli.commands import commands
from jcloud.cli.events import events
from jcloud.cli.groups import groups
from jcloud.cli.insights import insights
from jcloud.cli.iplists import ip_lists
from jcloud.cli.meta import meta
from jcloud.cli.policies import policies
from jcloud.cli.radius import radius
from jcloud.cli.soc2 import soc2
from jcloud.cli.systems import systems
from jcloud.cli.users import users


@click.group()
@click.option("--api-key", envvar="JUMPCLOUD_API_KEY", help="JumpCloud API key")
@click.option("--org-id", envvar="JUMPCLOUD_ORG_ID", default=None, help="Organization ID (MSP)")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format",
)
@click.pass_context
def cli(ctx: click.Context, api_key: str | None, org_id: str | None, fmt: str):
    """JumpCloud management CLI."""
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = api_key
    ctx.obj["org_id"] = org_id
    ctx.obj["fmt"] = fmt


cli.add_command(users)
cli.add_command(groups)
cli.add_command(systems)
cli.add_command(commands)
cli.add_command(policies)
cli.add_command(radius)
cli.add_command(apps)
cli.add_command(authn)
cli.add_command(events)
cli.add_command(insights)
cli.add_command(ip_lists)
cli.add_command(meta)
cli.add_command(soc2)


@cli.command("sync-state")
@click.pass_context
def sync_state(ctx: click.Context):
    """Pull all JumpCloud data and print a state summary."""
    from jcloud.api import commands as cmd_api
    from jcloud.api import systems as sys_api
    from jcloud.api import users as users_api
    from jcloud.client import get_client

    client = get_client(ctx)

    # Users
    all_users = users_api.list_users(client)
    click.echo("## Users\n")
    click.echo(
        f"{'Name':<20} {'Email':<25} {'Username':<10} {'ID':<26} {'State':<10} {'PwdSet':<6} {'MFA':<14} {'Bound System':<20} {'Sudo':<5}"
    )
    click.echo("-" * 140)
    for u in all_users:
        mfa = u.get("mfaEnrollment", {}).get("overallStatus", "?")
        r = client.get(f"/users/{u['_id']}/associations", version=2, params={"targets": ["system"]})
        bindings = r.json()
        if bindings:
            for b in bindings:
                try:
                    s = sys_api.get_system(client, b["to"]["id"])
                    sname = s.get("displayName", "?")
                except Exception:
                    sname = b["to"]["id"]
                sudo = b.get("attributes", {}).get("sudo", {}).get("enabled", False)
                click.echo(
                    f"{u['firstname'] + ' ' + u['lastname']:<20} {u['email']:<25} {u['username']:<10} {u['_id']:<26} {u['state']:<10} {str(u['activated']):<6} {mfa:<14} {sname:<20} {str(sudo):<5}"
                )
        else:
            click.echo(
                f"{u['firstname'] + ' ' + u['lastname']:<20} {u['email']:<25} {u['username']:<10} {u['_id']:<26} {u['state']:<10} {str(u['activated']):<6} {mfa:<14} {'None':<20} {'—':<5}"
            )

    # Systems
    all_systems = sys_api.list_systems(client)
    click.echo("\n## Systems\n")
    click.echo(
        f"{'Display Name':<20} {'Hostname':<32} {'OS':<12} {'Version':<10} {'ID':<26} {'Active':<7} {'FDE':<5} {'Key':<5}"
    )
    click.echo("-" * 130)
    for s in all_systems:
        fde = s.get("fde", {})
        click.echo(
            f"{s.get('displayName', '?'):<20} {s.get('hostname', '?'):<32} {s.get('os', '?'):<12} {s.get('version', '?'):<10} {s['_id']:<26} {str(s.get('active')):<7} {str(fde.get('active', '?')):<5} {str(fde.get('keyPresent', '?')):<5}"
        )

    # Commands
    all_cmds = cmd_api.list_commands(client)
    click.echo("\n## Commands\n")
    click.echo(f"{'Name':<40} {'Type':<8} {'ID':<26}")
    click.echo("-" * 76)
    for cmd in all_cmds:
        click.echo(f"{cmd['name']:<40} {cmd['commandType']:<8} {cmd['_id']:<26}")

    # Groups
    ugroups = client.paginate_v2("/usergroups")
    sgroups = client.paginate_v2("/systemgroups")
    click.echo("\n## Groups\n")
    for g in ugroups:
        click.echo(f"  user_group: {g['name']} ({g['id']})")
    for g in sgroups:
        click.echo(f"  system_group: {g['name']} ({g['id']})")

    # Directories
    dirs = client.paginate_v2("/directories")
    click.echo("\n## Integrations\n")
    for d in dirs:
        click.echo(f"  {d['type']}: {d['name']} ({d['id']})")


if __name__ == "__main__":
    cli()
