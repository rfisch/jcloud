from __future__ import annotations

import click

from jcloud.api import systems as systems_api
from jcloud.api import users as api
from jcloud.client import get_client, output

USER_COLUMNS = ["_id", "username", "email", "firstname", "lastname", "account_locked", "activated"]


@click.group()
def users():
    """Manage JumpCloud users."""


@users.command("list")
@click.option("--limit", default=0, help="Max results (0 = all)")
@click.pass_context
def list_users(ctx: click.Context, limit: int):
    """List all users."""
    client = get_client(ctx)
    results = api.list_users(client)
    if limit:
        results = results[:limit]
    output(results, ctx.obj["fmt"], columns=USER_COLUMNS)


@users.command()
@click.argument("user_id")
@click.pass_context
def get(ctx: click.Context, user_id: str):
    """Get user details by ID."""
    client = get_client(ctx)
    user = api.get_user(client, user_id)
    output(user, ctx.obj["fmt"])


@users.command()
@click.option("--username", required=True)
@click.option("--email", required=True)
@click.option("--firstname", default="")
@click.option("--lastname", default="")
@click.pass_context
def create(ctx: click.Context, username: str, email: str, firstname: str, lastname: str):
    """Create a new user."""
    client = get_client(ctx)
    user = api.create_user(client, username, email, firstname, lastname)
    click.echo(f"Created user {user['_id']}")
    output(user, ctx.obj["fmt"])


@users.command()
@click.argument("user_id")
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
@click.pass_context
def delete(ctx: click.Context, user_id: str):
    """Delete a user by ID."""
    client = get_client(ctx)
    api.delete_user(client, user_id)
    click.echo(f"Deleted user {user_id}")


@users.command()
@click.argument("user_id")
@click.pass_context
def lock(ctx: click.Context, user_id: str):
    """Lock a user account."""
    client = get_client(ctx)
    api.lock_user(client, user_id)
    click.echo(f"Locked user {user_id}")


@users.command()
@click.argument("user_id")
@click.pass_context
def unlock(ctx: click.Context, user_id: str):
    """Unlock a user account."""
    client = get_client(ctx)
    api.unlock_user(client, user_id)
    click.echo(f"Unlocked user {user_id}")


@users.command("reset-mfa")
@click.argument("user_id")
@click.pass_context
def reset_mfa(ctx: click.Context, user_id: str):
    """Reset MFA for a user."""
    client = get_client(ctx)
    api.reset_mfa(client, user_id)
    click.echo(f"MFA reset for user {user_id}")


@users.command("expire-password")
@click.argument("user")
@click.pass_context
def expire_password(ctx: click.Context, user: str):
    """Force a user to change their password on next login.

    USER can be a username, email, or JumpCloud user ID.
    """
    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    user_data = api.get_user(client, user_id)
    api.expire_password(client, user_id)
    click.echo(f"Password expired for {user_data['username']} — must change on next login")


@users.command("suspend")
@click.argument("user")
@click.pass_context
def suspend(ctx: click.Context, user: str):
    """Suspend a user account.

    USER can be a username, email, or JumpCloud user ID.
    """
    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    user_data = api.get_user(client, user_id)
    api.suspend_user(client, user_id)
    click.echo(f"Suspended {user_data['username']} ({user_data['email']})")


@users.command("activate")
@click.argument("user")
@click.pass_context
def activate(ctx: click.Context, user: str):
    """Re-activate a suspended user account.

    USER can be a username, email, or JumpCloud user ID.
    """
    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    user_data = api.get_user(client, user_id)
    api.activate_user(client, user_id)
    click.echo(f"Activated {user_data['username']} ({user_data['email']})")


@users.command("set-password")
@click.argument("user")
@click.argument("password")
@click.pass_context
def set_password(ctx: click.Context, user: str, password: str):
    """Set a user's password and force-sync to bound devices.

    USER can be a username, email, or JumpCloud user ID.

    After setting the password, triggers a lightweight command on all
    bound systems to force an agent check-in so the new password takes
    effect immediately (instead of waiting for the next scheduled sync).
    """
    from jcloud.api import commands as cmd_api

    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    user_data = api.get_user(client, user_id)
    resp = client.put(f"/systemusers/{user_id}", json={"password": password})
    resp.raise_for_status()
    click.echo(f"Password set for {user_data['username']} ({user_data['email']})")

    # Force agent check-in on all bound systems
    associations = api.get_user_systems(client, user_id)
    system_ids = [a["to"]["id"] for a in associations]
    if not system_ids:
        click.echo("No bound systems — skipping agent sync.")
        return

    count = cmd_api.force_sync_systems(client, system_ids)
    click.echo(f"Triggered agent sync on {count} system(s) — password should take effect shortly.")


@users.command()
@click.argument("user")
@click.argument("system")
@click.option("--sudo", is_flag=True, default=False, help="Grant sudo/admin privileges")
@click.pass_context
def bind(ctx: click.Context, user: str, system: str, sudo: bool):
    """Bind a user to a system.

    USER can be a username, email, or JumpCloud user ID.
    SYSTEM can be a hostname, displayName, or JumpCloud system ID.

    The JumpCloud username MUST match the local account username
    to take over the existing account instead of creating a duplicate.
    """
    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    system_id = systems_api.resolve_system_id(client, system)

    # Show what we're about to do
    user_data = api.get_user(client, user_id)
    system_data = systems_api.get_system(client, system_id)
    click.echo(
        f"Binding user '{user_data['username']}' to system "
        f"'{system_data.get('displayName', system_data.get('hostname'))}'"
    )
    click.echo(f"  JC username: {user_data['username']}")
    click.echo(f"  Sudo: {'yes' if sudo else 'no'}")
    click.echo(
        f"  WARNING: Local account username must be '{user_data['username']}' "
        f"or a duplicate account will be created."
    )

    if not click.confirm("Proceed?"):
        raise SystemExit("Aborted.")

    api.bind_user_to_system(client, user_id, system_id, sudo=sudo)
    click.echo("Bound successfully.")


@users.command()
@click.argument("user")
@click.argument("system")
@click.pass_context
def unbind(ctx: click.Context, user: str, system: str):
    """Unbind a user from a system.

    USER can be a username, email, or JumpCloud user ID.
    SYSTEM can be a hostname, displayName, or JumpCloud system ID.
    """
    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    system_id = systems_api.resolve_system_id(client, system)

    user_data = api.get_user(client, user_id)
    system_data = systems_api.get_system(client, system_id)
    click.echo(
        f"Unbinding user '{user_data['username']}' from system "
        f"'{system_data.get('displayName', system_data.get('hostname'))}'"
    )

    if not click.confirm("Proceed?"):
        raise SystemExit("Aborted.")

    api.unbind_user_from_system(client, user_id, system_id)
    click.echo("Unbound successfully.")


@users.command("systems")
@click.argument("user")
@click.pass_context
def user_systems(ctx: click.Context, user: str):
    """List systems bound to a user.

    USER can be a username, email, or JumpCloud user ID.
    """
    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    associations = api.get_user_systems(client, user_id)

    if not associations:
        click.echo("No systems bound.")
        return

    # Enrich with system details
    results = []
    for assoc in associations:
        sys_id = assoc["to"]["id"]
        try:
            sys_data = systems_api.get_system(client, sys_id)
            sudo_attrs = assoc.get("attributes", {}).get("sudo", {})
            results.append(
                {
                    "system_id": sys_id,
                    "displayName": sys_data.get("displayName", ""),
                    "hostname": sys_data.get("hostname", ""),
                    "os": sys_data.get("os", ""),
                    "sudo": sudo_attrs.get("enabled", False),
                }
            )
        except Exception:
            results.append(
                {
                    "system_id": sys_id,
                    "displayName": "?",
                    "hostname": "?",
                    "os": "?",
                    "sudo": "?",
                }
            )

    output(results, ctx.obj["fmt"])


@users.command("link-google")
@click.argument("user")
@click.pass_context
def link_google(ctx: click.Context, user: str):
    """Associate a user with the Google Workspace directory for password sync.

    USER can be a username, email, or JumpCloud user ID.
    This MUST be done before the user sets their password.

    Requires JUMPCLOUD_GSUITE_DIR_ID environment variable to be set.
    """
    import os

    gsuite_dir_id = os.environ.get("JUMPCLOUD_GSUITE_DIR_ID")
    if not gsuite_dir_id:
        raise click.UsageError(
            "JUMPCLOUD_GSUITE_DIR_ID not set. Add it to your .env file."
        )

    client = get_client(ctx)
    user_id = api.resolve_user_id(client, user)
    user_data = api.get_user(client, user_id)

    resp = client.post(
        f"/gsuites/{gsuite_dir_id}/associations",
        version=2,
        json={"id": user_id, "op": "add", "type": "user"},
    )
    if resp.status_code == 204:
        click.echo(f"Linked {user_data['username']} ({user_data['email']}) to Google Workspace")
    elif resp.status_code == 409:
        click.echo(f"{user_data['username']} is already linked to Google Workspace")
    else:
        resp.raise_for_status()


MFA_COLUMNS = [
    "username",
    "email",
    "state",
    "activated",
    "totp",
    "push",
    "webauthn",
    "jc_go",
    "overall",
]


@users.command("mfa-audit")
@click.pass_context
def mfa_audit(ctx: click.Context):
    """Audit MFA enrollment status for all users."""
    client = get_client(ctx)
    results_list = api.list_users(client)

    rows = []
    enrolled = 0
    for u in results_list:
        mfa = u.get("mfaEnrollment", {})
        overall = mfa.get("overallStatus", "UNKNOWN")
        if overall == "ENROLLED":
            enrolled += 1
        rows.append(
            {
                "username": u.get("username", ""),
                "email": u.get("email", ""),
                "state": u.get("state", ""),
                "activated": u.get("activated", False),
                "totp": mfa.get("totpStatus", "UNKNOWN"),
                "push": mfa.get("pushStatus", "UNKNOWN"),
                "webauthn": mfa.get("webAuthnStatus", "UNKNOWN"),
                "jc_go": mfa.get("jcGoStatus", "UNKNOWN"),
                "overall": overall,
            }
        )

    output(rows, ctx.obj["fmt"], columns=MFA_COLUMNS)

    total = len(rows)
    click.echo(
        f"\nMFA Coverage: {enrolled}/{total} users ({100 * enrolled // total if total else 0}%)"
    )
    not_enrolled = [r["username"] for r in rows if r["overall"] != "ENROLLED"]
    if not_enrolled:
        click.echo(f"NOT ENROLLED: {', '.join(not_enrolled)}")
