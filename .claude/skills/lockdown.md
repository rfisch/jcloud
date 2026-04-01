---
name: lockdown
description: Full incident response — lock user account, lock/wipe all bound devices, reset MFA. For stolen laptops or confirmed breaches.
command: /lockdown
---

# Lockdown

Full incident response for stolen laptops, confirmed breaches, or situations requiring immediate lockout of a user AND their devices.

For account-only lockout (no device action), use `/lock-user` instead.

## Steps

1. **Identify the user** — Ask for the employee's name or username:
   ```bash
   make list-users
   ```

2. **Show current bindings** — Display all systems bound to this user:
   ```bash
   make user-systems USER=<username>
   ```

3. **Confirm the lockdown** — Clearly explain what will happen:
   > This will:
   > 1. Lock the user's JumpCloud account (no login)
   > 2. Remotely lock all bound devices
   > 3. Reset MFA enrollment
   >
   > The user will be completely locked out. Proceed?

4. **Lock the user account:**
   ```bash
   make lock-user USER=<user_id>
   ```

5. **Lock all bound devices:**
   For each bound system:
   ```bash
   make lock-system SYSTEM=<hostname>
   ```

6. **Reset MFA:**
   ```bash
   make reset-mfa USER=<user_id>
   ```

7. **Assess if device wipe is needed** — Ask the admin:
   - Is the device stolen/unrecoverable? → Remote wipe:
     ```bash
     make erase-system SYSTEM=<hostname>
     ```
     **WARNING: This is irreversible and erases all data on the device.**
   - Is the device still in the employee's possession? → Lock is sufficient for now.

8. **Remind about Google Workspace** — JumpCloud lock does NOT disable Google Workspace. The admin should also:
   - Suspend the user in Google Workspace admin console
   - Revoke all OAuth tokens / app passwords

9. **Update state file** — Log the lockdown action, reason, and affected systems in `.claude/state.md`.

## Important Notes

- Device lock and wipe require the device to be online and the JC agent running
- If the device is offline, the command will execute when it next connects
- Remote wipe (`erase-system`) is IRREVERSIBLE — confirm twice before running
- This does NOT affect Google Workspace — handle that separately
