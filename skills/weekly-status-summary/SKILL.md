---
name: weekly-status-summary
description: "Generate and post a consolidated weekly Slack summary from roadmap project updates. Use when assembling, generating, creating, drafting, posting, compiling, or formatting a weekly status summary, team update, or status rollup for Slack from project tracking data."
depends-on: [slack, blueprint-status-update]
references: [airtable, snowflake]
---

# Weekly Status Summary

Generates a consolidated Slack message summarizing all recent roadmap project updates for the week. Designed to run after `blueprint-status-update` has posted individual project updates.

**STOP** if any of these are missing:
- Airtable API token configured
- Slack skill installed and authenticated

## Workflow

Load `references/workflow.md` for the full step-by-step workflow.

### High-Level Steps

1. **Load Config** — Read `~/.config/amp/weekly-summary.json` or run first-time setup
2. **Gather Updates** — Pull this week's status updates for the user's projects
3. **Pull Metrics** — Fetch headline metrics from configured sources (data warehouse, Slack, or manual)
4. **Assemble Message** — Build Slack mrkdwn message with project summaries, demo links, and metrics
5. **Preview and Post** — Show in chat for review, ask which Slack channel to post to

## Key Rules

- Every project name must be a clickable link to the project tracker
- Summarize each project's update into a single concise line
- Format numbers with commas
- Always preview in chat before posting
- Ask the user which channel to post to — never auto-post
