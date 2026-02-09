---
status: resolved
trigger: "Investigate why `acli whoami` command fails with unknown command error"
created: "2026-02-08T00:00:00Z"
updated: "2026-02-08T00:00:00Z"
---

## Current Focus

hypothesis: acli does not have a 'whoami' command - it uses 'jira auth status' instead
test: Check acli help and test auth commands
expecting: Find correct auth check command
next_action: Provide diagnosis

## Symptoms

expected: acli authentication check should work without errors
actual: Command 'acli whoami' failed with exit code 1: unknown command 'whoami' for 'acli'
errors: "× Error: unknown command 'whoami' for 'acli'"
reproduction: Run uv run monocli, Work Items section shows error
started: Unknown

## Eliminated

- hypothesis: acli is not installed
  evidence: 'which acli' found it at /opt/homebrew/bin/acli
  timestamp: 2026-02-08

- hypothesis: acli has whoami but with different syntax
  evidence: 'acli --help' shows no whoami command; available commands: admin, auth, confluence, jira, rovodev, completion, config, feedback, help
  timestamp: 2026-02-08

## Evidence

- timestamp: 2026-02-08
  checked: acli help output
  found: "Available Commands: admin, auth, confluence, jira, rovodev, completion, config, feedback, help" - NO whoami command exists
  implication: The code references a non-existent command

- timestamp: 2026-02-08
  checked: acli auth subcommands
  found: "Available Commands: login, logout, status, switch"
  implication: 'acli auth status' exists and shows authentication status

- timestamp: 2026-02-08
  checked: acli jira auth status
  found: "✓ Authenticated, Site: axpopolska.atlassian.net, Exit code: 0"
  implication: 'acli jira auth status' is the correct command to verify Jira authentication

- timestamp: 2026-02-08
  checked: File /Users/pg/Coding/_bucket/monocli/src/monocli/adapters/jira.py line 94
  found: "await self.run([\"whoami\"], check=True)" in check_auth() method
  implication: This file uses invalid command

- timestamp: 2026-02-08
  checked: File /Users/pg/Coding/_bucket/monocli/src/monocli/ui/main_screen.py line 124
  found: "registry.register(CLIDetector(\"acli\", [\"whoami\"]))"
  implication: This file also uses invalid command

## Resolution

root_cause: acli (Atlassian CLI) does not have a 'whoami' command. The correct command to check authentication is 'acli jira auth status' (for Jira-specific auth) or 'acli auth status' (for global auth). Both source files incorrectly use ['whoami'] as the auth check command.

fix: Replace ['whoami'] with ['jira', 'auth', 'status'] in both files

verification: Tested 'acli jira auth status' - returns exit code 0 with authentication info when authenticated, suitable for auth checking

files_changed:
  - /Users/pg/Coding/_bucket/monocli/src/monocli/adapters/jira.py: line 94, change ["whoami"] to ["jira", "auth", "status"]
  - /Users/pg/Coding/_bucket/monocli/src/monocli/ui/main_screen.py: line 124, change ["whoami"] to ["jira", "auth", "status"]
