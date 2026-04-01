---
name: lock-user
description: Immediately lock a user's JumpCloud account. Use for terminations or precautionary lockouts.
command: /lock-user
---

# Lock User

Quick action to immediately lock a user's account. For full incident response (account + devices), use `/lockdown` instead.

## Steps

1. **Identify the user** — Ask for the employee's name or username, or let the admin pick from:
   ```bash
   make list-users
   ```

2. **Show current bindings** — Display what systems the user is bound to:
   ```bash
   make user-systems USER=<username>
   ```

3. **Confirm the lock** — Ask the admin to confirm. This will immediately prevent the user from logging into any JC-managed device or service.

4. **Lock the account** — Run:
   ```bash
   make lock-user USER=<user_id>
   ```

5. **Assess next steps** — Ask the admin:
   - Is this a stolen/lost device? → Recommend `/lockdown` to also lock/wipe devices
   - Is this a termination? → Suggest running `/offboard-user` next
   - Is this a security incident? → Recommend `/lockdown` for full incident response
   - Is this temporary? → Note that `make unlock-user` can reverse this

6. **Update state file** — Update `.claude/state.md` to reflect the locked status and reason.

## Important Notes

- Locking is immediate — the user will be unable to log in on their next attempt
- This does NOT lock their Google Workspace account — remind the admin to handle that separately if needed
- This does NOT lock their devices — use `/lockdown` for that
- For full incident response (account + devices + MFA), use `/lockdown`
