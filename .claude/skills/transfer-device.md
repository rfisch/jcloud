---
name: transfer-device
description: Transfer a device from one user to another — unbind the current user and bind the new one.
command: /transfer-device
---

# Transfer Device

Reassign a device from one employee to another. Handles unbinding, rebinding, and username considerations.

## Steps

1. **Identify the device:**
   ```bash
   make list-systems
   ```

2. **Show current binding** — Who is currently bound to this device:
   ```bash
   make system-users SYSTEM=<system_id>
   ```

3. **Identify the new user:**
   ```bash
   make list-users
   ```

4. **Check username compatibility** — The new user's JC username must match (or will become) the local account username on the device.
   - If the device had user A's account and is being reassigned to user B, the admin needs to decide:
     - Wipe the machine and start fresh? (cleanest)
     - Create a new local account for user B alongside user A's old account?
     - Rename the local account? (risky)

5. **Confirm the plan** with the admin.

6. **Unbind the current user:**
   ```bash
   make unbind-user USER=<current_username> SYSTEM=<hostname>
   ```

7. **Bind the new user:**
   ```bash
   make bind-user USER=<new_username> SYSTEM=<hostname>
   ```

8. **Verify:**
   ```bash
   make system-users SYSTEM=<system_id>
   make user-systems USER=<new_username>
   ```

9. **On-device steps** — Remind the admin:
   - If the machine was wiped: follow WINDOWS_SETUP.md or MAC_SETUP.md from the beginning
   - If a new local account was created: the new user logs in with their JC credentials
   - The old user's local account/data may still be on the machine — decide whether to delete it

10. **Update state file** — Reflect the new assignment in `.claude/state.md`.
