---
Skill name: notion
Skill description: Access Block's Notion workspace to read, search, create, and update pages and databases. Use when asked to fetch Notion pages, search Notion, query Notion databases, or interact with any Notion content.
---

# Notion

Access Block's internal Notion workspace via the Notion API MCP server.

## Setup (one-time)

1. Go to https://www.notion.so/profile/integrations and create an internal integration for the Square workspace
2. Copy the integration token (starts with `ntn_`)
3. Save it: `echo 'NOTION_TOKEN=ntn_YOUR_TOKEN' > ~/.secrets-notion`
4. In Notion, go to the **Access** tab of your integration settings and grant access to the pages/databases you need
5. Alternatively, on any Notion page, click `⋯` → **Connect to** → select your integration

## Capabilities

- **Search** pages and databases by title
- **Read** page content, properties, and blocks
- **Create** new pages and databases
- **Update** existing page content and properties
- **Query** databases with filters and sorts
- **Manage** comments on pages

## Usage Notes

- The MCP server exposes Notion API tools automatically
- When fetching a page by URL, extract the page ID from the URL (the 32-char hex string at the end)
- Database queries use `data_source_id` (not `database_id`)
- For page URLs like `https://www.notion.so/workspace/Page-Name-abc123def456`, the ID is `abc123def456`
