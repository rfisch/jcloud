---
name: harden-ssh
description: Disable SSH root login on a managed machine. Can be run locally or remotely via JumpCloud command.
command: /harden-ssh
---

# Harden SSH

Disable SSH root login on a managed machine for SOC 2 compliance.

## Steps

1. **Identify the target machine** — Ask which system to harden:
   ```bash
   make list-systems
   ```

2. **Determine access method:**
   - **Local (you're on the machine):** Run the command directly
   - **Remote (via JumpCloud command):** Push the command through JC

3. **For Mac:**

   Local:
   ```bash
   sudo sed -i '' 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
   ```

   Remote via JumpCloud: use `make run-command CMD=<ssh-harden-mac-id> SYSTEMS=<system_id>`

4. **For Windows:**

   SSH root login is not a concern on Windows — SSH server is typically not installed. If it is, the equivalent is disabling the built-in Administrator account for SSH access.

5. **Verify** — After running, confirm the change:

   Mac:
   ```bash
   grep "PermitRootLogin" /etc/ssh/sshd_config
   ```
   Should show: `PermitRootLogin no`

6. **No restart required** — macOS applies the change on the next SSH connection attempt without restarting sshd.

## Important Notes

- This should be done on every Mac during onboarding
- SOC 2 auditors flag SSH root login as a finding
- JumpCloud reports `sshRootEnabled` in system details — but the API cannot change it, it must be done via sshd_config
- Consider creating a JumpCloud command to push this to all Macs at once
