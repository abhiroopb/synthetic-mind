---
name: blueprint-project-status
description: "Audit and update roadmap project statuses in bulk. Use when reviewing, auditing, sweeping, triaging, or cleaning up stale projects in your project tracking system (Airtable). Scans either a user-selected view or the current person's owned projects (DRI, Eng DRI, PM DRI, Design DRI), cross-references Slack channels, Linear tickets, and Jira issues via Connected Resources, flags projects with stale updates, overdue dates, mismatched signals, or missing fields, and guides the user through correcting them."
depends-on: [airtable, slack, linear, jira]
references: [launch-a-product]
metadata:
  version: "1.1.0"
  status: beta
---

# Roadmap Project Status Auditor

Portfolio-level status auditor for roadmap projects. Scans either an Airtable view or a user's owned projects, cross-references external signals (Slack, Linear, Jira), identifies projects that need attention, and guides the user through updating them.

**Scope:** Audit and update project status fields. No GTM preparation, positioning, or comms drafting — use `launch-a-product` for that.

**Context:** Your project tracking system is the source of truth for project tracking. Status updates, dates, and field completeness directly feed downstream processes (bundle inclusion, GTM, CS/AM enablement, leadership summaries). Stale or inaccurate data degrades all of these.

## Prerequisites

**STOP** if any of these are not met — tell the user what's missing.

- Connected to corporate VPN
- Airtable MCP enabled
- Slack MCP enabled
- Linear and/or Jira MCP enabled (depending on project tooling)

## Key IDs

| Resource | ID |
|----------|-----|
| Project Tracking Base | `<your-airtable-base-id>` |
| Projects Table | `<your-projects-table-id>` |
| Status Updates Table | `<your-status-updates-table-id>` |
| Connected Resources Table | `<your-connected-resources-table-id>` |

## Core Workflow

### Step 1: Select Project Source

```text
Welcome to Roadmap Project Status Audit!

I'll scan either a view or your owned projects, cross-reference
Slack/Linear/Jira activity, and flag projects that need attention.

How would you like to choose projects?
  1. Scan an Airtable view
  2. Audit my owned projects (DRI, Eng DRI, PM DRI, Design DRI)
```

- [ ] If the user chooses **view mode**, ask for a view name, view ID, or link
- [ ] If the user chooses **ownership mode**, ask for the person to match (name, email, or LDAP)
- [ ] In ownership mode, resolve the person against the People Database using `list_records` with `filterByFormula`
- [ ] If multiple matches are found, show the candidates and ask the user to choose

### Step 2: Load Projects

- [ ] If using **view mode**, fetch all records from the user-provided view using `list_records` with the `view` query parameter. **Paginate** through all results
- [ ] If using **ownership mode**, resolve the selected person to a People record ID, then fetch active owned projects with a `filterByFormula` combining active statuses with DRI ownership
- [ ] Filter to active projects only: status is `Not Started`, `In Progress`, `At Risk`, or `Blocked`
- [ ] For each project, note: Project Name, Project Status, Expected Completion Date, Rollout Start Date, Development Start Date, Most Recent Update Date, DRI, Eng DRI, PM DRI, Design DRI, Requesting Organization, Connected Resources link
- [ ] Display count: "Found X active projects. Scanning for issues..."

### Step 3: Gather External Context

For each active project, gather signals from connected resources:

**3a. Find Connected Resources**
- [ ] Query the Connected Resources table filtering by project record ID
- [ ] Also check the project's Jira/Linear and Slack Channel fields as fallbacks

**3b. Check Slack Activity**
- [ ] For each Slack channel found, search for recent messages (last 7 days)
- [ ] Note: active discussion, blockers mentioned, shipped announcements, silence

**3c. Check Linear/Jira Activity**
- [ ] For each Linear or Jira resource found, check recent activity
- [ ] Note: open issues, recent completions, blockers, milestone progress

### Step 4: Run Audit — Flag Issues

| Signal | Condition | Severity |
|--------|-----------|----------|
| **Stale Update** | No status update in 7+ days | 🔴 High |
| **Overdue** | Expected Completion Date is in the past but status is not `Delivered` | 🔴 High |
| **Status Mismatch** | Slack/Linear/Jira signals contradict Airtable status | 🟡 Medium |
| **Missing Required Fields** | Empty fields that should be filled for current phase | 🟡 Medium |
| **Date Drift** | Dates appear inconsistent with external signals | 🟡 Medium |
| **No Connected Resources** | No Slack channel, Linear project, or Jira ticket linked | 🟡 Medium |

### Step 5: Present Findings

Display a summary table of all flagged projects, sorted by severity:

```text
## Audit Results: [View Name or Person Scope]

Scanned X active projects. Y need attention.

### 🔴 High Priority (Z projects)

| Project | Status | Issue | Signal Source | Suggested Action |
|---------|--------|-------|---------------|------------------|
| Project Alpha | In Progress | Stale update (14 days) | Airtable | Add weekly status update |
| Project Beta | In Progress | Overdue (target was Mar 10) | Airtable | Update date or mark Delivered |

### 🟡 Medium Priority (Z projects)

| Project | Status | Issue | Signal Source | Suggested Action |
|---------|--------|-------|---------------|------------------|
| Project Gamma | In Progress | Shipped in Slack but still "In Progress" | #project-gamma | Update status to Delivered |

### ✅ Clean (Z projects)
Projects with no issues detected.
```

Then ask which projects to update (all, specific, or high-priority only).

### Step 6: Guide Updates

For each selected project, walk the user through fixes:

**For stale updates:**
- [ ] Summarize what was found in Slack/Linear/Jira as a draft update
- [ ] Ask user to confirm or edit the draft
- [ ] Propose RYG status (🟢/🟡/🔴) based on signals
- [ ] Write to Status Updates table, linked to the project

**For overdue dates:**
- [ ] Show current date vs. Expected Completion Date
- [ ] Ask: "Should I update the date, or has this been delivered?"

**For status mismatches:**
- [ ] Show the contradiction and propose the corrected status
- [ ] Get user confirmation

**For missing fields:**
- [ ] List missing required fields with descriptions and available options
- [ ] Try to infer values from Slack/Linear/Jira context

**For all updates:**
- [ ] Always show a diff of proposed changes before writing
- [ ] Get explicit user approval before any Airtable write

### Step 7: Summary

```text
## Audit Complete

Updated: X projects
- Y status updates written
- Z fields corrected
- W dates updated

Still needs attention: N projects
[List any remaining flagged projects the user skipped]

Run this audit again anytime to keep your roadmap current.
```

## Anti-patterns

- Don't update Airtable without showing the user a diff and getting approval
- Don't write status updates directly to the project record — always use the Status Updates table
- Don't assume a project is delivered just because Slack is quiet — ask the user
- Don't skip the Connected Resources table — it's the primary source for linked resources
- Don't scan the entire Projects table unless the user explicitly chose ownership mode
