---
name: update-api
description: Check JumpCloud API for changes (new endpoints, models, versions) and update the project's code, skills, and documentation accordingly.
command: /update-api
---

# Update API

Check for changes to the JumpCloud API and update this project's code, CLI commands, Make targets, skills, and documentation to match.

## Steps

1. **Fetch the latest JumpCloud API spec** — Download and review the current OpenAPI specification:
   - V1: https://docs.jumpcloud.com/api/1.0/index.yaml
   - V2: https://docs.jumpcloud.com/api/2.0/index.yaml

   Also check the JumpCloud changelog and release notes for recent API changes:
   - https://jumpcloud.com/support/release-notes

2. **Compare against current implementation** — For each API module in `src/jcloud/api/`, compare the endpoints we implement against what the spec offers:

   | Module | File | Covers |
   |--------|------|--------|
   | Users | `api/users.py` | `/systemusers`, `/users/{id}/associations` |
   | Systems | `api/systems.py` | `/systems`, `/systems/{id}/command/builtin/*`, `/systems/{id}/fdekey` |
   | Commands | `api/commands.py` | `/commands`, `/runCommand`, `/commandresults` |
   | Groups | `api/groups.py` | `/usergroups`, `/systemgroups` |
   | Policies | `api/policies.py` | `/policies`, `/policies/{id}/policystatuses` |
   | RADIUS | `api/radius.py` | `/radiusservers` |
   | Apps | `api/apps.py` | `/applications` |
   | Insights | `api/insights.py` | `/systeminsights/*` |
   | Events | `api/events.py` | `/events` |
   | Auth | `api/authn.py` | `/authn/policies` |
   | IP Lists | `api/iplists.py` | `/iplists` |
   | Meta | `api/meta.py` | `/organizations`, `/policytemplates`, `/directories` |

3. **Identify gaps** — Look for:
   - New endpoints not yet implemented
   - Changed request/response schemas
   - Deprecated endpoints we still use
   - New capabilities on existing endpoints (new parameters, fields)
   - New System Insights tables
   - Version bumps or breaking changes

4. **Report findings** — Present a summary to the admin:
   - New endpoints available
   - Changes to existing endpoints
   - Deprecated features
   - Recommended updates

5. **If changes found, update the project:**

   a. **API layer** (`src/jcloud/api/`) — Add new functions or update existing ones
   b. **CLI layer** (`src/jcloud/cli/`) — Add new commands or update existing ones
   c. **Makefile** — Add new Make targets for new commands
   d. **Skills** (`.claude/skills/`) — Update workflows if new capabilities are relevant
   e. **SKILLS.md** — Update the skills reference
   f. **CLAUDE.md** — Update the quick reference
   g. **README.md** — Update if significant new features added
   h. **Setup guides** — Update MAC_SETUP.md / WINDOWS_SETUP.md if device management changes

6. **Run linter** — Verify all new code passes:
   ```bash
   make lint
   ```

7. **Test imports** — Verify everything loads:
   ```bash
   .venv/bin/python -c "from jcloud.cli.main import cli; print('OK')"
   ```

8. **Update state file** — Log the API review date and any changes made.

## What to Watch For

### High-priority changes (implement immediately)
- New device management endpoints (lock, wipe, restart)
- New user state management (suspend, reactivate)
- Security-related endpoints (auth policies, MFA changes)
- Password management changes

### Medium-priority (implement if relevant to your organization)
- New System Insights tables
- Software management endpoints
- Reporting endpoints
- Health monitoring / alerts

### Low-priority (note but skip)
- Apple MDM (we don't use it)
- Google EMM / Android (we don't use it)
- MSP / Provider endpoints
- SCIM provisioning
- Workday integration
- Password Manager endpoints

## API Spec URLs

- V1 OpenAPI: `https://docs.jumpcloud.com/api/1.0/index.yaml`
- V2 OpenAPI: `https://docs.jumpcloud.com/api/2.0/index.yaml`
- Release notes: `https://jumpcloud.com/support/release-notes`
- API docs: `https://docs.jumpcloud.com/api/`

## Important Notes

- Always test new endpoints against the live API before committing
- Check for breaking changes that could affect existing workflows
- Update the `.claude/state.md` action log after making changes
- Run `make lint` and `make format` after any code changes
