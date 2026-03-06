# Gmail Skill

Interact with Gmail for email management. Search, read, send, draft, and manage emails, labels, and filters.

## MCP Server

This skill uses the `gmail` MCP server (`uvx mcp_gmail@latest`) configured in `~/.config/amp/settings.json`.

## Setup

### Prerequisites

1. **Google Cloud Project** with Gmail API enabled
2. **OAuth 2.0 credentials** (Desktop app type) from Google Cloud Console

### Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project → Enable the **Gmail API**
3. Go to "APIs & Services" → "Credentials" → "Create Credentials" → "OAuth client ID"
4. Choose "Desktop app" → Download the JSON credentials
5. Set the `GMAIL_OAUTH_CONFIG` env var in `~/.config/amp/settings.json` to the **stringified JSON** content of the downloaded credentials file

### First Run

On first use, the server opens a browser for Google OAuth authentication. After authorizing, the token is stored in the system keyring for future use.

## Available Tools

- **search_emails** — Search Gmail using Gmail search syntax (from:, to:, subject:, is:unread, has:attachment, etc.)
- **read_message** — Read full email content by message ID
- **send_email** — Send a new email
- **draft_email** — Create a draft email
- **modify_labels** — Add/remove labels on messages
- **list_labels** — List all Gmail labels
- **create_filter** / **list_filters** / **delete_filter** — Manage Gmail filters
