---
Skill name: historical-info
Skill description: Searches across multiple sources to find what the user is or has been working on. Use when asked about historical information, past activities, current work, or what they've been doing.
---

# Historical Information Lookup

Provides a comprehensive summary of the user's activities and impact by searching across multiple data sources **in parallel**.

## Sources

When the user asks about what they're working on, what they've done, or any historical activity, query **all** of the following:

1. **Glean** — enterprise knowledge search (Confluence, Jira, etc.). Use the `glean` skill.
2. **Google Drive** — documents, spreadsheets, presentations. Use the `gdrive` skill.
3. **GitHub** — pull requests, commits, code reviews. Use `gh` CLI.
4. **Slack** — messages, conversations, decisions. Use the `slack` skill.
5. **Linear** — issues, projects, tasks assigned to the user. Use Linear MCP tools.
6. **Notion** — pages, databases, tasks, notes. Search for relevant content.
7. **Employee Directory** — verify key contributors are still active. Use the employee directory via `gdrive` skill.
8. **LaunchDarkly Feature Flags** — flag states, rollout percentages, stale flags. Use `ldcli` CLI.
9. **Airtable (Roadmap)** — project priority, phase, roadmap quarter, DRI(s), staffing, status updates, and timeline. Use the Airtable API. Search the Roadmap base for projects where the user is a DRI or assignee.

## Workflow

1. **Query all sources in parallel** — they are independent of each other.
2. **Synthesize** — combine findings into a unified summary grouped by project or workstream.
3. **Highlight** — call out active work, recent completions, blockers, and upcoming deadlines.

## User Identity

- Name: Your Name
- Username: your_username
- Email: your_email@example.com

Use these identifiers when filtering results by assignee, author, or owner across all sources.
