---
name: mfa-audit
description: Audit MFA enrollment status across all users. Flags users without MFA for SOC 2 compliance.
command: /mfa-audit
---

# MFA Audit

Check MFA enrollment status for all JumpCloud users and flag compliance gaps.

## Steps

1. **Run the MFA audit:**
   ```bash
   make mfa-audit
   ```

2. **Review the output** — The CLI reports each user's enrollment status for TOTP, Push, WebAuthn, and JC Go, plus an overall coverage percentage.

3. **Flag issues:**
   - Users with NO MFA enrolled — SOC 2 finding
   - Users with only one MFA method — recommend backup method
   - Users still in STAGED state or not activated — can't enroll MFA until they set their password

4. **Provide recommendations:**
   - For users without MFA: "Send them instructions to enroll TOTP or push notifications"
   - For the organization: "Consider enforcing MFA requirement in JumpCloud security policies"

5. **SOC 2 note:** Auditors will ask for evidence that MFA is enforced for all users. This audit output can be used as evidence. Recommend running this monthly.
