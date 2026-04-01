---
name: security-audit
description: Comprehensive security review — MFA, encryption, login events, account status, and device compliance.
command: /security-audit
---

# Security Audit

Comprehensive security review combining multiple checks. Run before SOC 2 audits or as a monthly security review.

## Steps

1. **MFA Enrollment Check:**
   ```bash
   make mfa-audit
   ```
   Flag any users without MFA enrolled.

2. **Disk Encryption Check:**
   ```bash
   make insight-encryption
   ```
   Verify FileVault (Mac) and BitLocker (Windows) are active on all devices.

3. **OS Version Check:**
   ```bash
   make insight-os
   ```
   Flag any devices running outdated OS versions.

4. **Account Status Review:**
   ```bash
   make list-users
   ```
   Flag:
   - Locked accounts that should be unlocked (or vice versa)
   - Staged accounts that haven't been activated
   - Users not bound to any system

5. **Login Event Review:**
   ```bash
   make event-logins --START=<7-days-ago-iso>
   ```
   Look for:
   - Failed login attempts (brute force indicators)
   - Logins from unexpected locations or times
   - Users who haven't logged in recently

6. **FDE Key Escrow Verification:**
   ```bash
   make sync-state
   ```
   Check the state file — every device should have `Key Escrowed: Yes`.

7. **Device Compliance:**
   ```bash
   make list-systems
   ```
   Check:
   - All devices actively checking in
   - No unknown or unauthorized devices
   - All devices have the JC agent running

8. **Authentication Policies:**
   ```bash
   make list-authn-policies
   ```
   Verify MFA requirements and conditional access rules are in place.

9. **Generate Report** — Summarize findings:
   - Total users / systems
   - MFA coverage percentage
   - Encryption coverage
   - Any flagged issues
   - Recommended actions

10. **Update state file** — Log the audit date and findings.

## Important Notes

- This audit covers JumpCloud-managed resources only
- Google Workspace access review is separate
- For formal SOC 2 access review with sign-off, use `/access-review`
- Schedule this monthly or before auditor visits
