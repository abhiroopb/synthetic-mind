---
name: blueprint-project-update
description: "Draft and add weekly roadmap project updates. Use when writing, drafting, preparing, updating, posting, or refreshing a weekly status, project update, progress report, rollout check-in, or risks/blockers entry for one specific roadmap project. Starts from the project record, follows linked resources, summarizes the last 7 days, and creates a new Status Updates row after approval."
depends-on: [airtable]
references: [blueprint-status-update, gh-pr-read, slack, gdrive, linear, launch-a-product, project-status]
argument-hint: "Project name, Airtable URL, or record ID"
metadata:
  version: "1.0.0"
  status: beta
---

# Roadmap Project Update

Draft a weekly project update for any project lead. Start from the project record, gather evidence only from resources already linked on that project, synthesize **Progress / Problems / Plans** internally, then map that into the project tracking system's `Weekly Status`, `Update`, and `Risks/Blockers` fields.

**Scope:** Weekly updates for one selected project at a time. This skill does not replace full GTM readiness work, broad project investigation, or batch portfolio syncing.

## Prerequisites

**STOP** if any of these are not met:

- Airtable access to the project tracking base is unavailable
- The project cannot be uniquely resolved from the user input

Before gathering evidence, confirm you can access the linked systems that appear on the project record. If a linked source such as Linear, GitHub, Slack, Google Drive, or feature flags is unavailable, note the gap and continue with the evidence you do have.

## Core Workflow

### Step 1: Identify the Current User

- [ ] Determine the current user's email address from session context; fall back to Slack `get_user_info` with username `me`
- [ ] Look up the user in the People Database table by filtering on the `Email` field
- [ ] Store the matching People record ID for the `Submitted - By` field
- [ ] If no match is found, warn the user and continue

### Step 2: Resolve the Project

- [ ] Search the Projects table using the project name, Airtable URL, or record ID from `$ARGUMENTS`
- [ ] If multiple matches are found, show a disambiguation list
- [ ] Fetch the full project record and show a brief summary: project name, status, DRI, owning org, and linked resources

### Step 3: Gather Recent Evidence

- [ ] Read the 2-3 most recent status updates linked to this project for context
- [ ] Follow only the resources already linked on the project record
- [ ] Use the last 7 days as the default evidence window
- [ ] Do not do broad org-wide searches — continue with available evidence

### Step 4: Draft Progress / Problems / Plans

- [ ] Build an internal PPP view from the evidence
- [ ] Keep `Progress` limited to work completed or meaningfully advanced in the last 7 days
- [ ] Include `Problems` only when backed by evidence
- [ ] Keep `Plans` focused on the next 1-2 concrete outcomes

### Step 5: Map the Draft into Fields

- `Weekly Status`: 🟢 (on track) / 🟡 (risk or dependency) / 🔴 (blocked or slipping)
- `Update`: Concise summary of what moved this week and what happens next
- `Risks/Blockers`: Leave empty when no material risks; otherwise summarize plainly

### Step 6: Review in Chat Before Writing

- [ ] Show the user the exact proposed diff before writing
- [ ] Revise the draft in chat if the user wants changes
- [ ] Stop here unless the user explicitly approves the write

### Step 7: Create the Status Update Record

- [ ] Create a new record in the Status Updates table
- [ ] Link it to the project record
- [ ] Set the `Submitted - By` field to the resolved People record ID
- [ ] Never overwrite a prior status-update record
- [ ] Confirm the new record was created and summarize what was written

## Output Rules

- Always show the draft directly in chat first
- Keep the final `Update` concise and recent
- Prefer summaries over verbatim quotes from Slack or docs
- Do not include secrets, credentials, or unnecessary PII
- If evidence is thin, say so clearly instead of inventing confidence

## Related Skills

- **blueprint-status-update** — Batch update sweep rather than single-project drafts
- **gh-pr-read** — When a linked resource is a GitHub PR
- **launch-a-product** — Broader GTM readiness workflow
- **project-status** — Wider multi-system project investigation
