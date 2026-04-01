---
name: force-sync
description: Force JumpCloud agent check-in on devices. Use after password resets or policy changes to apply immediately.
command: /force-sync
---

# Force Sync

Force a JumpCloud agent check-in on one or more devices to immediately apply pending changes (password resets, policy updates, binding changes).

## Steps

1. **Determine scope** — Ask the admin:
   - A specific user's devices? → Get their bound systems
   - A specific device? → Use the hostname or system ID
   - All devices? → Get all systems

2. **Find target systems:**

   For a specific user's devices:
   ```bash
   make user-systems USER=<username>
   ```

   For all systems:
   ```bash
   make list-systems
   ```

3. **Trigger the sync** — Run the "Force agent check-in" command on the target system(s):
   ```bash
   make run-command CMD=<force-sync-cmd-id> SYSTEMS=<system_id>
   ```

   If the "Force agent check-in" command doesn't exist yet, create it:
   ```bash
   jcloud commands create --name "Force agent check-in" --command "echo 'sync'" --type mac
   ```

4. **Confirm** — Let the admin know the sync was triggered and changes should take effect within a minute.

## Important Notes

- The `set-password` command already does this automatically — you only need `/force-sync` for other changes
- The agent must be running and the device must be online for the sync to work
- If the device is offline, the sync will happen when it next connects
