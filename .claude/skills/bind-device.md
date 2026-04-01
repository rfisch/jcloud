---
name: bind-device
description: Bind a JumpCloud user to a device after agent installation.
command: /bind-device
---

# Bind Device

Bind an existing JumpCloud user to a device that already has the JC agent installed.

## Steps

1. **List available systems** — Show unbound systems:
   ```bash
   make list-systems
   ```

2. **List available users** — Show users and their current bindings:
   ```bash
   make list-users
   ```

3. **Ask the admin** — Which user and which system to bind. Accept username, email, or ID for the user; hostname or ID for the system.

4. **Verify username match** — Remind the admin:
   - The JC username MUST match the local account username exactly
   - For Windows fresh machines: JC creates the account on first login, so the username it creates will match the JC username
   - For existing machines: the local username must already match
   - If they don't match, JC will create a duplicate account

5. **Bind** — Execute:
   ```bash
   make bind-user USER=<username> SYSTEM=<hostname>
   ```

6. **Verify** — Confirm the binding:
   ```bash
   make user-systems USER=<username>
   make system-users SYSTEM=<system_id>
   ```

7. **Update state file** — Update `.claude/state.md` with the new binding.

8. **Next steps** — Tell the admin:
   - Employee can now log out and log in with their JC username and password
   - Verify device policies are applying (BitLocker/FileVault, screen lock, etc.)
