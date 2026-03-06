---
Skill name: creating-tasks-cli
Skill description: Creates tasks via a task management CLI, including labels, status, and artifacts. Use when you need to create or update tasks from the command line.
---

# Creating Tasks (CLI)

Create tasks with a task management CLI and attach labels/artifacts.

## When to use

- You need to create a task programmatically or from the terminal
- You need to attach artifacts or update status quickly
- The web UI is not available or inconvenient

## Prerequisites

- Task CLI is built and on PATH
- You have access (appropriate role or equivalent)

Check the CLI first:

```bash
taskcli --help
```

If the CLI is not built yet or not on PATH, build it quickly:

```bash
cd ~/Development/task-manager
just build-all
```

If the repo is missing, clone and build it:

```bash
cd ~/Development
git clone <org>@github.com:<org>/task-manager.git
cd task-manager
just build-all
```

If `taskcli` still isn't on PATH, ask for or probe a direct path and use it explicitly (common build path: `~/Development/task-manager/build/taskcli`).

## Quick reference

```bash
# Find and view tasks
taskcli list
taskcli show <key>

# Attach artifacts (message or URL)
taskcli attach <key> --type=message --title="Title" --content="..."
taskcli attach <key> --type=pr --url=<url>

# Update/edit an artifact (use artifact key from task show)
taskcli overwrite <artifact-key> --content="..."
taskcli overwrite <artifact-key> --title="..."

# Update task status
taskcli update <key> --status=in_progress
taskcli update <key> --status=complete

# Create subtask (if needed)
taskcli create "description" --parent=<parent-key>
```

Batch helpers:

```bash
# Create, move to in progress, attach repo (repeat per task)
taskcli create "<ticket>: <short goal>" --label <label>
taskcli update <key> --status=in_progress
taskcli attach <key> --type=repo --url=github.com/<org>/<repo>
```

## Choose a label

Ask which executor label they want, then explain options briefly. Do not preselect or suggest a label unless the user explicitly asks for a recommendation:

- `headless` - automated PRs via headless agent
- `workflow` - workflow engine automations
- `workstation` - runs agents in virtual workstations (requires access)
- `agent:amp` - uses Amp as the agent (preferred)
- `agent:claude` - uses Claude Code as the agent (default)
- `agent:goose` - uses Goose as the agent

If they are unsure, ask what kind of output they want (automated PR, automation workflow, or workstation) and let them choose without picking a label for them.

## Choose an artifact

Ask what artifact they want to attach:

- `repo` - required for headless agent when work happens in a repo
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

After creating the task, show the task details with `taskcli show <key>` and link the task in the UI (e.g., `https://<task-ui-url>/tasks/<key>`).

## Executor access pointers

- Headless agent: ensure `headless` label + repo artifact; see internal docs for setup
- Workstation: requires workstation access; see internal docs for setup
- Workflow: access is provisioned in the workflow engine; see internal docs for setup

## Notes

- Headless agent requires: `headless` label + `READY` status + repo artifact
- Tasks with dependencies must have zero incomplete dependencies to be picked up

## Example

```bash
taskcli create "Clean up unused feature flags in dashboard; follow recipe steps and open a PR."
# suppose output shows TSK-1234
taskcli update TSK-1234 --status=in_progress
taskcli attach TSK-1234 --type=repo --url=github.com/<org>/dashboard
```

Batch example with a direct CLI path:

```bash
/Users/me/Development/task-manager/build/taskcli create "ABC-1234: Update request logging in foo service." --label headless
/Users/me/Development/task-manager/build/taskcli update TSK-1001 --status=in_progress
/Users/me/Development/task-manager/build/taskcli attach TSK-1001 --type=repo --url=github.com/<org>/my-service
```
