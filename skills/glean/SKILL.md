---
name: glean
description: Use when searching, querying, looking up, finding, browsing, or discovering your company's internal knowledge base, wiki pages, policies, company information, or internal resources via Glean. Also use when querying Glean AI for answers or checking what documents exist on a topic.
roles: [cash-ios]
allowed-tools:
  - Bash(scripts/block-glean-cli:*)
  - Bash(lsof -ti :8030:*)
metadata:
  author: mikewilliams
  version: "1.0.0"
  status: experimental
---

# Glean Enterprise Search

Search your company's internal knowledge base, chat with Glean AI, and read document content.

Based on the `mcp_glean` MCP server, reimplemented as a self-contained CLI
with no dependency on `mcp_glean` at runtime.

The `block-glean-cli` is located at `scripts/block-glean-cli`.

## Quick reference

- **Search:** `scripts/block-glean-cli search "query"` (with optional `--datasource`, `--limit`)
- **Chat:** `scripts/block-glean-cli chat "question"` (with optional `--agent-id`)
- **Read doc:** `scripts/block-glean-cli read DOC_ID` (with optional `--start`, `--end`)
- **List agents:** `scripts/block-glean-cli agents` (with optional `--name`)

## Prerequisites

This skill requires **VPN** and **SSO** access. If authentication fails with `auth_error` or `Unable to retrieve client_id`, **STOP** and tell the user:

> Glean access requires VPN and SSO. Please ensure you are connected to VPN and can access the internal portal, then try again.

## Authentication

The CLI uses OAuth with your company's SSO. Tokens are stored at `~/.config/block-glean/tokens.json`.

**Auto-authentication:** Commands automatically trigger OAuth when needed - no need to run `auth login` first.

```bash
# Check token status
scripts/block-glean-cli auth status

# Force re-authentication (if token is stale)
scripts/block-glean-cli auth login --reauth

# Remove stored tokens
scripts/block-glean-cli auth logout
```

## Search documents

Search across all indexed sources (Google Drive, Confluence, Slack, Jira, GitHub, etc).

```bash
# Basic search
scripts/block-glean-cli search "onboarding guide"

# Filter by datasource
scripts/block-glean-cli search "PTO policy" --datasource confluence

# Limit results
scripts/block-glean-cli search "incident" --limit 5
```

**Datasource filters:** `gdrive`, `confluence`, `slackentgrid`, `thehub`, `jira`, `github`, `notion`, `kaltura`

## Chat with Glean AI

Get AI-synthesized answers with citations.

```bash
# Ask a question
scripts/block-glean-cli chat "What is the PTO policy?"

# Use a specific agent
scripts/block-glean-cli chat "question" --agent-id AGENT_ID
```

## Read document content

Fetch content from a document by ID (obtained from search results).

```bash
# Read first 100 lines
scripts/block-glean-cli read DOC_ID

# Read specific line range
scripts/block-glean-cli read DOC_ID --start 50 --end 150
```

## List Glean agents

Find available Glean agents/bots.

```bash
# List all agents
scripts/block-glean-cli agents

# Search by name
scripts/block-glean-cli agents --name "People Compass"
```

## Output format

All commands output JSON:

```json
{"ok": true, "results": [...]}
{"ok": false, "error": "message", "error_type": "auth_required"}
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `auth_error` | Check VPN connection; may need `auth login --reauth` |
| `Unable to retrieve client_id` | Connect to VPN and the internal portal first |
| `Address already in use` | Kill process on port 8030: `lsof -ti :8030 \| xargs kill` |
