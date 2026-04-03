---
name: hermit
description: Use when installing, managing, listing, searching, upgrading, configuring, or troubleshooting developer tools and CLI binaries in a repository that uses Hermit for hermetic package management. Also use when agents attempt to install tools via brew, apt, npm, go install, pip, or other system package managers in a Hermit-managed repo, or when a required CLI tool is missing from the PATH.
metadata:
  status: experimental
  version: "1.0"
---

# Hermit Package Manager

Hermit is a hermetic binary package manager. It pins exact tool versions per-repository via lightweight proxy scripts in `bin/`, without polluting the system PATH.

## Detecting Hermit

A repository uses Hermit if it has a `bin/hermit` file. Before installing tools via system package managers or running bare tool names, check for Hermit:

- If the working directory contains `bin/hermit`, use Hermit for all tool management
- When in doubt, check before reaching for `brew`, `apt`, or `npm install -g`

## Critical Rules

1. **NEVER use bare tool names from the system PATH** (e.g., `gradle`, `node`, `go`). Always use the `bin/` prefix (e.g., `bin/gradle`, `bin/node`, `bin/go`).
2. **NEVER use wrapper scripts like `./gradlew` or `gradlew`** — Hermit replaces these. Use `bin/gradle`.
3. **NEVER install non-Hermit-packaged tools unilaterally when Hermit is present.** If a tool is not available via `bin/hermit search`, ask the user before installing via other package managers.
4. **Always run `bin/<tool>` from the repository root.**

## Commands

```bash
bin/hermit list                    # List installed packages
bin/hermit search <query>          # Search available packages
bin/hermit install <package>       # Install a package (available as bin/<tool>)
bin/hermit upgrade <package>       # Upgrade a package
bin/hermit info <package>          # Show package details
bin/hermit status                  # Check environment status
```

## When a Tool is Missing

If a command fails with "command not found" and the repo uses Hermit:

- [ ] Check if the tool exists: `ls bin/<tool-name>`
- [ ] If not found, search for it: `bin/hermit search <tool-name>`
- [ ] If available, install it: `bin/hermit install <tool-name>`
- [ ] If not in Hermit, ask the user how they'd like to proceed

## Configuration

Hermit environment configuration lives in `bin/hermit.hcl`, which defines package manifest sources and environment variables active when Hermit is enabled.
