# Mac Setup Guide

## Phase 0: Employee Password Setup

Before setting up the machine, the employee must set their JumpCloud password. Send them these instructions:

> You'll receive an email from JumpCloud with the subject "Set up your JumpCloud account."
>
> 1. Open the email and click **"Set Up Account"**
> 2. When it asks you to create a password, **use the same password as your Google Workspace (@yourcompany.com) account**
> 3. That's it — you're done

If they haven't received the email, have them check spam. The email comes from `no-reply@jumpcloud.com`.

---

Step-by-step instructions for setting up a Mac with JumpCloud agent, binding to an EXISTING local user account without creating a duplicate.

## Prerequisites

- Mac with an existing local user account already set up
- Employee has completed Phase 0 above
- You know the employee's local macOS username (MUST match JumpCloud username exactly)
- JumpCloud Connect Key: `$JUMPCLOUD_CONNECT_KEY`

## Current Mac Users

Track Mac users and their JumpCloud IDs in `.claude/state.md`.

---

## CRITICAL: Avoiding the Duplicate Account Problem

JumpCloud will create a NEW local macOS account if the usernames don't match. To take over an existing account:

1. The **JumpCloud username** must EXACTLY match the **local macOS username**
2. The binding must be configured to take over the existing account, not create a new one

**Check the local macOS username before doing anything:**

```bash
# On the Mac, run:
whoami
# or
dscl . -list /Users | grep -v '^_'
```

If the local username is `jdoe` but the JC username is `jane`, JC will create a second account called `jane`. Make sure they match.

---

## Phase 1: Verify Local macOS Username

1. On the employee's Mac, open **Terminal**
2. Run: `whoami`
3. Note the exact username — this is what the JumpCloud username MUST be set to
4. If the JC username doesn't match, update it in JumpCloud BEFORE installing the agent. Always match JC to local, not the other way around.

## Phase 2: Create Local Admin Account (if not already present)

Your management/support account. Unique password stored in your password manager.

1. Open **System Settings > Users & Groups**
2. Click **Add User...**
3. Set up the account:
   - Full Name: `IT Admin` (or your preferred name)
   - Account Name: `uadmin`
   - Password: unique for this machine, store in your password manager immediately
4. Change the account type to **Administrator**
5. Verify: the employee's account should be **Standard** (not Admin)
   - If the employee is currently an Admin, change them to Standard after creating the admin account
   - Make sure you're logged into the admin account or have admin credentials before downgrading the employee

## Phase 3: Install JumpCloud Agent

**Option A: GUI Installer (recommended)**

1. Open a browser and download the agent:
   - **Download URL:** [https://cdn02.jumpcloud.com/production/jumpcloud-agent.pkg](https://cdn02.jumpcloud.com/production/jumpcloud-agent.pkg)
2. Double-click `jumpcloud-agent.pkg` to run the installer
3. Follow the prompts — click Continue, Agree to terms, Install
4. Enter the admin password when prompted
5. When asked for the Connect Key, paste: `$JUMPCLOUD_CONNECT_KEY`
6. Click Continue to complete installation

**Option B: Command Line**

```bash
curl --tlsv1.2 --silent --show-error --header 'x-connect-key: $JUMPCLOUD_CONNECT_KEY' "https://kickstart.jumpcloud.com/Kickstart" | sudo bash
```

**Verify the agent is running:**

```bash
sudo launchctl list | grep jumpcloud
```

Should show the `com.jumpcloud.darwin-agent` service.

The machine should now appear in JumpCloud admin console under **Devices**

## Phase 4: Bind User to Machine (Takeover Existing Account)

Once the agent is installed and the machine appears in JumpCloud, bind the user from your Mac Studio (in the `jcloud` project directory). The username match ensures JC takes over the existing account.

```bash
# Find the new system
make list-systems

# Bind the user to the system
make bind-user USER=<username> SYSTEM=<hostname>
```

**CRITICAL:** After binding, verify in JumpCloud admin console that it shows "Account takeover" or the existing account was linked — NOT that a new account was created.

## Phase 5: Verify

```bash
make list-systems
make user-systems USER=<username>
```

Also verify on the machine:
1. Have the employee **log out and log back in** with their JumpCloud password
2. Verify only ONE user account exists for the employee:
   ```bash
   dscl . -list /Users | grep -v '^_'
   ```
3. Confirm device policies are applying:
   - FileVault should be enabled: `fdesetup status`
   - Check screen lock settings in System Settings

## Phase 6: Harden SSH

Disable SSH root login for SOC 2 compliance. Run on the machine:

```bash
sudo sed -i '' 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
```

Verify:
```bash
grep "PermitRootLogin" /etc/ssh/sshd_config
```

Should show: `PermitRootLogin no`

Or use the skill: `/harden-ssh`

## Phase 7: Grant macOS Permissions

After agent install, macOS may prompt for permissions. Approve these in **System Settings > Privacy & Security**:

- **Full Disk Access** — required for FileVault reporting and compliance
- **Accessibility** — may be needed for certain policies
- **Notifications** — for JumpCloud agent alerts

These may require the admin account to approve.

---

## Troubleshooting: Duplicate Account Was Created

If JumpCloud created a new account instead of taking over the existing one:

1. Unbind the user: `make unbind-user USER=<username> SYSTEM=<hostname>`
2. **Delete the duplicate account** in System Settings > Users & Groups
3. **Verify the JC username matches the local username exactly** (case-sensitive)
4. **Re-bind the user:** `make bind-user USER=<username> SYSTEM=<hostname>`

If the employee's data ended up in the wrong account, you'll need to migrate their home folder contents manually.

---

## Clean Exit Plan

If the company shuts down and employees keep their Macs:

1. Unbind the user: `make unbind-user USER=<username> SYSTEM=<hostname>`
2. Uninstall the JumpCloud agent:
   ```bash
   sudo /opt/jc/bin/jumpcloud-agent uninstall
   ```
   If that doesn't work:
   ```bash
   sudo launchctl unload /Library/LaunchDaemons/com.jumpcloud.darwin-agent.plist
   sudo rm -rf /opt/jc
   sudo rm /Library/LaunchDaemons/com.jumpcloud.darwin-agent.plist
   ```
3. The employee's local macOS account remains intact and functional
4. Remove the `uadmin` account if no longer needed
5. The employee can manage their own password going forward

## Notes

- The #1 cause of duplicate accounts is username mismatch — always verify with `whoami` first
- Employee accounts should be **Standard** (not Admin) for SOC 2 least-privilege compliance
- Admin account passwords are unique per machine and stored in your password manager
- JumpCloud password syncs to Google Workspace — one password for everything
- Always get the employee's local macOS username BEFORE creating their JC account
