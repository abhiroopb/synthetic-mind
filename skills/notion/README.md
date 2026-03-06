# Notion

> Read, search, create, and update Notion pages and databases.

## What it does

The Notion skill provides access to a Notion workspace via the Notion API MCP server. You can search pages and databases by title, read page content and properties, create new pages and databases, update existing content, query databases with filters and sorts, and manage comments. It handles URL-to-ID extraction and supports the full range of Notion API operations.

## Usage

Use this skill for any Notion interaction. Requires a Notion integration token configured in your environment.

**Trigger phrases:**
- "Search Notion for the release schedule"
- "Read this Notion page: [URL]"
- "Create a new Notion page in the project database"
- "Update the status on this Notion page"
- "Query the feature tracking database"

## Examples

- `"Search Notion for 'Q1 roadmap'"` — Searches pages and databases by title and returns matching results.
- `"Read this page: https://notion.so/workspace/Page-abc123"` — Extracts the page ID and fetches the full content.
- `"Query the release tracking database for items due this week"` — Runs a filtered database query with date-based filters.

## Why it was created

Notion contains critical project documentation, databases, and wikis. This skill enables seamless access to Notion content without leaving the agent workflow, making it easy to reference, update, and query information stored in Notion.
