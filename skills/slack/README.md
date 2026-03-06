# Slack

> Interact with Slack workspaces — search messages, read channels, post messages, manage status, and more.

## What it does

The Slack skill provides a comprehensive CLI for interacting with Slack across multiple workspaces. You can search messages, read channel history and threads, post messages and replies, manage DMs, download file attachments, set status and presence, manage Do Not Disturb, join/leave channels, and look up user information. All commands output JSON and support workspace selection for multi-workspace environments.

## Usage

Invoke when you need to interact with Slack — searching for messages, reading channels, posting messages, checking DMs, or managing your status. Supports multiple workspaces via the `--workspace` flag.

**Trigger phrases:**
- "Search Slack for..."
- "Read messages in #channel-name"
- "Post a message to #channel"
- "Set my Slack status"
- "Check my DMs"

## Examples

- `"Search Slack for 'quarterly report' in the engineering workspace"`
- `"Read the last 20 messages in #general"`
- `"DM johndoe saying 'Hey, quick question about the PR'"`

## Why it was created

Slack is a primary communication hub, but switching between the agent and Slack breaks flow. This skill brings full Slack functionality into the agent workflow — reading, searching, posting, and managing status without leaving the terminal.
