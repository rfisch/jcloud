from __future__ import annotations

import json

import click

from jcloud.api import soc2 as api
from jcloud.api import systems as systems_api
from jcloud.client import get_client


@click.group()
def soc2():
    """SOC 2 Type II compliance reports."""


@soc2.command("report")
@click.option("--system", "target_systems", multiple=True, help="Target specific system(s)")
@click.pass_context
def report(ctx: click.Context, target_systems: tuple[str, ...]):
    """Generate a SOC 2 Type II compliance report.

    Evaluates all managed systems against SOC 2 controls and produces
    a consolidated findings report. Use --system to target specific systems.
    """
    client = get_client(ctx)
    fmt = ctx.obj["fmt"]

    # Resolve system identifiers to IDs
    system_ids = None
    if target_systems:
        system_ids = [systems_api.resolve_system_id(client, s) for s in target_systems]

    report_data = api.generate_report(client, system_ids=system_ids)

    if fmt == "json":
        click.echo(json.dumps(report_data, indent=2, default=str))
        return

    _print_report(report_data)


def _print_report(data: dict) -> None:
    """Print a formatted SOC 2 compliance report."""
    w = 70

    click.echo("=" * w)
    click.echo("SOC 2 Type II Compliance Report")
    click.echo(f"Generated: {data['generated_at']}")
    click.echo("=" * w)

    # Executive summary
    click.echo("\nEXECUTIVE SUMMARY")
    click.echo(f"  Systems evaluated:       {data['total_systems']}")
    click.echo(f"  Controls evaluated:      {data['controls_evaluated']}")
    click.echo(
        f"  Controls fully passing:  "
        f"{data['controls_passing']}/{data['controls_evaluated']}"
    )
    click.echo(f"  Overall compliance:      {data['overall_compliance_pct']}%")

    # Per-control sections
    for control in data["controls"]:
        click.echo("")
        click.echo("-" * w)
        click.echo(f"{control['control_id']} — {control['control_name']}")
        click.echo(f"  Check: {control['description']}")
        click.echo(
            f"  Compliance: {control['compliant_count']}/{control['total_count']} "
            f"({control['compliance_pct']}%)"
        )
        click.echo("")

        # Findings table
        click.echo(
            f"  {'System':<22} {'OS':<12} {'Result':<6} Details"
        )
        click.echo(f"  {'─' * 22} {'─' * 12} {'─' * 6} {'─' * 24}")

        remediations = []
        for f in control["findings"]:
            click.echo(
                f"  {f['display_name']:<22} {f['os']:<12} {f['result']:<6} {f['details']}"
            )
            if f.get("remediation"):
                remediations.append(f"{f['display_name']}: {f['remediation']}")

        if remediations:
            click.echo("")
            click.echo("  Remediation:")
            for r in remediations:
                click.echo(f"    - {r}")
        else:
            click.echo("")
            click.echo("  Remediation: None required.")

    click.echo("")
    click.echo("=" * w)
