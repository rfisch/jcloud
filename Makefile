.PHONY: help venv install lint format test sync-state \
       list-users get-user create-user delete-user lock-user unlock-user reset-mfa \
       set-password link-google expire-password suspend-user activate-user \
       list-groups group-members add-group-member remove-group-member \
       list-systems get-system system-users bind-user unbind-user user-systems mfa-audit \
       lock-system erase-system restart-system shutdown-system fde-key system-policy-status force-sync \
       list-commands get-command run-command \
       list-policies get-policy policy-results \
       bind-policy-system unbind-policy-system bind-policy-group unbind-policy-group \
       policy-systems policy-groups policy-compliance \
       list-radius get-radius \
       list-apps get-app \
       insight-tables insight-query insight-os insight-encryption insight-apps \
       list-events event-logins event-count \
       list-authn-policies get-authn-policy create-authn-policy update-authn-policy \
       list-ip-lists get-ip-list create-ip-list

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
JCLOUD := $(VENV)/bin/jcloud

sync-state: ## Pull all JumpCloud data and print state summary
	$(JCLOUD) sync-state

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────────────

venv: ## Create virtualenv and install project
	python3 -m venv $(VENV)
	$(PIP) install -e ".[dev]"

install: ## Install project into current env
	pip install -e ".[dev]"

# ── Development ──────────────────────────────────────────────────────

lint: ## Run linter
	$(VENV)/bin/ruff check src/ tests/
	$(VENV)/bin/ruff format --check src/ tests/

format: ## Auto-format code
	$(VENV)/bin/ruff format src/ tests/
	$(VENV)/bin/ruff check --fix src/ tests/

test: ## Run tests
	$(VENV)/bin/pytest tests/ -v

# ── Users ────────────────────────────────────────────────────────────

list-users: ## List all users
	$(JCLOUD) users list

get-user: ## Get user details (USER=<id>)
	$(JCLOUD) users get $(USER)

create-user: ## Create user (USERNAME=x EMAIL=x FIRSTNAME=x LASTNAME=x)
	$(JCLOUD) users create --username $(USERNAME) --email $(EMAIL) \
		$(if $(FIRSTNAME),--firstname $(FIRSTNAME)) \
		$(if $(LASTNAME),--lastname $(LASTNAME))

delete-user: ## Delete user (USER=<id>)
	$(JCLOUD) users delete $(USER) --yes

lock-user: ## Lock user account (USER=<id>)
	$(JCLOUD) users lock $(USER)

unlock-user: ## Unlock user account (USER=<id>)
	$(JCLOUD) users unlock $(USER)

reset-mfa: ## Reset MFA for user (USER=<id>)
	$(JCLOUD) users reset-mfa $(USER)

# ── Groups ───────────────────────────────────────────────────────────

list-groups: ## List groups (TYPE=user|system, default: user)
	$(JCLOUD) groups list $(if $(TYPE),--type $(TYPE))

group-members: ## List group members (GROUP=<id> TYPE=user|system)
	$(JCLOUD) groups members $(GROUP) $(if $(TYPE),--type $(TYPE))

add-group-member: ## Add member to group (GROUP=<id> MEMBER=<id> TYPE=user|system)
	$(JCLOUD) groups add-member $(GROUP) $(MEMBER) $(if $(TYPE),--type $(TYPE))

remove-group-member: ## Remove member from group (GROUP=<id> MEMBER=<id> TYPE=user|system)
	$(JCLOUD) groups remove-member $(GROUP) $(MEMBER) $(if $(TYPE),--type $(TYPE))

# ── Systems ──────────────────────────────────────────────────────────

list-systems: ## List all systems
	$(JCLOUD) systems list

get-system: ## Get system details (SYSTEM=<id>)
	$(JCLOUD) systems get $(SYSTEM)

system-users: ## List users bound to a system (SYSTEM=<id>)
	$(JCLOUD) systems users $(SYSTEM)

bind-user: ## Bind user to system (USER=<name|email|id> SYSTEM=<hostname|id>) — admin by default
	$(JCLOUD) users bind $(USER) $(SYSTEM) --sudo

unbind-user: ## Unbind user from system (USER=<name|email|id> SYSTEM=<hostname|id>)
	$(JCLOUD) users unbind $(USER) $(SYSTEM)

user-systems: ## List systems bound to a user (USER=<id>)
	$(JCLOUD) users systems $(USER)

set-password: ## Set user password (USER=<name|email|id> PASSWORD=<password>)
	$(JCLOUD) users set-password $(USER) '$(PASSWORD)'

link-google: ## Associate user with Google Workspace for password sync (USER=<name|email|id>)
	$(JCLOUD) users link-google $(USER)

expire-password: ## Force password change on next login (USER=<name|email|id>)
	$(JCLOUD) users expire-password $(USER)

suspend-user: ## Suspend user account (USER=<name|email|id>)
	$(JCLOUD) users suspend $(USER)

activate-user: ## Re-activate suspended user (USER=<name|email|id>)
	$(JCLOUD) users activate $(USER)

mfa-audit: ## Audit MFA enrollment for all users
	$(JCLOUD) users mfa-audit

lock-system: ## Lock system remotely (SYSTEM=<hostname|id> PIN=<optional>)
	$(JCLOUD) systems lock $(SYSTEM) $(if $(PIN),--pin $(PIN)) --yes

erase-system: ## Remote wipe system — DESTRUCTIVE (SYSTEM=<hostname|id>)
	$(JCLOUD) systems erase $(SYSTEM) --yes

restart-system: ## Restart system remotely (SYSTEM=<hostname|id>)
	$(JCLOUD) systems restart $(SYSTEM)

shutdown-system: ## Shut down system remotely (SYSTEM=<hostname|id>)
	$(JCLOUD) systems shutdown $(SYSTEM)

fde-key: ## Get FileVault/BitLocker recovery key (SYSTEM=<hostname|id>)
	$(JCLOUD) systems fde-key $(SYSTEM)

system-policy-status: ## Show policy compliance for a system (SYSTEM=<hostname|id>)
	$(JCLOUD) systems policy-status $(SYSTEM)

force-sync: ## Force agent check-in (SYSTEM=<hostname|id> or ALL=yes for all systems)
	$(JCLOUD) systems force-sync $(if $(filter yes,$(ALL)),--all,$(SYSTEM))

# ── Commands ─────────────────────────────────────────────────────────

list-commands: ## List all commands
	$(JCLOUD) commands list

get-command: ## Get command details (CMD=<id>)
	$(JCLOUD) commands get $(CMD)

run-command: ## Trigger a command (CMD=<id> SYSTEMS=<id,id,...>)
	$(JCLOUD) commands run $(CMD) $(if $(SYSTEMS),--system-ids $(SYSTEMS))

# ── Policies ─────────────────────────────────────────────────────────

list-policies: ## List all policies
	$(JCLOUD) policies list

get-policy: ## Get policy details (POLICY=<name|id>)
	$(JCLOUD) policies get $(POLICY)

policy-results: ## Show policy status results (POLICY=<name|id>)
	$(JCLOUD) policies results $(POLICY)

bind-policy-system: ## Bind policy to system (POLICY=<name|id> SYSTEM=<hostname|id>)
	$(JCLOUD) policies bind-system $(POLICY) $(SYSTEM)

unbind-policy-system: ## Unbind policy from system (POLICY=<name|id> SYSTEM=<hostname|id>)
	$(JCLOUD) policies unbind-system $(POLICY) $(SYSTEM)

bind-policy-group: ## Bind policy to system group (POLICY=<name|id> GROUP=<name|id>)
	$(JCLOUD) policies bind-group $(POLICY) $(GROUP)

unbind-policy-group: ## Unbind policy from system group (POLICY=<name|id> GROUP=<name|id>)
	$(JCLOUD) policies unbind-group $(POLICY) $(GROUP)

policy-systems: ## List systems bound to a policy (POLICY=<name|id>)
	$(JCLOUD) policies systems $(POLICY)

policy-groups: ## List system groups bound to a policy (POLICY=<name|id>)
	$(JCLOUD) policies groups $(POLICY)

policy-compliance: ## Show policy compliance across all systems (POLICY=<name|id>)
	$(JCLOUD) policies compliance $(POLICY)

# ── RADIUS ───────────────────────────────────────────────────────────

list-radius: ## List RADIUS servers
	$(JCLOUD) radius list

get-radius: ## Get RADIUS server details (RADIUS=<id>)
	$(JCLOUD) radius get $(RADIUS)

# ── Applications ─────────────────────────────────────────────────────

list-apps: ## List SSO applications
	$(JCLOUD) apps list

get-app: ## Get application details (APP=<id>)
	$(JCLOUD) apps get $(APP)

# ── System Insights ─────────────────────────────────────────────────

insight-tables: ## List available System Insights tables
	$(JCLOUD) insights tables

insight-query: ## Query a System Insights table (TABLE=<name> SYSTEM=<optional>)
	$(JCLOUD) insights query $(TABLE) $(if $(SYSTEM),--system $(SYSTEM))

insight-os: ## Show OS versions across all systems
	$(JCLOUD) insights os

insight-encryption: ## Show disk encryption status across all systems
	$(JCLOUD) insights encryption

insight-apps: ## List installed applications (SYSTEM=<optional>)
	$(JCLOUD) insights apps $(if $(SYSTEM),--system $(SYSTEM))

# ── Directory Insights / Events ─────────────────────────────────────

list-events: ## List events (SERVICE=all|sso|directory|... START=<iso> END=<iso> SEARCH=<term>)
	$(JCLOUD) events list $(if $(SERVICE),--service $(SERVICE)) \
		$(if $(START),--start $(START)) $(if $(END),--end $(END)) \
		$(if $(SEARCH),--search $(SEARCH)) $(if $(LIMIT),--limit $(LIMIT))

event-logins: ## Show login events (START=<iso> END=<iso>)
	$(JCLOUD) events logins $(if $(START),--start $(START)) $(if $(END),--end $(END))

event-count: ## Get event counts (SERVICE=all|sso|... START=<iso> END=<iso>)
	$(JCLOUD) events count $(if $(SERVICE),--service $(SERVICE)) \
		$(if $(START),--start $(START)) $(if $(END),--end $(END))

# ── Authentication Policies ─────────────────────────────────────────

list-authn-policies: ## List authentication policies
	$(JCLOUD) authn list

get-authn-policy: ## Get auth policy details (POLICY=<id>)
	$(JCLOUD) authn get $(POLICY)

create-authn-policy: ## Create auth policy (NAME=<name> TYPE=<type> MFA=yes|no DEVICE_TRUST=yes|no DISABLED=yes|no)
	$(JCLOUD) authn create --name '$(NAME)' \
		$(if $(TYPE),--type $(TYPE)) \
		$(if $(filter yes,$(MFA)),--mfa-required,--no-mfa-required) \
		$(if $(filter yes,$(DEVICE_TRUST)),--device-trust) \
		$(if $(filter yes,$(DISABLED)),--disabled,--enabled)

update-authn-policy: ## Update auth policy (POLICY=<id> NAME=<name> MFA=yes|no DISABLED=yes|no)
	$(JCLOUD) authn update $(POLICY) \
		$(if $(NAME),--name '$(NAME)') \
		$(if $(filter yes,$(MFA)),--mfa-required) \
		$(if $(filter no,$(MFA)),--no-mfa-required) \
		$(if $(filter yes,$(DISABLED)),--disabled) \
		$(if $(filter no,$(DISABLED)),--enabled)

# ── IP Lists ────────────────────────────────────────────────────────

list-ip-lists: ## List IP lists
	$(JCLOUD) ip-lists list

get-ip-list: ## Get IP list details (LIST=<id>)
	$(JCLOUD) ip-lists get $(LIST)

create-ip-list: ## Create IP list (NAME=<name> IPS=<ip1,ip2,...>)
	$(JCLOUD) ip-lists create --name '$(NAME)' --ips '$(IPS)'

# ── API Metadata ────────────────────────────────────────────────────

org-info: ## Show organization info and API settings
	$(JCLOUD) meta org

policy-templates: ## List available policy templates
	$(JCLOUD) meta policy-templates

directories: ## List configured directories (Google Workspace, LDAP, AD)
	$(JCLOUD) meta directories
