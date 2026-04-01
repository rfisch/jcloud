---
name: recover-device
description: Retrieve FileVault/BitLocker recovery key for a locked-out device.
command: /recover-device
---

# Recover Device

Retrieve the FileVault or BitLocker recovery key for a device when a user is locked out at the disk encryption level.

## Steps

1. **Identify the device** — Ask which employee or device is affected:
   ```bash
   make list-systems
   ```

   Or find the system by user:
   ```bash
   make user-systems USER=<username>
   ```

2. **Retrieve the recovery key:**
   ```bash
   make fde-key SYSTEM=<hostname>
   ```

3. **Provide the key to the user** — Walk them through entering the recovery key:
   - **Mac (FileVault):** At the login screen, click the `?` icon or enter the wrong password 3 times to reveal the recovery key entry option
   - **Windows (BitLocker):** The recovery key screen appears automatically when BitLocker can't unlock the drive. Enter the 48-digit recovery key.

4. **After recovery** — Recommend the user set a new password:
   ```bash
   make set-password USER=<username> PASSWORD='<new_password>'
   ```

5. **Update state file** — Log the recovery event.

## Important Notes

- The FDE key must have been escrowed to JumpCloud for this to work (check `fde.keyPresent` in system details)
- If the key is not escrowed, you cannot recover the device through JumpCloud
- Windows 11 Home may not support full BitLocker / key escrow
- After using a recovery key, the user should change their password to re-enable normal unlock
