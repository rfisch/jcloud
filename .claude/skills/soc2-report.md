---
name: soc2-report
description: Generate a SOC 2 Type II compliance report evaluating managed systems against security controls.
command: /soc2-report
---

# SOC 2 Type II Compliance Report

Evaluate all managed systems against SOC 2 controls and produce a consolidated findings report.

## Controls Evaluated

| Control | SOC 2 ID | What It Checks |
|---------|----------|---------------|
| OS Version Currency | CC7.1 | OS within 2 major versions of latest |
| Security Patch Management | CC8.1 | Security patches installed within 90 days |
| Antivirus/Endpoint Protection | CC6.8 | AV installed and active with current definitions |

## Steps

1. **Run the compliance report:**
   ```bash
   make soc2-report
   ```
   This evaluates every managed system against all SOC 2 controls and produces a formatted report with PASS/FAIL per system, compliance percentages, and remediation recommendations.

2. **Review findings** — For each control section:
   - Check per-system results
   - Note any FAIL findings and their remediation steps
   - N/A results (e.g., Mac systems for patch management) are expected

3. **For audit evidence (JSON output):**
   ```bash
   jcloud --format json soc2 report > soc2-report-$(date +%Y-%m-%d).json
   ```

4. **Target a specific system:**
   ```bash
   make soc2-report SYSTEM=<hostname>
   ```

5. **Remediate failures** using existing Make targets:
   - OS outdated: guide user to update
   - Missing patches: guide user to run Windows Update
   - No antivirus: guide user to enable Windows Defender

6. **Re-run report** after remediation to verify compliance.

## Report Structure

- **Executive Summary** — Systems evaluated, controls passing, overall compliance %
- **Per-Control Sections** — Control ID, description, per-system findings table, remediation steps
- **Compliance Percentages** — Per-control and overall

## Platform Notes

- **macOS:** Patch management shows N/A (patches bundled with OS updates). Antivirus checks XProtect (built-in, auto-updated on supported versions).
- **Windows:** Patch management checks Windows Update history. Antivirus checks Windows Security Center for active AV products.

## Adding New Controls

New controls can be added to `src/jcloud/api/soc2.py` by writing an evaluator function and adding it to the `CONTROL_EVALUATORS` list. No CLI or Makefile changes needed.

## Complementary Skills

- `/security-audit` — broader security review (MFA, encryption, login events, accounts)
- `/device-audit` — device compliance (encryption, OS, agent status)
- `/mfa-audit` — MFA enrollment check
- `/access-review` — quarterly SOC 2 access review with sign-off
