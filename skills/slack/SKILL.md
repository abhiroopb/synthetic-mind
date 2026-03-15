---
Skill name: slack
Skill description: Interact with Slack workspaces and channels. Search messages, read channels, post messages, manage status, and more across multiple workspaces.
roles: [frontend]
---

# Slack Skill

Interact with Slack workspaces using a local Python CLI that wraps the internal `mcp_slack` package.

## CRITICAL: Auto-Authentication Flow

When any command returns `"error_type": "auth_required"`, run this single command:

```bash
{{SKILL_DIR}}/scripts/slack-cli auth callback --workspace default
```

This opens a browser with a simple web page where the user can:
1. Click a link to open Slack authorization
2. Paste their token into the form
3. Click "Save Token"

The page auto-closes on success and the command outputs the result as JSON.

Tell the user:
> "I've opened a browser page for Slack authentication. Please follow the steps there - click the authorization link, copy your token, and paste it into the form."

After auth succeeds, retry whatever command originally failed.

---

## Prerequisites

### Install uv (if needed)

```bash
which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Authenticate

```bash
{{SKILL_DIR}}/scripts/slack-cli auth login
```

This will:
1. Open the Slack OAuth page in your browser
2. After clicking "Allow", you'll see your token displayed
3. Copy and paste the token when prompted
4. Select your default workspace

Credentials are stored at `~/.config/slack-skill/credentials.json`.

Check status: `{{SKILL_DIR}}/scripts/slack-cli auth status`

---

## Quick Reference

All commands output JSON. Run from `{{SKILL_DIR}}/scripts`:

```bash
{{SKILL_DIR}}/scripts/slack-cli <command> [options]
```

### Workspace Selection

Every command accepts `--workspace` (or `-w`) to select which workspace to use:

Configure workspace aliases in your credentials file. Use `--workspace <alias>` to switch between them.

Examples:
```bash
{{SKILL_DIR}}/scripts/slack-cli list-channels --workspace my-workspace
{{SKILL_DIR}}/scripts/slack-cli search-messages -w another-workspace --query "incident"
```

---

## Authentication

```bash
# Interactive login (opens browser, prompts for token)
{{SKILL_DIR}}/scripts/slack-cli auth login

# Login without opening browser
{{SKILL_DIR}}/scripts/slack-cli auth login --no-browser

# Login with token directly
{{SKILL_DIR}}/scripts/slack-cli auth login --token "xoxp-..."

# Check auth status
{{SKILL_DIR}}/scripts/slack-cli auth status

# Remove credentials
{{SKILL_DIR}}/scripts/slack-cli auth logout
```

---

## Workspaces

```bash
# List configured workspaces
{{SKILL_DIR}}/scripts/slack-cli workspace list

# Set default workspace
{{SKILL_DIR}}/scripts/slack-cli workspace set-default myworkspace

# Add custom workspace alias
{{SKILL_DIR}}/scripts/slack-cli workspace add myteam T0XXXXXXXX
```

---

## Reading Messages

### Get Channel Messages

```bash
# By channel name
{{SKILL_DIR}}/scripts/slack-cli get-channel-messages --channel-name general --limit 20

# By channel ID
{{SKILL_DIR}}/scripts/slack-cli get-channel-messages --channel-id C123ABC456

# From a DM
{{SKILL_DIR}}/scripts/slack-cli get-channel-messages --dm-username johndoe

# Thread replies
{{SKILL_DIR}}/scripts/slack-cli get-channel-messages --channel-id C123 --thread-ts 1234567890.123456

# From a different workspace
{{SKILL_DIR}}/scripts/slack-cli get-channel-messages -w square --channel-name eng-help
```

### File Attachments

Messages with attached files include a `files` array with `id` and `name`. To download a file locally (e.g., for image analysis with `look_at`):

```bash
# Download by file ID
{{SKILL_DIR}}/scripts/slack-cli download-file --file-id F0AE4JL1SDS --output /tmp/screenshot.png
```

### Search Messages

```bash
# Basic search
{{SKILL_DIR}}/scripts/slack-cli search-messages --query "quarterly report"

# Search in specific channel
{{SKILL_DIR}}/scripts/slack-cli search-messages --query "deploy" --in-channel eng-releases

# Search from specific user
{{SKILL_DIR}}/scripts/slack-cli search-messages --query "oncall" --from-user johndoe

# Sort by time instead of relevance
{{SKILL_DIR}}/scripts/slack-cli search-messages --query "incident" --sort timestamp --sort-dir desc
```

---

## Channels

```bash
# List channels you're a member of
{{SKILL_DIR}}/scripts/slack-cli list-channels

# Filter by name
{{SKILL_DIR}}/scripts/slack-cli list-channels --name-filter "eng-"

# Include DMs
{{SKILL_DIR}}/scripts/slack-cli list-channels --types "public_channel,private_channel,im"

# Get channel info
{{SKILL_DIR}}/scripts/slack-cli get-channel-info --channel-name goose-slack-mcp
{{SKILL_DIR}}/scripts/slack-cli get-channel-info --channel-id C08G2DR1B40
```

---

## Users

```bash
# Get current user info
{{SKILL_DIR}}/scripts/slack-cli get-user-info

# By user ID
{{SKILL_DIR}}/scripts/slack-cli get-user-info --user-id U03PNTMGFQX

# By email
{{SKILL_DIR}}/scripts/slack-cli get-user-info --email johndoe@example.com

# By username
{{SKILL_DIR}}/scripts/slack-cli get-user-info --username johndoe

# By real name
{{SKILL_DIR}}/scripts/slack-cli get-user-info --real-name "John Doe"
```

---

## Posting Messages

```bash
# Post to channel by name
{{SKILL_DIR}}/scripts/slack-cli post-message --channel-name test-channel --text "Hello from CLI!"

# Post to channel by ID
{{SKILL_DIR}}/scripts/slack-cli post-message --channel-id C123ABC --text "Hello!"

# DM a user
{{SKILL_DIR}}/scripts/slack-cli post-message --dm-username johndoe --text "Hey!"

# Reply to a thread
{{SKILL_DIR}}/scripts/slack-cli post-message --channel-id C123 --thread-ts 1234567890.123 --text "Reply!"

# Message yourself
{{SKILL_DIR}}/scripts/slack-cli post-message --dm-myself --text "Note to self"
```

---

## Message Operations

```bash
# Get message reactions
{{SKILL_DIR}}/scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation get_message_reactions

# Add reaction
{{SKILL_DIR}}/scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation add_reaction --emoji thumbsup

# Remove reaction
{{SKILL_DIR}}/scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation remove_reaction --emoji thumbsup

# Get message info
{{SKILL_DIR}}/scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation get_message_info

# Update message
{{SKILL_DIR}}/scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation update_message --text "Updated text"

# Delete message
{{SKILL_DIR}}/scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation delete_message
```

---

## Status & Presence

```bash
# Set status
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation set_status \
  --status-text "In a meeting" --status-emoji ":calendar:"

# Clear status
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation clear_status

# Set presence
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation set_presence --presence away
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation set_presence --presence auto

# Enable Do Not Disturb
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation set_dnd --num-minutes 60

# Disable DND
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation end_dnd
```

---

## Misc Read Operations

```bash
# List all accessible workspaces
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation get_workspaces

# Get user profile
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation get_user_profile
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation get_user_profile --user-id U123

# Get presence
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation get_presence --user-id U123

# Get DND info
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation get_dnd_info

# List scheduled messages
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation list_scheduled_messages

# Get channel members
{{SKILL_DIR}}/scripts/slack-cli misc-read --operation get_channel_members --channel-id C123
```

---

## Channel Management

```bash
# Join a channel
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation join_channel --channel-id C123

# Leave a channel
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation leave_channel --channel-id C123

# Set channel topic
{{SKILL_DIR}}/scripts/slack-cli misc-write --operation set_channel_topic \
  --channel-id C123 --topic "New topic here"
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "SLACK_TOKEN environment variable not set" | Run `{{SKILL_DIR}}/scripts/slack-cli auth login` |
| "Forbidden" during OAuth | Ensure VPN is connected and authenticated |
| "missing_scope" errors | Re-run the OAuth flow to get updated scopes |
| "channel_not_found" | Try specifying `--workspace` to switch workspaces |
| Package resolution errors | Run the uv config setup from Prerequisites |

### Re-authenticate

If you encounter auth issues, re-run the OAuth flow:

```bash
{{SKILL_DIR}}/scripts/slack-cli auth login
```

The same token will be generated, but with any newly added scopes.

### Check your configuration

```bash
{{SKILL_DIR}}/scripts/slack-cli auth status
```

### Support

Questions? Check the project repository for support channels.
