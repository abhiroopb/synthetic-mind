---
name: jira
description: Interact with Jira issue tracking using Atlassian CLI (ACLI). Use when listing, viewing, searching, creating, editing, updating, transitioning, commenting on, assigning, or managing Jira issues, tickets, stories, bugs, epics, or sprints.
metadata:
  version: "1.0.0"
  status: stable
---

# Jira (ACLI)

Interact with Jira using the official Atlassian CLI (`acli`).

## Prerequisites

Before running any Jira commands, verify ACLI is installed and authenticated. See `SETUP.md` for installation and auth instructions.

```bash
which acli && acli jira auth status
```

**CRITICAL:** Authentication cannot be automated — ACLI requires interactive TTY input. Do NOT attempt to pipe tokens. Tell the user to run auth commands themselves.

---

## Quick Reference

| Action | Command |
|--------|---------|
| View issue | `acli jira workitem view KEY-123` |
| Search issues | `acli jira workitem search --jql "..."` |
| Create issue | `acli jira workitem create -p PROJECT -t Task -s "Summary"` |
| Transition | `acli jira workitem transition -k KEY-123 -s "Done"` |

---

## Search Issues

```bash
# Search with JQL
acli jira workitem search --jql "project = PROJ"

# My assigned issues
acli jira workitem search --jql "assignee = currentUser()"

# My in-progress issues
acli jira workitem search --jql "assignee = currentUser() AND status = 'In Progress'"

# My tasks in current sprint
acli jira workitem search --jql "assignee = currentUser() AND sprint in openSprints() ORDER BY updated DESC" --paginate

# Output formats
acli jira workitem search --jql "project = PROJ" --csv
acli jira workitem search --jql "project = PROJ" --json
acli jira workitem search --jql "project = PROJ" --count
acli jira workitem search --jql "project = PROJ" --web
```

---

## View Issue

```bash
acli jira workitem view KEY-123
acli jira workitem view KEY-123 --fields "*all"
acli jira workitem view KEY-123 --json
acli jira workitem view KEY-123 --web
```

---

## Create Issue

```bash
# Basic creation
acli jira workitem create \
  --project "PROJ" \
  --type "Task" \
  --summary "Issue title"

# With description
acli jira workitem create \
  --project "PROJ" \
  --type "Bug" \
  --summary "Bug title" \
  --description "Bug description"

# Assign to self
acli jira workitem create \
  --project "PROJ" \
  --type "Task" \
  --summary "My task" \
  --assignee "@me"

# Sub-task
acli jira workitem create \
  --project "PROJ" \
  --type "Sub-task" \
  --summary "Sub-task" \
  --parent "KEY-123"
```

Issue types: `Epic`, `Story`, `Task`, `Bug`, `Sub-task`

---

## Transition Issue

```bash
acli jira workitem transition --key "KEY-123" --status "In Progress"
acli jira workitem transition --key "KEY-123" --status "Done"
acli jira workitem transition --key "KEY-123" --status "Done" --yes
```

---

## Comments

```bash
acli jira workitem comment create --key "KEY-123" --body "Comment text"
acli jira workitem comment list KEY-123
```

---

## Assign Issue

```bash
acli jira workitem assign --key "KEY-123" --assignee "user@company.com"
acli jira workitem assign --key "KEY-123" --assignee "@me"
```

---

## Edit Issue

```bash
acli jira workitem edit --key "KEY-123" --summary "New title"
acli jira workitem edit --key "KEY-123" --labels "new-label"
```

### Rich Text Descriptions (ADF)

`--description "text"` renders as plain text. For rich formatting with headings, bold, code blocks, and lists, use `--from-json` with Atlassian Document Format (ADF). Load `references/rich-text-adf.md` for the full JSON format.

---

## Projects

```bash
acli jira project list --limit 50
acli jira project view PROJ
```

---

## Boards & Sprints

```bash
acli jira board search
acli jira board list-sprints --id 123
acli jira sprint list-workitems --sprint 456 --board 123
```

---

## Tips

- Use `--json` for structured output when parsing
- Use `--csv` for spreadsheet-compatible output
- Use `--web` to quickly open in browser
- Use `@me` for self-assignment
- Use `--yes` to skip confirmations in scripts

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| Not authenticated | Run `acli jira auth login` (see `SETUP.md`) |
| Project not found | Check project key with `acli jira project list` |
| Transition not allowed | Check workflow allows this status change |

---

## Notes

- Jira instance: `https://your-org.atlassian.net`
- Uses OAuth authentication (no API tokens needed)
- ACLI docs: https://developer.atlassian.com/cloud/acli/

---

## References

- `references/rich-text-adf.md` — Rich formatting for descriptions
- `references/jql-queries.md` — JQL query examples
- `references/common-workflows.md` — Multi-step workflow patterns
