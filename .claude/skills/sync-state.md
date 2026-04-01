---
name: sync-state
description: Sync the local state file with live JumpCloud data. Run this to refresh the cache.
command: /sync-state
---

# Sync State

Pull live data from JumpCloud and update `.claude/state.md` to match.

## Steps

1. **Pull all live data:**
   ```bash
   make sync-state
   ```

2. **Review the output** — The CLI pulls all users, systems, groups, integrations, commands, and policies from JumpCloud.

3. **Update `.claude/state.md`** — Replace all sections with the live data. Preserve the Configuration Decisions and Action Log sections — those are manual.

4. **Append to the Action Log** — Add an entry:
   ```
   | YYYY-MM-DD | State synced with live JumpCloud data |
   ```

## Important Notes

- Run this at the start of every session to ensure the state file is current
- Run after any changes made directly in the JumpCloud admin console (not through CLI)
- The Configuration Decisions section is manually maintained — do not overwrite it
- The Action Log is append-only — never remove entries
