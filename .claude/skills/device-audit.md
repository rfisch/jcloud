---
name: device-audit
description: Audit all managed devices for compliance — encryption, OS version, agent status, last check-in.
command: /device-audit
---

# Device Audit

Check all JumpCloud-managed devices for policy compliance and flag issues.

## Steps

1. **Pull all systems** — Get full system details:
   ```bash
   make list-systems
   ```

2. **For each system, check and report:**
   - OS type and version (is it up to date?)
   - Agent version (is it current?)
   - Last contact time (has it checked in recently?)
   - Disk encryption status (BitLocker on Windows, FileVault on Mac)
   - Bound user(s)
   - Device group membership

3. **Display summary table:**

   | Device | OS | Version | Encryption | Last Check-in | Bound User | Issues |
   |--------|-----|---------|------------|---------------|------------|--------|
   | ... | ... | ... | ... | ... | ... | ... |

4. **Flag issues:**
   - Devices that haven't checked in for 7+ days — may be offline or agent removed
   - Devices without disk encryption — SOC 2 finding
   - Devices with outdated OS — security risk
   - Devices with no bound users — orphaned
   - Devices not in appropriate device group (Mac Devices, Windows Devices)

5. **Provide recommendations:**
   - For stale devices: "Investigate if the device is still in use"
   - For unencrypted devices: "Enable BitLocker/FileVault policy in JumpCloud"
   - For outdated OS: "Push OS update policy or notify the user"

6. **SOC 2 note:** Auditors want evidence of endpoint compliance. This audit output serves as evidence. Recommend running monthly or before audit reviews.
