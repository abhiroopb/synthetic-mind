---
Skill name: gmail
Skill description: Interact with Gmail for email management. Search, read, send, draft, and manage emails, labels, and filters.
---

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

## Key Patterns

- **Always preview drafts** in chat before sending. Never send without user confirmation.
- **Search defaults to Inbox.** Set `label: "all"` to search across all labels.
- **Pass `timezone`** on search and read calls when available (IANA format).
- **Reply drafts:** Use `draft_type: "reply"` with `reference_message_id`.
- **Batch reads:** `read_message` accepts multiple `message_ids` in one call.
- **Mark as read:** Use `modify_labels` with `labels_to_remove: ["UNREAD"]`.
