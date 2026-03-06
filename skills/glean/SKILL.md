---
name: glean
description: "Search Glean enterprise knowledge, documents, and people directory. Use when asked to search company docs, find people, chat with Glean AI, or read documents from Glean."
metadata:
  author: abhiroop
  version: "1.0"
---

# Glean Skill

Search and interact with Block's internal knowledge base via the Glean MCP server.

## Prerequisites

- Connected to **WARP VPN**
- Logged in to **The Hub** (my.sqprod.co)

Authentication is handled automatically via OAuth (Block Okta). On first use, a browser window opens for login. Tokens are cached at `~/.config/goose/mcp-glean/tokens.json`.

## Available Tools

| Tool | Description |
|------|-------------|
| `search_block_knowledge_base` | Search across Confluence, Google Drive, Slack, Jira, GitHub, The Hub, and more. Supports datasource filters, date ranges, author/owner filters, and pagination. |
| `chat_with_block_knowledge_base` | Ask Glean's AI assistant questions grounded in Block's knowledge base. Supports custom agent IDs. |
| `read_documents_from_block_knowledge_base` | Read full or partial document content by document ID (from search results). Supports line ranges. |
| `fetch_agent_info` | List all available Glean agents or search by name to get agent IDs for chat. |

## Common Workflows

### Search company knowledge

Use `search_block_knowledge_base` with a query. Filter by datasource (e.g. `["Confluence", "Google Drive"]`), author, owner, or date range.

### Ask a question

Use `chat_with_block_knowledge_base` for conversational Q&A. For specialized agents, first call `fetch_agent_info` to get the agent ID, then pass it to chat.

### Read a document

After searching, use `read_documents_from_block_knowledge_base` with the document ID and optional line range to fetch content.

### Find a Glean agent

Use `fetch_agent_info` with a name to search, or without arguments to list all available agents.

## Datasource Filters

Available values for `datasources_filter`:
`Airtable`, `Coda`, `Confluence`, `Console Apps`, `Google Calendar`, `Github`, `Google Tools`, `Google Drive`, `Jira`, `The Hub`, `Notion`, `Looker`, `Slack`, `Videos`

## Troubleshooting

| Error | Solution |
|-------|----------|
| Unable to retrieve client_id | Connect to WARP VPN and log in to The Hub |
| Token expired | Re-run any Glean tool — OAuth will auto-refresh via browser |
| Authorization timeout | Ensure browser can reach `login.block.xyz` |
