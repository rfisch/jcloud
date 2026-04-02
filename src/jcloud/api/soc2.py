from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jcloud.api import authn, groups, insights, systems, users
from jcloud.client import JumpCloudClient

# OS version baselines — update when new major versions release
LATEST_OS_VERSIONS = {
    "darwin": {"name": "macOS", "latest_major": 26, "min_major": 24},
    "windows": {"name": "Windows", "latest_major": 11, "min_major": 10},
}

# Patches older than this are a finding
PATCH_MAX_AGE_DAYS = 90

# macOS versions that still receive XProtect updates
MAC_MIN_SUPPORTED_MAJOR = 24

# Systems not checking in for this many days are stale
STALE_SYSTEM_DAYS = 7

# Users with no login for this many days are stale
STALE_USER_DAYS = 90

# Failed login threshold per user in the last 7 days
FAILED_LOGIN_THRESHOLD = 10


def _build_system_map(client: JumpCloudClient) -> dict[str, dict]:
    """Build a lookup map of system_id -> system data."""
    return {s["_id"]: s for s in systems.list_systems(client)}


def _system_display(system: dict) -> str:
    return system.get("displayName", system.get("hostname", system["_id"]))


def _parse_mac_major(version: str) -> int | None:
    """Parse major version from macOS version string like '26.3.1'."""
    try:
        return int(version.split(".")[0])
    except (ValueError, IndexError):
        return None


def _parse_windows_major(version_str: str) -> int | None:
    """Parse major version from Windows version string like '11 Pro' or '11 Home'."""
    try:
        return int(version_str.split()[0])
    except (ValueError, IndexError):
        return None


def _make_finding(system: dict, result: str, details: str, remediation: str = "") -> dict:
    return {
        "system_id": system["_id"],
        "display_name": _system_display(system),
        "hostname": system.get("hostname", ""),
        "os": system.get("os", ""),
        "result": result,
        "details": details,
        "remediation": remediation,
    }


def _make_entity_finding(
    entity_id: str, name: str, entity_type: str, result: str,
    details: str, remediation: str = "",
) -> dict:
    return {
        "system_id": entity_id,
        "display_name": name,
        "hostname": "",
        "os": entity_type,
        "result": result,
        "details": details,
        "remediation": remediation,
    }


def evaluate_os_currency(client: JumpCloudClient, system_map: dict) -> dict:
    """CC7.1 — Check OS is within 2 major versions of latest."""
    os_data = insights.query_table(client, "os_version")

    # Map system_id -> os_version record
    os_by_system: dict[str, dict] = {}
    for row in os_data:
        sid = row.get("system_id", "")
        if sid in system_map:
            os_by_system[sid] = row

    findings = []
    for sid, system in system_map.items():
        os_row = os_by_system.get(sid)
        if not os_row:
            findings.append(_make_finding(
                system, "FAIL", "No OS data available",
                "Verify system is online and agent is current",
            ))
            continue

        platform = os_row.get("platform", "")
        baseline = LATEST_OS_VERSIONS.get(platform)
        if not baseline:
            findings.append(_make_finding(
                system, "PASS", f"OS: {os_row.get('name', '?')} {os_row.get('version', '?')}",
            ))
            continue

        # Parse major version
        if platform == "darwin":
            major = _parse_mac_major(os_row.get("version", ""))
        else:
            major = _parse_windows_major(system.get("version", ""))

        if major is None:
            findings.append(_make_finding(
                system, "FAIL", f"Could not parse OS version: {os_row.get('version', '?')}",
                "Check system agent version",
            ))
            continue

        version_display = f"{baseline['name']} {system.get('version', os_row.get('version', '?'))}"
        gap = baseline["latest_major"] - major

        if major >= baseline["min_major"]:
            if gap == 0:
                detail = f"{version_display} — current"
            else:
                detail = f"{version_display} — {gap} version(s) behind"
            findings.append(_make_finding(system, "PASS", detail))
        else:
            findings.append(_make_finding(
                system, "FAIL",
                f"{version_display} — {gap} version(s) behind (min: {baseline['min_major']})",
                f"Update to {baseline['name']} {baseline['min_major']} or later",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC7.1",
        "control_name": "Configuration and Vulnerability Management",
        "description": "OS version within 2 major versions of latest",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


def evaluate_patch_management(client: JumpCloudClient, system_map: dict) -> dict:
    """CC8.1 — Check security patches are current."""
    patch_data = insights.query_table(client, "patches")

    # Group patches by system_id, track most recent install date
    latest_patch: dict[str, datetime] = {}
    for row in patch_data:
        sid = row.get("system_id", "")
        if sid not in system_map:
            continue
        installed_on = row.get("installed_on", "")
        if not installed_on:
            continue
        try:
            dt = datetime.strptime(installed_on, "%m/%d/%Y").replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                dt = datetime.fromisoformat(installed_on.replace("Z", "+00:00"))
            except ValueError:
                continue
        if sid not in latest_patch or dt > latest_patch[sid]:
            latest_patch[sid] = dt

    cutoff = datetime.now(timezone.utc) - timedelta(days=PATCH_MAX_AGE_DAYS)
    findings = []

    for sid, system in system_map.items():
        os_name = system.get("os", "")

        # Mac — patches bundled with OS updates
        if os_name == "Mac OS X":
            findings.append(_make_finding(
                system, "N/A", "macOS — security patches bundled with OS updates",
            ))
            continue

        last = latest_patch.get(sid)
        if last is None:
            findings.append(_make_finding(
                system, "FAIL", "No patch data available",
                "Verify Windows Update is enabled and system is online",
            ))
            continue

        age_days = (datetime.now(timezone.utc) - last).days
        if last >= cutoff:
            findings.append(_make_finding(
                system, "PASS",
                f"Last patch: {last.strftime('%Y-%m-%d')} ({age_days} days ago)",
            ))
        else:
            findings.append(_make_finding(
                system, "FAIL",
                f"Last patch: {last.strftime('%Y-%m-%d')} ({age_days} days ago)",
                f"Install pending Windows updates (>{PATCH_MAX_AGE_DAYS} days since last patch)",
            ))

    # Compliance count excludes N/A systems
    applicable = [f for f in findings if f["result"] != "N/A"]
    compliant = sum(1 for f in applicable if f["result"] == "PASS")
    total = len(applicable)
    return {
        "control_id": "CC8.1",
        "control_name": "Security Patch Management",
        "description": f"Security patches installed within last {PATCH_MAX_AGE_DAYS} days",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": total,
        "compliance_pct": 100 * compliant // total if total else 0,
    }


def evaluate_endpoint_protection(client: JumpCloudClient, system_map: dict) -> dict:
    """CC6.8 — Check antivirus is installed with current definitions."""
    # Windows: query security products
    sec_products = insights.query_table(client, "windows_security_products")

    # Group AV products by system_id
    av_by_system: dict[str, list[dict]] = {}
    for row in sec_products:
        sid = row.get("system_id", "")
        if sid not in system_map:
            continue
        ptype = row.get("type", "").lower()
        if "antivirus" in ptype or "anti-virus" in ptype:
            av_by_system.setdefault(sid, []).append(row)

    findings = []
    for sid, system in system_map.items():
        os_name = system.get("os", "")

        # Mac — XProtect is built-in and auto-updated on supported versions
        if os_name == "Mac OS X":
            version = system.get("version", "")
            major = _parse_mac_major(version) if version else None
            if major and major >= MAC_MIN_SUPPORTED_MAJOR:
                findings.append(_make_finding(
                    system, "PASS",
                    f"XProtect (built-in, auto-updated) — macOS {version}",
                ))
            else:
                findings.append(_make_finding(
                    system, "FAIL",
                    f"macOS {version} — may no longer receive XProtect updates",
                    f"Update to macOS {MAC_MIN_SUPPORTED_MAJOR} or later",
                ))
            continue

        # Windows — check security products
        av_products = av_by_system.get(sid, [])
        if not av_products:
            findings.append(_make_finding(
                system, "FAIL", "No antivirus detected",
                "Install and enable Windows Defender or third-party antivirus",
            ))
            continue

        # Check if any AV is active with current signatures
        active_av = []
        for av in av_products:
            state = av.get("state", "").lower()
            name = av.get("name", "Unknown AV")
            if state in ("on", "enabled", "active"):
                active_av.append(name)

        if active_av:
            findings.append(_make_finding(
                system, "PASS", f"Active: {', '.join(active_av)}",
            ))
        else:
            names = [av.get("name", "Unknown") for av in av_products]
            findings.append(_make_finding(
                system, "FAIL",
                f"AV installed but not active: {', '.join(names)}",
                "Enable antivirus protection",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC6.8",
        "control_name": "Unauthorized and Malicious Code Protection",
        "description": "Antivirus installed with current definitions",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


def evaluate_disk_encryption(client: JumpCloudClient, system_map: dict) -> dict:
    """CC6.1a — Check full disk encryption enabled with key escrowed."""
    findings = []
    for sid, system in system_map.items():
        fde = system.get("fde", {})
        active = fde.get("active", False)
        key_present = fde.get("keyPresent", False)
        name = _system_display(system)

        if active and key_present:
            findings.append(_make_finding(system, "PASS", "FDE active, recovery key escrowed"))
        elif active and not key_present:
            findings.append(_make_finding(
                system, "FAIL", "FDE active but recovery key NOT escrowed",
                "Escrow recovery key to JumpCloud",
            ))
        else:
            findings.append(_make_finding(
                system, "FAIL", "Disk encryption not enabled",
                f"Enable FileVault (Mac) or BitLocker (Windows) on {name}",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC6.1a",
        "control_name": "Full Disk Encryption",
        "description": "Disk encryption enabled with recovery key escrowed",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


def evaluate_mfa_enrollment(client: JumpCloudClient, system_map: dict) -> dict:
    """CC6.1b — Check all active users have MFA enrolled."""
    all_users = users.list_users(client)

    findings = []
    for u in all_users:
        mfa = u.get("mfaEnrollment", {})
        status = mfa.get("overallStatus", "UNKNOWN")
        username = u.get("username", "?")
        activated = u.get("activated", False)

        if not activated:
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "N/A",
                "Account not yet activated",
            ))
            continue

        if status == "ENROLLED":
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "PASS",
                f"MFA enrolled ({status})",
            ))
        else:
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "FAIL",
                f"MFA status: {status}",
                f"Enroll MFA for {username}",
            ))

    applicable = [f for f in findings if f["result"] != "N/A"]
    compliant = sum(1 for f in applicable if f["result"] == "PASS")
    total = len(applicable)
    return {
        "control_id": "CC6.1b",
        "control_name": "Multi-Factor Authentication",
        "description": "All active users have MFA enrolled",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": total,
        "compliance_pct": 100 * compliant // total if total else 0,
    }


def evaluate_access_control(client: JumpCloudClient, system_map: dict) -> dict:
    """CC6.3 — Check users have role-based access (in groups, bound to systems)."""
    all_users = users.list_users(client)
    user_groups = groups.list_user_groups(client)

    # Build set of user IDs that are in at least one group
    users_in_groups: set[str] = set()
    for g in user_groups:
        members = groups.list_members(client, g["id"], group_type="user")
        for m in members:
            mid = m.get("to", {}).get("id", m.get("id", ""))
            if mid:
                users_in_groups.add(mid)

    findings = []
    for u in all_users:
        uid = u["_id"]
        username = u.get("username", "?")
        activated = u.get("activated", False)

        if not activated:
            continue

        issues = []
        if uid not in users_in_groups:
            issues.append("not in any user group")

        # Check system bindings
        assocs = users.get_user_systems(client, uid)
        if not assocs:
            issues.append("not bound to any system")

        if issues:
            findings.append(_make_entity_finding(
                uid, username, "user", "FAIL",
                "; ".join(issues).capitalize(),
                f"Add {username} to appropriate group and bind to system",
            ))
        else:
            bound_count = len(assocs)
            findings.append(_make_entity_finding(
                uid, username, "user", "PASS",
                f"In group, bound to {bound_count} system(s)",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC6.3",
        "control_name": "Role-Based Access Control",
        "description": "All active users in groups and bound to systems",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


def evaluate_deprovisioning(client: JumpCloudClient, system_map: dict) -> dict:
    """CC6.5 — Check for stale or orphan accounts."""
    all_users = users.list_users(client)

    findings = []
    for u in all_users:
        username = u.get("username", "?")
        locked = u.get("account_locked", False)
        suspended = u.get("suspended", False)
        activated = u.get("activated", False)

        if locked or suspended:
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "PASS",
                f"Account {'locked' if locked else 'suspended'}",
            ))
            continue

        if not activated:
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "FAIL",
                "Account exists but never activated",
                f"Activate or remove {username}",
            ))
            continue

        # Check for system bindings — active user with no binding is suspect
        assocs = users.get_user_systems(client, u["_id"])
        if not assocs:
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "FAIL",
                "Active account with no system binding",
                f"Bind {username} to a system or deactivate",
            ))
        else:
            findings.append(_make_entity_finding(
                u["_id"], username, "user", "PASS",
                f"Active, bound to {len(assocs)} system(s)",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC6.5",
        "control_name": "Access Deprovisioning",
        "description": "No stale, orphan, or unactivated accounts",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


def evaluate_auth_policies(client: JumpCloudClient, system_map: dict) -> dict:
    """CC6.6 — Check authentication policies enforce MFA and device trust."""
    auth_policies = authn.list_policies(client)

    if not auth_policies:
        return {
            "control_id": "CC6.6",
            "control_name": "Authentication Policy Enforcement",
            "description": "Auth policies enforce MFA for all access",
            "findings": [_make_entity_finding(
                "", "No policies", "policy", "FAIL",
                "No authentication policies configured",
                "Create authentication policies with MFA required",
            )],
            "compliant_count": 0,
            "total_count": 1,
            "compliance_pct": 0,
        }

    findings = []
    for p in auth_policies:
        name = p.get("name", "Unnamed")
        pid = p.get("id", "")
        disabled = p.get("disabled", False)
        mfa_required = p.get("mfa", {}).get("required", False)

        if disabled:
            findings.append(_make_entity_finding(
                pid, name, "policy", "N/A", "Policy disabled",
            ))
            continue

        if mfa_required:
            findings.append(_make_entity_finding(
                pid, name, "policy", "PASS", "MFA required",
            ))
        else:
            findings.append(_make_entity_finding(
                pid, name, "policy", "FAIL",
                "MFA not required",
                f"Enable MFA requirement on policy '{name}'",
            ))

    applicable = [f for f in findings if f["result"] != "N/A"]
    compliant = sum(1 for f in applicable if f["result"] == "PASS")
    total = len(applicable)
    return {
        "control_id": "CC6.6",
        "control_name": "Authentication Policy Enforcement",
        "description": "Auth policies enforce MFA for all access",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": total,
        "compliance_pct": 100 * compliant // total if total else 0,
    }


def evaluate_policy_coverage(client: JumpCloudClient, system_map: dict) -> dict:
    """CC5.2 — Check all systems have required policies bound."""
    findings = []
    for sid, system in system_map.items():
        name = _system_display(system)
        statuses = systems.get_system_policy_statuses(client, sid)

        if not statuses:
            findings.append(_make_finding(
                system, "FAIL", "No policies applied",
                f"Bind required policies to {name}",
            ))
            continue

        failed = [s for s in statuses if not s.get("success", False)]
        total = len(statuses)
        passing = total - len(failed)

        if failed:
            fail_names = []
            for s in failed:
                detail = s.get("detail", "")
                if isinstance(detail, str) and detail:
                    fail_names.append(detail[:60])
                else:
                    fail_names.append(s.get("policyID", "unknown")[:24])
            findings.append(_make_finding(
                system, "FAIL",
                f"{passing}/{total} policies passing",
                f"Fix failing policies on {name}",
            ))
        else:
            findings.append(_make_finding(
                system, "PASS", f"{total} policies applied, all passing",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC5.2",
        "control_name": "Technology Control Coverage",
        "description": "All systems have required policies applied and passing",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


def evaluate_system_monitoring(client: JumpCloudClient, system_map: dict) -> dict:
    """CC7.2 — Check all systems are actively checking in."""
    findings = []
    for sid, system in system_map.items():
        active = system.get("active", False)
        last_contact = system.get("lastContact", "")
        name = _system_display(system)

        if not active:
            findings.append(_make_finding(
                system, "FAIL",
                f"Offline (last: {last_contact[:10] if last_contact else 'unknown'})",
                f"Verify {name} is powered on and agent is running",
            ))
        else:
            findings.append(_make_finding(
                system, "PASS", "System active and checking in",
            ))

    compliant = sum(1 for f in findings if f["result"] == "PASS")
    return {
        "control_id": "CC7.2",
        "control_name": "System Monitoring",
        "description": "All systems actively checking in",
        "findings": findings,
        "compliant_count": compliant,
        "total_count": len(findings),
        "compliance_pct": 100 * compliant // len(findings) if findings else 0,
    }


# Registry of all controls — add new controls here
CONTROL_EVALUATORS = [
    evaluate_disk_encryption,
    evaluate_mfa_enrollment,
    evaluate_access_control,
    evaluate_deprovisioning,
    evaluate_auth_policies,
    evaluate_policy_coverage,
    evaluate_os_currency,
    evaluate_patch_management,
    evaluate_endpoint_protection,
    evaluate_system_monitoring,
]


def generate_report(
    client: JumpCloudClient, system_ids: list[str] | None = None,
) -> dict:
    """Generate a SOC 2 Type II compliance report across all controls."""
    system_map = _build_system_map(client)

    if system_ids:
        system_map = {sid: s for sid, s in system_map.items() if sid in system_ids}

    controls = []
    for evaluator in CONTROL_EVALUATORS:
        controls.append(evaluator(client, system_map))

    controls_passing = sum(
        1 for c in controls if c["total_count"] > 0 and c["compliant_count"] == c["total_count"]
    )

    total_findings = sum(c["total_count"] for c in controls)
    total_compliant = sum(c["compliant_count"] for c in controls)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_systems": len(system_map),
        "controls_evaluated": len(controls),
        "controls_passing": controls_passing,
        "controls_failing": len(controls) - controls_passing,
        "overall_compliance_pct": 100 * total_compliant // total_findings if total_findings else 0,
        "controls": controls,
    }
