---
name: onboard-user
description: Onboard a new employee — create JumpCloud account, link to Google Workspace, send activation email, and prepare for device binding.
command: /onboard-user
---

# Onboard User

Walk the admin through onboarding a new employee to JumpCloud and their device.

## Steps

1. **Gather information** — Ask for:
   - Full name
   - Google Workspace email (@yourcompany.com)
   - Device type (Windows or Mac)
   - If Mac: is this a fresh machine or existing with a local account?

2. **Determine JC username** — Follow the naming convention: first name, lowercase (e.g., `jsmith`). Confirm with the admin.

3. **Check if user already exists** — Run:
   ```bash
   make list-users
   ```
   If the user exists, show their status and skip to step 5.

4. **Create the user** — Run:
   ```bash
   make create-user USERNAME=<username> EMAIL=<email> FIRSTNAME=<first> LASTNAME=<last>
   ```

5. **Associate with Google Workspace directory** — This MUST happen BEFORE the user sets their password, otherwise password export to Google will not work:
   ```bash
   make link-google USER=<user_id>
   ```

6. **Send activation email** — Inform the admin to send the employee these instructions:
   > You'll receive an email from JumpCloud with the subject "Set up your JumpCloud account."
   > 1. Open the email and click "Set Up Account"
   > 2. When it asks you to create a password, **set your new password** — this will become your Google Workspace password too
   > 3. That's it — you're done

7. **Device setup** — Based on device type, reference the appropriate guide:
   - **Windows fresh machine:** Follow WINDOWS_SETUP.md Section 1
   - **Windows BYOD:** Follow WINDOWS_SETUP.md Section 2
   - **Mac BYOD:** Follow MAC_SETUP.md

   Remind the admin:
   - The JC username must match the local account username exactly
   - For Windows fresh machines: employee uses personal Microsoft account for OOBE, JC creates the employee's account on first login after binding
   - For existing machines: get the employee's `whoami` output first

8. **Bind user to device** — Once the JC agent is installed and the system appears:
   ```bash
   make list-systems
   make bind-user USER=<username> SYSTEM=<hostname>
   ```
   This grants admin privileges and sets the user as primary user on the system.

9. **Verify** — Confirm the binding:
   ```bash
   make user-systems USER=<username>
   ```

10. **Update state file** — Update `.claude/state.md` with the new user's details, system binding, and completed status.

## Important Notes

- Google Workspace is the IdP, not JumpCloud
- Password sync is EXPORT: JC password pushes to Google Workspace
- The Google Workspace association MUST be in place before the user sets their password
- All users get admin on their machines
- Connect Key: `$JUMPCLOUD_CONNECT_KEY`
