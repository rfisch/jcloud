---
name: export-inventory
description: Export all JumpCloud users, systems, bindings, and policies to a spreadsheet for auditors or insurance.
command: /export-inventory
---

# Export Inventory

Generate a comprehensive inventory report of all JumpCloud-managed users, devices, and configurations.

## Steps

1. **Pull all data:**
   ```bash
   make list-users
   make list-systems
   make list-groups
   make list-policies
   make list-commands
   ```

2. **For each user, gather:**
   - Name, email, username, JC ID
   - Account state and activation status
   - MFA enrollment status
   - System bindings
   - Group memberships
   - Creation date

3. **For each system, gather:**
   - Hostname, display name, OS, version
   - Agent version and last contact
   - Bound user(s)
   - Device group membership
   - Encryption status

4. **Generate the export** — Create a spreadsheet or CSV with tabs/sections:
   - **Users** — all user details and statuses
   - **Systems** — all device details and compliance
   - **Bindings** — user-to-system mapping
   - **Groups** — group memberships
   - **Policies** — applied policies

5. **Save the export** to the project directory with a dated filename:
   - `exports/inventory-YYYY-MM-DD.csv` (or .xlsx if the xlsx skill is available)

6. **Summary** — Display a quick summary:
   - Total users (active vs staged)
   - Total systems (by OS)
   - Unbound users or systems
   - MFA coverage percentage

## Important Notes

- This report can be provided directly to SOC 2 auditors as evidence of asset management
- Recommend running quarterly or before each audit review
- For insurance purposes, this documents all managed hardware assets
