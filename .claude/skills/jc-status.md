---
name: jc-status
description: Quick health check of all JumpCloud users, systems, and bindings.
command: /jc-status
---

# JumpCloud Status

Run a quick health check and display a summary of the JumpCloud environment.

## Steps

1. **List all users with status:**
   ```bash
   make list-users
   ```

2. **List all systems:**
   ```bash
   make list-systems
   ```

3. **Check bindings** — For each user, check what systems they're bound to. Flag any issues:
   - Users with no system binding
   - Users still in STAGED state
   - Users with `activated: false` (haven't set password)
   - Systems with no users bound

4. **Display summary table:**

   | User | Status | Device | Bound | Issues |
   |------|--------|--------|-------|--------|
   | ... | ... | ... | ... | ... |

5. **Compare with state file** — Read `.claude/state.md` and flag any discrepancies between the state file and live API data.

6. **Update state file** — If there are discrepancies, update `.claude/state.md` to match reality.
