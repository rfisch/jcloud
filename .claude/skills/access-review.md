---
name: access-review
description: Quarterly access review for SOC 2. Shows who has access to what and asks for confirmation of each.
command: /access-review
---

# Access Review

Perform a formal access review for SOC 2 compliance. Walk through every user and their access, requiring explicit admin confirmation for each.

## Steps

1. **Announce the review** — Inform the admin:
   > Starting quarterly access review. For SOC 2, you need to confirm that each user's access is still appropriate. I'll walk through each user one at a time.

2. **Pull all data:**
   ```bash
   make list-users
   make list-systems
   ```
   Also gather all user-system bindings and group memberships.

3. **For each user, present and ask:**

   Display:
   - Name, email, role/title (if available)
   - Account status (active, locked, staged)
   - MFA enrolled?
   - Systems they're bound to
   - Groups they're in
   - Last login date (if available)

   Then ask:
   > **[User Name]** has access to [system(s)]. Is this access still appropriate?
   > - Yes, keep as-is
   > - Modify (change access level or system bindings)
   > - Revoke (offboard or remove access)

4. **Handle modifications** — If the admin wants to change access:
   - Unbind from systems: `make unbind-user USER=<username> SYSTEM=<hostname>`
   - Bind to new systems: `make bind-user USER=<username> SYSTEM=<hostname>`
   - Lock account: `make lock-user USER=<user_id>`

5. **Flag concerns:**
   - Users who haven't logged in for 30+ days
   - Users without MFA
   - Users with access to systems they may no longer need
   - Staged or inactive accounts

6. **Generate review record** — Save the results:
   - Date of review
   - Reviewer (admin name)
   - Each user reviewed with the decision (keep/modify/revoke)
   - Any actions taken

   Save to `reviews/access-review-YYYY-MM-DD.md`

7. **Update state file** — Reflect any changes in `.claude/state.md`.

## Important Notes

- SOC 2 Type II requires regular access reviews (typically quarterly)
- The review record serves as audit evidence — keep all review files
- This should cover JumpCloud access only — Google Workspace and SaaS app access reviews are separate
- Recommend scheduling this as a recurring task every quarter
