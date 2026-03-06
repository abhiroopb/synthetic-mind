---
name: creating-builderbot-tasks
description: Creates Builderbot tasks via the Builderbot CLI, including labels, status, and artifacts. Use when you need to create or update Builderbot tasks from the command line.
---

# Creating Builderbot Tasks (CLI)

Create Builderbot tasks with the CLI (`builderbot`) and attach labels/artifacts.

## When to use

- You need to create a task programmatically or from the terminal
- You need to attach artifacts or update status quickly
- The web UI is not available or inconvenient

## Prerequisites

- Builderbot CLI is built and on PATH
- You have Builderbot access (role `builderbot--users` or equivalent)

Check the CLI first:

```bash
builderbot --help
```

If the CLI is not built yet or not on PATH, build it quickly:

```bash
cd ~/Development/BuilderBot
just build-all
```

If the repo is missing, clone and build it:

```bash
cd ~/Development
git clone org-49461806@github.com:squareup/builderbot.git
cd builderbot
just build-all
```

If `builderbot` still isn't on PATH, ask for or probe a direct path and use it explicitly (common build path: `~/Development/builderbot/build/builderbot`).

## Quick reference

```bash
# Find and view tasks
builderbot list
builderbot show <key>

# Attach artifacts (message or URL)
builderbot attach <key> --type=message --title="Title" --content="..."
builderbot attach <key> --type=pr --url=<url>

# Update/edit an artifact (use artifact key from task show)
builderbot overwrite <artifact-key> --content="..."
builderbot overwrite <artifact-key> --title="..."

# Update task status
builderbot update <key> --status=in_progress
builderbot update <key> --status=complete

# Create subtask (if needed)
builderbot create "description" --parent=<parent-key>
```

Batch helpers:

```bash
# Create, move to in progress, attach repo (repeat per task)
builderbot create "<ticket>: <short goal>" --label <label>
builderbot update <key> --status=in_progress
builderbot attach <key> --type=repo --url=github.com/squareup/<repo>
```

## Choose a label

Ask which executor label they want, then explain options briefly. Do not preselect or suggest a label unless the user explicitly asks for a recommendation:

- `devbox` (Headless Goose) - automated PRs via Goose
- `g2` - G2 workflows and automations
- `blox` - Blox runs agents in virtual workstations (requires Blox access)
- `agent:amp` - uses Amp as the agent (preferred)
- `agent:claude` - uses Claude Code as the agent (default)
- `agent:goose` - uses Goose as the agent

If they are unsure, ask what kind of output they want (automated PR, automation workflow, or workstation) and let them choose without picking a label for them.

## Choose an artifact

Ask what artifact they want to attach:

- `repo` - required for Goose/Blox when work happens in a repo
- `pr` - attach a pull request URL
- `message` - notes or instructions
- `url` - any reference link

## Task description template

Use a consistent description format for scanability:

```text
<TICKET-ID>: <short goal>.
```

## Preview before creating

Before creating a task, show the user a short preview of what you are about to run (description, labels, and artifacts) and wait for confirmation.

After creating the task, show the task details with `builderbot show <key>` and link the task in the UI (e.g., `https://blockcell.sqprod.co/sites/builderbot/tasks/<key>`).

## Executor access pointers

- Headless Goose: ensure `devbox` label + repo artifact; see https://dev-guides.sqprod.co/docs/tools/goose/getting-started
- Blox: requires `blox--users` access; see https://dev-guides.sqprod.co/docs/tools/blox/getting-started/overview
- G2: access is provisioned in G2; see https://dev-guides.sqprod.co/docs/tools/builderbot/getting-started

## Notes

- Headless Goose requires: `devbox` label + `READY` status + repo artifact
- Tasks with dependencies must have zero incomplete dependencies to be picked up

## Example

```bash
builderbot create "Clean up unused LaunchDarkly flags in dashboard; follow recipe steps and open a PR."
# suppose output shows TSK-1234
builderbot update TSK-1234 --status=in_progress
builderbot attach TSK-1234 --type=repo --url=github.com/squareup/dashboard
```

Batch example with a direct CLI path:

```bash
/Users/me/Development/builderbot/build/builderbot create "ABC-1234: Update request logging in foo service." --label devbox
/Users/me/Development/builderbot/build/builderbot update TSK-1001 --status=in_progress
/Users/me/Development/builderbot/build/builderbot attach TSK-1001 --type=repo --url=github.com/squareup/cash-server
```
