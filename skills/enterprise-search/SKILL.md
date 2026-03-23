---
name: enterprise-search
description: "Search your organization's internal knowledge base, chat with AI assistants, and read indexed documents. Use when searching, querying, looking up, finding, browsing, or discovering internal wiki pages, policies, company information, or internal resources."
---

# Enterprise Search

Search your organization's internal knowledge base, chat with AI assistants, and read document content.

Based on a self-contained CLI wrapper around an enterprise search API (e.g., Glean, Elasticsearch, or similar), with no external MCP dependency at runtime.

The CLI is located at `scripts/enterprise-search-cli`.

## Quick reference

- **Search:** `scripts/enterprise-search-cli search "query"` (with optional `--datasource`, `--limit`)
- **Chat:** `scripts/enterprise-search-cli chat "question"` (with optional `--agent-id`)
- **Read doc:** `scripts/enterprise-search-cli read DOC_ID` (with optional `--start`, `--end`)
- **List agents:** `scripts/enterprise-search-cli agents` (with optional `--name`)

## Prerequisites

This skill requires **VPN** and **SSO** access to your organization's enterprise search instance. If authentication fails with `auth_error` or `Unable to retrieve client_id`, **STOP** and tell the user:

> Enterprise search access requires VPN and SSO. Please ensure you are connected to VPN and can access the internal portal, then try again.

## Authentication

The CLI uses OAuth with your organization's SSO provider. Tokens are stored at `~/.config/enterprise-search/tokens.json`.

**Auto-authentication:** Commands automatically trigger OAuth when needed — no need to run `auth login` first.

```bash
# Check token status
scripts/enterprise-search-cli auth status

# Force re-authentication (if token is stale)
scripts/enterprise-search-cli auth login --reauth

# Remove stored tokens
scripts/enterprise-search-cli auth logout
```

## Search documents

Search across all indexed sources (Google Drive, Confluence, Slack, Jira, GitHub, etc).

```bash
# Basic search
scripts/enterprise-search-cli search "onboarding guide"

# Filter by datasource
scripts/enterprise-search-cli search "PTO policy" --datasource confluence

# Limit results
scripts/enterprise-search-cli search "incident" --limit 5
```

**Datasource filters:** `gdrive`, `confluence`, `slack`, `wiki`, `jira`, `github`, `notion`

## Chat with AI

Get AI-synthesized answers with citations.

```bash
# Ask a question
scripts/enterprise-search-cli chat "What is the PTO policy?"

# Use a specific agent
scripts/enterprise-search-cli chat "question" --agent-id AGENT_ID
```

## Read document content

Fetch content from a document by ID (obtained from search results).

```bash
# Read first 100 lines
scripts/enterprise-search-cli read DOC_ID

# Read specific line range
scripts/enterprise-search-cli read DOC_ID --start 50 --end 150
```

## List AI agents

Find available AI agents/bots in the enterprise search platform.

```bash
# List all agents
scripts/enterprise-search-cli agents

# Search by name
scripts/enterprise-search-cli agents --name "HR Assistant"
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
| `Unable to retrieve client_id` | Connect to VPN and internal portal first |
| `Address already in use` | Kill process on the auth callback port: `lsof -ti :<PORT> \| xargs kill` |
