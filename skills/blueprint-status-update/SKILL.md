---
name: blueprint-status-update
description: "Audit and update roadmap project statuses by pulling from connected resources (Linear, Slack, Jira). Use when asked to run status updates, write weekly updates, sync Linear to the project tracker, update projects, audit project health, check project staleness, nudge project leads, or generate weekly status reports."
argument-hint: "Optional: specific project name or 'all' (default: all active DRI projects)"
depends-on: [slack, linear]
references: [airtable]
---

# Roadmap Status Update

Audits and updates roadmap project statuses by pulling from Connected Resources (Linear, Slack, Jira, etc.), up-leveling into PM-friendly format, and writing to the project tracker with user approval.

**STOP** if any of these are missing — the skill cannot function without them:
- Airtable API token (see `SETUP.md`)
- Linear API key (see `SETUP.md`)
- Slack skill installed and authenticated

## Prerequisites

- Linear API key environment variable must be set (see `SETUP.md`)
- Airtable token configured (see `SETUP.md`)
- Slack skill authenticated with full scopes (for DM nudges and reading channels)
- Mapping DB at `~/.config/amp/project-linear-map.json` (auto-discovered on first run)

## Workflow

Load `references/workflow.md` for the full step-by-step workflow.

### High-Level Steps

1. **Load Projects** — Query Airtable for active projects where you are DRI
2. **Gather Connected Resources** — Pull linked Linear projects, Slack channels, Jira epics
3. **Check for Fresh Updates** — Query each source for recent activity (last 7 days)
4. **Run Health Audit** — Flag stale updates, overdue dates, status mismatches, missing fields
5. **Present Findings** — Show one project at a time with proposed update for user approval
6. **Write Approved Updates** — Create status update records in Airtable
7. **Nudge Missing Updates** — Send Slack DMs to project leads who haven't posted updates
8. **Demo Proposals** — Suggest demo-worthy items from shipped work with eng lead names
9. **Final Summary** — Report what was updated, nudged, skipped, and health issues found

> **Tip:** After running this skill, use `weekly-status-summary` to assemble a consolidated Slack message from the approved updates.

## Key Rules

- Always show a diff of proposed changes before writing — never auto-write without approval
- Present one project at a time — don't batch approvals
- Use `- ` (dash) for bullets in updates, NOT `•` — the project tracker renders `- ` as proper bullets
- Remove internal eng jargon but keep enough technical context for comprehension
- Frame progress in terms of user/customer impact where possible
- Preserve dates, percentages, metrics, and platform breakdowns

## Reference Files

- `references/workflow.md` — Full update cycle step-by-step
- `references/field-ids.md` — Airtable base, table, and field IDs
- `references/update-format.md` — Formatting guidelines and template
