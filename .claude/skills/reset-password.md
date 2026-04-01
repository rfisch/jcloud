---
name: reset-password
description: Reset or set a user's JumpCloud password, unlock their account, or reset MFA. Auto-syncs to devices.
command: /reset-password
---

# Reset Password

Help an employee who is locked out, forgot their password, or needs a password change.

## Steps

1. **Identify the user** — Ask for the employee's name or username:
   ```bash
   make list-users
   ```

2. **Determine the issue:**
   - Forgot password → set a new one
   - Account locked → unlock first, then set password
   - MFA issues → reset MFA

3. **If account is locked, unlock first:**
   ```bash
   make unlock-user USER=<user_id>
   ```

4. **Set a new password:**
   ```bash
   make set-password USER=<username> PASSWORD='<new_password>'
   ```
   This automatically forces an agent check-in on all bound devices so the password takes effect immediately — no waiting for the next scheduled sync.

   Quote the password if it contains spaces.

5. **If MFA needs reset:**
   ```bash
   make reset-mfa USER=<user_id>
   ```

6. **Verify** — After the employee confirms they're back in:
   - Can they log into their device?
   - Can they access Google Workspace?

7. Update the state file action log.

## Important Notes

- Password sync exports from JC to Google Workspace — setting the password here will push it to Google
- The `set-password` command automatically triggers an agent sync on bound devices — the password should take effect within a minute
- If the agent sync doesn't work, you can manually force it: `make run-command CMD=<force-sync-cmd-id> SYSTEMS=<system_id>`
- Passwords with spaces must be quoted: `PASSWORD='my passphrase here'`
