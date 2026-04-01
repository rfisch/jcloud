# Windows Machine Setup Guide

## Phase 0: Employee Password Setup

Before setting up the machine, the employee must set their JumpCloud password. Send them these instructions:

> You'll receive an email from JumpCloud with the subject "Set up your JumpCloud account."
>
> 1. Open the email and click **"Set Up Account"**
> 2. When it asks you to create a password, **use the same password as your Google Workspace (@yourcompany.com) account**
> 3. That's it — you're done

If they haven't received the email, have them check spam. The email comes from `no-reply@jumpcloud.com`.

---

## Section 1: Fresh Machine Setup

### Prerequisites

- Fresh Windows machine (out of box)
- Employee has completed Phase 0 above
- JumpCloud Connect Key: `$JUMPCLOUD_CONNECT_KEY`

### User Assignments

Track Windows users and their JumpCloud IDs in `.claude/state.md`.

---

### Phase 1: Windows OOBE

We create a temporary local account to get past setup. JumpCloud will create the real work account later.

1. Power on the machine
2. Select region and keyboard layout
3. When it asks to connect to Wi-Fi, press **Shift + F10** to open a Command Prompt
4. Type `OOBE\BYPASSNRO` and press Enter — the machine will reboot
5. After reboot, go through region/keyboard again
6. On the network screen, click **"I don't have internet"**, then **"Continue with limited setup"**
7. Create a temporary local account (e.g., name: `setup`, no password)
8. Decline everything (privacy settings, etc.)
9. Once at the desktop, connect to Wi-Fi

### Phase 2: Install JumpCloud Agent

Send the employee these instructions:

> 1. Open your browser and go to: **https://cdn02.jumpcloud.com/production/versions/2.101.1/jcagent-msi-signed.msi**
> 2. A file will download — double-click `jcagent-msi-signed.msi` to install it
> 3. When it asks for the Connect Key, enter: **$JUMPCLOUD_CONNECT_KEY**
> 4. Wait for the installer to finish (2-3 minutes)
> 5. Go to **Settings > System > About** and tell me your **Device name**

Once they provide the device name, verify from your Mac:
```bash
make list-systems
```

### Phase 3: Bind User to Machine

From your Mac (in the `jcloud` project directory):

```bash
make bind-user USER=<username> SYSTEM=<device-name>
```

Example:
```bash
make bind-user USER=jsmith SYSTEM=DESKTOP-ABC123
```

All users are bound with admin privileges by default.

### Phase 4: Employee First Login

Send the employee these instructions:

> 1. Sign out of your current Windows account (Start > click your name > Sign out)
> 2. On the login screen, click **"Other user"**
> 3. Log in with your JumpCloud username and password:
>    - Username: your JumpCloud username (typically first name, lowercase)
>    - Password: the password you set in your JumpCloud activation email
> 4. Windows will set up your new profile — this takes a minute
> 5. You're done — use this account going forward

### Phase 5: Verify

```bash
make list-systems
make user-systems USER=<username>
```

---

## Section 2: Existing Machine (BYOD) Setup

For Windows machines where the employee already has a local account and you need to add JumpCloud management.

### Prerequisites

- Employee has completed Phase 0 above
- Admin access to the machine

### Phase 1: Get Device Name and Local Username

Ask the employee to go to **Settings > System > About** and tell you:
- **Device name** (e.g., DESKTOP-ABC123)
- **Account name** they're logged in as (visible at **Settings > Accounts > Your info**)

The JumpCloud username must match their local account name. If they don't match, update the JC username to match the local account.

### Phase 2: Install JumpCloud Agent

Send the employee the same instructions as Section 1, Phase 2.

### Phase 3: Bind User to Machine

From your Mac:

```bash
make bind-user USER=<username> SYSTEM=<device-name>
```

JumpCloud will take over the existing local account since the usernames match. No duplicate account is created.

### Phase 4: Verify

```bash
make list-systems
make user-systems USER=<username>
```

Employee logs out and back in with their JC password to confirm.

---

## Clean Exit Plan

If the company shuts down and employees keep their machines:

```bash
make unbind-user USER=<username> SYSTEM=<device-name>
```

Then tell the employee:
- Open **Settings > Apps > Installed apps**
- Find **JumpCloud** and uninstall it
- Their Windows account and files remain intact

## Notes

- Employee's Microsoft account used during OOBE remains on the machine but is unused
- All JC user accounts have admin privileges on their machines
- JumpCloud password syncs to Google Workspace — one password for everything
- JumpCloud creates the employee's local account on first login (fresh machines)
- JumpCloud takes over the existing local account when usernames match (BYOD machines)
