---
name: login-history
description: Review login events from Directory Insights. For security reviews and incident investigation.
command: /login-history
---

# Login History

Review login events from JumpCloud Directory Insights to investigate suspicious activity or audit login patterns.

## Steps

1. **Determine scope** — Ask the admin:
   - A specific user? → Filter by their email or username
   - A time range? → Default to last 7 days
   - All logins? → No filter

2. **Pull login events:**
   ```bash
   make event-logins START=<start-date-iso> END=<end-date-iso>
   ```

   For broader event search:
   ```bash
   make list-events SERVICE=sso START=<start-date-iso>
   ```

   For all event types:
   ```bash
   make list-events SERVICE=all START=<start-date-iso>
   ```

3. **Analyze the results:**
   - Total login count
   - Failed vs successful logins
   - Logins per user
   - Any unusual patterns (off-hours, unusual frequency)

4. **Flag concerns:**
   - Multiple failed login attempts for the same user → possible brute force
   - Logins at unusual times → possible compromised credentials
   - Users who haven't logged in at all → may need access review

5. **Take action if needed:**
   - Suspicious activity → `/lock-user` or `/lockdown`
   - Too many failed attempts → check if account is locked, reset password
   - Unused accounts → consider suspension

## Important Notes

- Directory Insights events are available for a limited retention period
- Use ISO 8601 format for dates (e.g., `2026-03-20T00:00:00Z`)
- Event count can help identify trends: `make event-count SERVICE=sso`
