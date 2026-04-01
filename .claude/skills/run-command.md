---
name: run-command
description: Execute a JumpCloud command on one or more managed machines.
command: /run-command
---

# Run Command

Execute a JumpCloud command on target systems. Use for pulling logs, running scripts, or remote diagnostics.

## Steps

1. **List available commands** — Show what's configured:
   ```bash
   make list-commands
   ```

2. **Ask the admin** — What do they want to run, and on which system(s)?
   - Pick an existing command, or describe what they need
   - If the needed command doesn't exist, note that it must be created in the JumpCloud admin console first

3. **Identify target systems:**
   ```bash
   make list-systems
   ```

4. **Confirm execution** — Show the admin:
   - Command name and what it does
   - Target system(s)
   - Ask for confirmation before running

5. **Execute the command:**
   ```bash
   make run-command CMD=<command_id> SYSTEMS=<system_id>
   ```

6. **Check results** — Command results are available in the JumpCloud admin console under the command's results tab. Let the admin know where to find the output.

## Important Notes

- Commands run with root/admin privileges on the target machine
- Results may take a few minutes to appear depending on agent check-in frequency
- For immediate results, the machine's agent must be online and checking in
- Currently configured commands can be viewed with `make list-commands`
