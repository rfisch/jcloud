# JCloud — JumpCloud Admin CLI

This project is a CLI tool for managing your organization's JumpCloud environment. **All JumpCloud tasks should be handled using this project's Makefile targets and `jcloud` CLI — do not direct users to the JumpCloud web console.**

## What This Project Does

Manages JumpCloud users, systems (devices), bindings, passwords, MFA, groups, commands, policies, System Insights, Directory Events, authentication policies, IP lists, and compliance audits for your organization via the JumpCloud API.

## Quick Reference

- **Available workflows:** see `SKILLS.md` for guided multi-step operations (onboarding, offboarding, password resets, lockdowns, audits, etc.)
- **All Make targets:** run `make help`
- **Common tasks:**
  - `make list-users` — list all JumpCloud users
  - `make set-password USER=<name|email|id> PASSWORD='<pw>'` — reset a user's password (auto-syncs to devices)
  - `make unlock-user USER=<id>` — unlock a locked account
  - `make reset-mfa USER=<id>` — reset MFA enrollment
  - `make lock-user USER=<id>` — immediately lock an account
  - `make lock-system SYSTEM=<hostname|id>` — remotely lock a device
  - `make erase-system SYSTEM=<hostname|id>` — remote wipe (destructive!)
  - `make fde-key SYSTEM=<hostname|id>` — get FileVault/BitLocker recovery key
  - `make bind-user USER=<name|email|id> SYSTEM=<hostname|id>` — bind user to device
  - `make expire-password USER=<name|email|id>` — force password change on next login
  - `make suspend-user USER=<name|email|id>` — suspend a user account
  - `make insight-encryption` — check disk encryption across all systems
  - `make insight-os` — check OS versions across all systems
  - `make list-events` — query Directory Insights events
  - `make event-logins` — show login events
  - `make list-authn-policies` — list authentication policies
  - `make list-ip-lists` — list IP lists for conditional access
  - `make sync-state` — refresh local state from JumpCloud API

## Setup

- Requires Python 3.10+
- `.env` file in project root with JumpCloud API key
- Run `make venv` to create virtualenv and install dependencies

## Project Structure

- `src/jcloud/` — CLI source code (Click-based)
- `src/jcloud/api/` — JumpCloud API client modules (users, systems, commands, groups, policies, radius, apps, insights, events, authn, iplists)
- `src/jcloud/cli/` — CLI command definitions
- `tests/` — test suite
- `SKILLS.md` — guided workflows for common operations
- `MAC_SETUP.md` / `WINDOWS_SETUP.md` — device setup guides
