# jcloud

CLI tool for managing JumpCloud users, devices, and policies. Built for use with [Claude Code](https://claude.ai/claude-code) as an AI-assisted IT admin workflow.

## Setup

```bash
# Clone and install
git clone <repo-url>
cd jcloud
make venv

# Configure
cp .env.example .env
# Edit .env and add your JumpCloud API key
```

## Usage

```bash
# List all users
make list-users

# Set a user's password (auto-syncs to devices)
make set-password USER=jsmith PASSWORD='new password here'

# Lock a user account
make lock-user USER=<user_id>

# Lock a device remotely
make lock-system SYSTEM=<hostname>

# Get FileVault/BitLocker recovery key
make fde-key SYSTEM=<hostname>

# Check disk encryption compliance
make insight-encryption

# Review login events
make event-logins

# Full environment status
make sync-state

# See all available commands
make help
```

## CLI

The `jcloud` CLI is organized into command groups:

| Group | Description |
|-------|-------------|
| `users` | User CRUD, password, MFA, lock/unlock, suspend, bind/unbind |
| `systems` | Device management, lock/erase/restart/shutdown, FDE keys |
| `commands` | Remote command execution on devices |
| `groups` | User and system group management |
| `policies` | Device policy management |
| `insights` | System Insights queries (OS versions, encryption, installed apps) |
| `events` | Directory Insights event log (logins, security events) |
| `authn` | Authentication policies |
| `ip-lists` | IP allowlists for conditional access |
| `radius` | RADIUS server management |
| `apps` | SSO application management |

Run `jcloud <group> --help` for details on each group.

## Claude Code Workflows

This project includes guided workflows for Claude Code. See [SKILLS.md](SKILLS.md) for the full list, including:

- `/onboard-user` — Full new employee setup
- `/offboard-user` — Employee departure
- `/reset-password` — Password reset with auto device sync
- `/lockdown` — Full incident response (account + devices)
- `/security-audit` — Comprehensive compliance review
- `/device-audit` — Device compliance check
- `/mfa-audit` — MFA enrollment audit

## Requirements

- Python 3.10+
- JumpCloud API key (admin-level)
