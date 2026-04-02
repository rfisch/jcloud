# JCloud Skills Reference

Skills are conversational workflows you can run inside Claude Code from this project directory. They guide you through multi-step JumpCloud operations using the Make targets and CLI built into this project.

Type the command (e.g., `/onboard-user`) in the Claude Code prompt to start a skill.

---

## Onboarding & Offboarding

### `/onboard-user`
Full new employee flow: create JC account → link Google Workspace → send activation email → walk through device setup → bind user → add to groups → verify.

**Use when:** A new employee needs a JumpCloud account and device setup.

**Sample prompts:**
- `/onboard-user`
- "I need to onboard a new employee, jane@example.com, she's getting a new Windows laptop"
- "New employee starting Monday, Windows machine"
- "Set up a new Mac user for a new hire"

### `/offboard-user`
Remove JumpCloud management from an employee's device while keeping the machine functional. Unbind → uninstall instructions → optional account deletion.

**Use when:** An employee is leaving the company.

**Sample prompts:**
- `/offboard-user`
- "An employee is leaving, remove them from JumpCloud"
- "Offboard jsmith and make sure his machine stays functional"
- "An employee quit today, I need to remove their access immediately"

---

## Device Management

### `/bind-device`
Bind an existing JumpCloud user to a device that already has the JC agent installed. Verifies username match before binding.

**Use when:** JC agent is installed and you just need to link a user to a machine.

**Sample prompts:**
- `/bind-device`
- "Bind jsmith to his new Windows machine"
- "The agent is installed on DESKTOP-ABC123, bind jdoe to it"
- "I just installed the JC agent, now I need to bind the user"

### `/transfer-device`
Reassign a device from one user to another. Unbinds the current user, binds the new one, handles username and local account considerations.

**Use when:** An employee gets a new machine or a device is being reassigned.

**Sample prompts:**
- `/transfer-device`
- "Move jsmith's laptop to jdoe"
- "Reassign DESKTOP-ABC123 from one user to another"
- "An employee left and we're giving their machine to a new hire"

### `/run-command`
Execute a JumpCloud command on one or more managed machines. For pulling logs, running scripts, or remote diagnostics.

**Use when:** You need to run something on a remote machine.

**Sample prompts:**
- `/run-command`
- "Pull the agent logs from jsmith's machine"
- "Run the 'Get agent logs' command on all Windows devices"
- "I need to run a diagnostic on DESKTOP-DEF456"

### `/force-sync`
Force a JumpCloud agent check-in on one or more systems. Triggers the agent to pull latest state (passwords, policies, bindings) immediately instead of waiting for the next scheduled sync.

**Use when:** You've made changes in JumpCloud (password reset, policy change) and need them to take effect on a device immediately.

**Sample prompts:**
- `/force-sync`
- "Force sync jsmith's machine"
- "Push the latest changes to all devices"
- "The password change isn't taking effect — force a sync"

---

## Policy Management

### `/manage-policies`
View, bind, and audit JumpCloud configuration policies across systems and groups. Bind policies to individual systems or system groups, check which systems a policy applies to, and review compliance status.

**Use when:** You need to apply a policy to systems/groups, check which systems have a policy, or audit policy compliance.

**Sample prompts:**
- `/manage-policies`
- "Bind the BitLocker policy to all Windows machines"
- "Which systems have the disk encryption policy applied?"
- "Show me compliance status for the BitLocker policy"
- "Apply the firewall policy to the Windows Devices group"
- "Remove the screen lock policy from a system"
- "Audit policy compliance across all systems"

---

## Security & Incidents

### `/lock-user`
Immediately lock a user's account. Shows affected systems and recommends next steps (remote wipe, offboarding, Google Workspace).

**Use when:** Quick account disable — termination, suspicious activity, or precautionary lockout.

**Sample prompts:**
- `/lock-user`
- "Lock jsmith's account immediately"
- "We just terminated an employee, lock them out now"
- "Security incident — disable this user's access right away"

### `/lockdown`
Full incident response: lock user account → lock all bound devices → reset MFA → show affected systems and apps. Use for confirmed security incidents like stolen laptops or breaches.

**Use when:** Stolen laptop, confirmed breach, or any situation requiring immediate full lockout of a user AND their devices.

**Sample prompts:**
- `/lockdown`
- "An employee's laptop was stolen — lock everything down"
- "Security breach — full lockdown on jsmith's account and devices"
- "Terminate all access for this user immediately, device and account"

### `/reset-password`
Walk through password reset for a locked-out user. Unlocks account if locked, sets new password, forces agent sync on bound devices so the password takes effect immediately, and verifies.

**Use when:** An employee can't log in.

**Sample prompts:**
- `/reset-password`
- "jdoe is locked out of her machine"
- "jsmith forgot his password and can't log in"
- "A user's account got locked after too many failed attempts"
- "An employee doesn't remember their password"

### `/recover-device`
Retrieve the FileVault/BitLocker recovery key for a locked-out device. For when a user is locked out of their machine at the disk encryption level.

**Use when:** A user can't get past FileVault or BitLocker on their machine.

**Sample prompts:**
- `/recover-device`
- "An employee is locked out of their Mac at the FileVault screen"
- "I need the BitLocker recovery key for DESKTOP-ABC123"
- "Employee forgot their disk encryption password"

### `/harden-ssh`
Disable SSH root login on a Mac. Can be run locally or pushed remotely via JumpCloud command. SOC 2 requirement.

**Use when:** Setting up a new Mac or hardening existing machines.

**Sample prompts:**
- `/harden-ssh`
- "Disable SSH root login on all Macs"
- "Harden SSH on jsmith's machine"
- "Lock down SSH root access"

---

## Compliance & Auditing

### `/soc2-report`
Generate a SOC 2 Type II compliance report. Evaluates all managed systems against SOC 2 controls (OS currency CC7.1, patch management CC8.1, endpoint protection CC6.8) and produces a consolidated findings report with per-system PASS/FAIL results, compliance percentages, and remediation recommendations.

**Use when:** Preparing for SOC 2 audit, monthly compliance checks, or generating evidence for auditors.

**Sample prompts:**
- `/soc2-report`
- "Run the SOC 2 compliance report"
- "Check all systems against SOC 2 controls"
- "Generate a SOC 2 report for the auditor"
- "Run SOC 2 compliance check on a specific machine"

### `/jc-status`
Quick health check: all users, systems, bindings. Flags issues like unbound users, staged accounts, missing devices. Compares live data against the state file.

**Use when:** You want a quick overview of your JumpCloud environment.

**Sample prompts:**
- `/jc-status`
- "Show me the current state of JumpCloud"
- "Are all users set up correctly?"
- "Quick health check on all devices and users"

### `/mfa-audit`
Check MFA enrollment across all users. Flags anyone without MFA enrolled — a SOC 2 finding.

**Use when:** Preparing for an audit or monthly compliance check.

**Sample prompts:**
- `/mfa-audit`
- "Who doesn't have MFA set up?"
- "Run an MFA compliance check for all users"
- "I need to verify everyone has two-factor enabled before the audit"

### `/device-audit`
Check all managed devices for compliance: encryption, OS version, agent status, last check-in. Uses System Insights data for disk encryption and OS version details. Flags non-compliant devices.

**Use when:** Preparing for an audit or monthly compliance check.

**Sample prompts:**
- `/device-audit`
- "Are all devices compliant?"
- "Check if BitLocker and FileVault are enabled everywhere"
- "Which machines haven't checked in recently?"
- "Run a device compliance check before the audit"

### `/security-audit`
Comprehensive security review combining multiple checks: MFA enrollment, device compliance, login event review (via Directory Insights), locked/suspended account review, unbound user check, and FDE key verification.

**Use when:** Comprehensive security review or SOC 2 preparation.

**Sample prompts:**
- `/security-audit`
- "Run a full security audit"
- "Prepare the security review for SOC 2"
- "I need a comprehensive security check before the auditor comes"

### `/access-review`
Formal quarterly access review for SOC 2. Walks through every user and their access, requires explicit confirmation for each. Generates a review record as audit evidence.

**Use when:** Quarterly SOC 2 access review.

**Sample prompts:**
- `/access-review`
- "Time for the quarterly access review"
- "I need to do an access review for SOC 2"
- "Walk me through who has access to what so I can confirm everything"

### `/export-inventory`
Export all users, systems, bindings, and policies to a spreadsheet. For auditors, insurance, or asset tracking.

**Use when:** You need a full inventory report.

**Sample prompts:**
- `/export-inventory`
- "Export everything for the auditor"
- "I need an inventory report for our insurance renewal"
- "Generate a spreadsheet of all users and devices"
- "Dump the full JumpCloud inventory to a CSV"

---

## System Insights & Events

### `/check-encryption`
Check disk encryption status (FileVault/BitLocker) across all managed systems. Uses System Insights for detailed status.

**Use when:** Verifying encryption compliance.

**Sample prompts:**
- `/check-encryption`
- "Is FileVault enabled on all Macs?"
- "Check BitLocker status across Windows devices"
- "Which devices don't have disk encryption?"

### `/check-os-versions`
Show OS versions across all managed systems. Flags outdated or mismatched versions.

**Use when:** Checking OS compliance or planning updates.

**Sample prompts:**
- `/check-os-versions`
- "What OS versions are all devices running?"
- "Are any machines running outdated macOS?"
- "Show me the OS breakdown across the fleet"

### `/check-installed-apps`
List installed applications across managed systems. Can filter by specific system.

**Use when:** Software inventory or license auditing.

**Sample prompts:**
- `/check-installed-apps`
- "What software is installed on jsmith's machine?"
- "Show me all installed apps across the fleet"
- "Is Zoom installed on all devices?"

### `/login-history`
Review login events from Directory Insights. Shows who logged in, when, and whether it succeeded. Useful for security reviews and incident investigation.

**Use when:** Investigating suspicious activity or reviewing login patterns.

**Sample prompts:**
- `/login-history`
- "Show me all login events from the past week"
- "Who logged in today?"
- "Were there any failed login attempts recently?"
- "Show me jsmith's login history"

---

## Maintenance

### `/update-api`
Check the JumpCloud API for changes (new endpoints, deprecated features, version bumps) and update the project's code, CLI commands, Make targets, skills, and documentation accordingly.

**Use when:** Periodically checking for API changes, after a JumpCloud release, or when a feature seems missing.

**Sample prompts:**
- `/update-api`
- "Check if JumpCloud has added any new API endpoints"
- "Are we missing any JumpCloud API capabilities?"
- "Update the project to match the latest JumpCloud API"

---

## State Management

### `/sync-state`
Pull live data from JumpCloud and update the local state file to match. Run at the start of every session or after changes made in the admin console.

**Use when:** Starting a new session, or after making changes directly in the JumpCloud admin console.

**Sample prompts:**
- `/sync-state`
- "Refresh the state file"
- "Sync state with JumpCloud"
- "Update the local cache"

---

## Prerequisites

All skills assume:
- You are in the `jcloud` project directory
- The `.env` file is in place with your JumpCloud API key
- The virtualenv is set up (`make venv`)

## State File

Skills read and update `.claude/state.md` to track users, systems, bindings, and configuration decisions. This prevents repeating work across sessions.

## Setup Documents

Skills reference these guides for detailed step-by-step instructions:
- `WINDOWS_SETUP.md` — Windows fresh machine and BYOD setup
- `MAC_SETUP.md` — Mac BYOD setup (existing local account)
