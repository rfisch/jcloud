---
name: offboard-user
description: Offboard an employee — unbind from device, document clean exit steps.
command: /offboard-user
---

# Offboard User

Walk the admin through removing an employee from JumpCloud management while preserving their machine.

## Steps

1. **Identify the user** — Ask for the employee's name or username, or let the admin pick from:
   ```bash
   make list-users
   ```

2. **Show current bindings** — Display what systems the user is bound to:
   ```bash
   make user-systems USER=<username>
   ```

3. **Confirm offboarding** — Ask the admin to confirm they want to unbind this user from their device(s).

4. **Unbind from system(s)** — For each bound system:
   ```bash
   make unbind-user USER=<username> SYSTEM=<hostname>
   ```

5. **Provide on-device instructions** — Based on device type:

   **Windows:**
   - Log in as `uadmin`
   - Uninstall JC agent: `msiexec /x "{A0E756D4-E3BB-4F68-8F0F-26B1B89E1AE7}" /qn`
   - Promote employee's account back to Administrator
   - Remove `uadmin` account
   - Employee sets their own local password

   **Mac:**
   - Log in as `uadmin`
   - Uninstall JC agent: `sudo /opt/jc/bin/jumpcloud-agent uninstall`
   - Remove `uadmin` account
   - Employee manages their own password

6. **Handle JumpCloud account** — Ask the admin:
   - Delete the JC user account? (if leaving the company)
   - Or just leave unbound? (if keeping for other purposes)

   If deleting:
   ```bash
   make delete-user USER=<user_id>
   ```

7. **Update state file** — Update `.claude/state.md` to reflect the offboarding.

## Important Notes

- The goal is a clean exit — the employee keeps a fully functional machine
- Google Workspace account is managed separately — remind admin to handle that too
- `uadmin` password is in your password manager if the admin needs to access the machine
