---
name: slack
description: Interact with Slack workspaces and channels. Search messages, read channels, post messages, manage status, and more across Block, Square, and Cash App workspaces.
roles: [frontend]
allowed-tools:
  - Bash(scripts/slack-cli:*)
  - Read(reference/**)
metadata:
  author: square
  version: "1.0"
  status: experimental
---

# Slack Skill

Interact with Slack workspaces using a local Python CLI that wraps the internal `mcp_slack` package.

## CRITICAL: Auto-authentication flow

When any command returns `"error_type": "auth_required"`, run this single command:

```bash
scripts/slack-cli auth callback --workspace block
```

This opens a browser with a simple web page where the user can:
1. Click a link to open Slack authorization (requires WARP VPN)
2. Paste their token into the form
3. Click "Save Token"

The page auto-closes on success and the command outputs the result as JSON.

Tell the user:
> "I've opened a browser page for Slack authentication. Please follow the steps there - click the authorization link, copy your token, and paste it into the form."

After auth succeeds, retry whatever command originally failed.

**Important**: The user must be connected to WARP VPN for the OAuth flow to work.

For first-time setup (uv installation, PyPI config, manual auth), see [SETUP.md](SETUP.md).

---

## Safety guidelines

- **ALWAYS confirm with the user** before posting messages, deleting messages,
  updating messages, or removing users from channels.
- **Never send DMs** to users unless the user explicitly requests it and
  specifies the recipient.
- **Never read** `~/.config/slack-skill/credentials.json` or attempt to access
  stored tokens. The CLI handles authentication internally.

---

## Calling `slack-cli`

In the examples below, `scripts/slack-cli` is relative to the skill's base directory. **Always invoke it using the absolute path**, e.g.:

```bash
/path/to/skill/scripts/slack-cli <command> [options]
```

Do NOT `cd` into the skill directory. Just prepend the base directory to `scripts/slack-cli`.

---

## Quick reference

All commands output JSON. 

### Workspace selection

Every command accepts `--workspace` (or `-w`) to select which workspace to use:

| Alias | Workspace ID | Description |
|-------|-------------|-------------|
| `block` | T05HJ0CKWG5 | Block (default) |
| `square` | T024FALR8 | Square |
| `cashapp` | T01H5TZGHUJ | Cash App |
| `tidal` | T0414TYF4 | Tidal |

Examples:
```bash
scripts/slack-cli list-channels --workspace square
scripts/slack-cli search-messages -w cashapp --query "incident"
```

---

## Authentication

```bash
# Interactive login (opens browser, prompts for token)
scripts/slack-cli auth login

# Login without opening browser
scripts/slack-cli auth login --no-browser

# Login with token directly
scripts/slack-cli auth login --token "xoxp-..."

# Check auth status
scripts/slack-cli auth status

# Remove credentials
scripts/slack-cli auth logout
```

---

## Workspaces

```bash
# List configured workspaces
scripts/slack-cli workspace list

# Set default workspace
scripts/slack-cli workspace set-default cashapp

# Add custom workspace alias
scripts/slack-cli workspace add myteam T0XXXXXXXX
```

---

## Reading messages

```bash
# By channel name
scripts/slack-cli get-channel-messages --channel-name general --limit 20

# By channel ID
scripts/slack-cli get-channel-messages --channel-id C123ABC456

# From a DM
scripts/slack-cli get-channel-messages --dm-username johndoe

# Thread replies
scripts/slack-cli get-channel-messages --channel-id C123 --thread-ts 1234567890.123456
```

### File attachments

Messages with attached files include a `files` array with `id` and `name`. To download a file locally (e.g., for image analysis with `look_at`):

```bash
scripts/slack-cli download-file --file-id F0AE4JL1SDS --output /tmp/screenshot.png
```

### Search messages

```bash
scripts/slack-cli search-messages --query "quarterly report"
scripts/slack-cli search-messages --query "deploy" --in-channel eng-releases
scripts/slack-cli search-messages --query "oncall" --from-user johndoe
scripts/slack-cli search-messages --query "incident" --sort timestamp --sort-dir desc
```

---

## Channels

```bash
scripts/slack-cli list-channels
scripts/slack-cli list-channels --name-filter "eng-"
scripts/slack-cli list-channels --types "public_channel,private_channel,im"
scripts/slack-cli get-channel-info --channel-name goose-slack-mcp
scripts/slack-cli get-channel-info --channel-id C08G2DR1B40
```

---

## Users

```bash
scripts/slack-cli get-user-info
scripts/slack-cli get-user-info --user-id U03PNTMGFQX
scripts/slack-cli get-user-info --email johndoe@squareup.com
scripts/slack-cli get-user-info --username johndoe
```

---

## Posting messages

The `post-message` command accepts a `--format` option. Choose based on what you need:

- **`markdown`** (default) — use for most messages. Supports bold, italic, links, lists, code blocks, and blockquotes. Just write standard Markdown.
- **`mrkdwn`** — use only when you need Slack-specific syntax like user mentions (`<@U123>`), channel links (`<#C123>`), or emoji shortcodes that standard Markdown can't express.
- **`json`** — use when you need tables, headers, two-column field layouts, or other structured layouts that Markdown can't express. Read [reference/block-kit.md](reference/block-kit.md) before constructing Block Kit JSON.

For the full syntax of each format, see [reference/message-formatting.md](reference/message-formatting.md).

```bash
# Markdown (default)
scripts/slack-cli post-message --channel-name test-channel \
  "Hello **world**, see [docs](https://example.com)"

# DM a user
scripts/slack-cli post-message --dm-username johndoe "Hey!"

# Reply to a thread
scripts/slack-cli post-message --channel-id C123 --thread-ts 1234567890.123 "Reply!"

# Message yourself
scripts/slack-cli post-message --dm-myself "Note to self"

# Slack mrkdwn format
scripts/slack-cli post-message --format mrkdwn "*bold* and _italic_"

# Block Kit JSON
scripts/slack-cli post-message --channel-name test-channel \
  --format json '[{"type":"header","text":{"type":"plain_text","text":"Report"}}]'
```

---

## More commands

For message operations (reactions, updates, deletes), status/presence,
and channel management, see [reference/commands.md](reference/commands.md).

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "SLACK_TOKEN environment variable not set" | Run `scripts/slack-cli auth login` |
| "Forbidden" during OAuth | Ensure WARP VPN is connected and authenticated |
| "missing_scope" errors | Re-run the OAuth flow to get updated scopes |
| "channel_not_found" | Try specifying `--workspace` to switch workspaces |
| Package resolution errors | Run the uv config setup from [SETUP.md](SETUP.md) |

### Re-authenticate

If you encounter auth issues, re-run the OAuth flow:

```bash
scripts/slack-cli auth login
```

The same token will be generated, but with any newly added scopes.

### Check your configuration

```bash
scripts/slack-cli auth status
```

### Support

Questions? Reach out in [#goose-slack-mcp](https://square.enterprise.slack.com/archives/C08G2DR1B40).
