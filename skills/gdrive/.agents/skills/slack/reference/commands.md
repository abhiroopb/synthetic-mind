# Command reference

Additional commands beyond the basics covered in SKILL.md.

## Message operations

```bash
# Get message reactions
scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation get_message_reactions

# Add reaction
scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation add_reaction --emoji thumbsup

# Remove reaction
scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation remove_reaction --emoji thumbsup

# Get message info
scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation get_message_info

# Update message
scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation update_message --text "Updated text"

# Delete message
scripts/slack-cli message --channel-id C123 --message-ts 1234567890.123 \
  --operation delete_message
```

## Status & presence

```bash
# Set status
scripts/slack-cli misc-write --operation set_status \
  --status-text "In a meeting" --status-emoji ":calendar:"

# Clear status
scripts/slack-cli misc-write --operation clear_status

# Set presence
scripts/slack-cli misc-write --operation set_presence --presence away
scripts/slack-cli misc-write --operation set_presence --presence auto

# Enable Do Not Disturb
scripts/slack-cli misc-write --operation set_dnd --num-minutes 60

# Disable DND
scripts/slack-cli misc-write --operation end_dnd
```

## Misc read operations

```bash
# List all accessible workspaces
scripts/slack-cli misc-read --operation get_workspaces

# Get user profile
scripts/slack-cli misc-read --operation get_user_profile
scripts/slack-cli misc-read --operation get_user_profile --user-id U123

# Get presence
scripts/slack-cli misc-read --operation get_presence --user-id U123

# Get DND info
scripts/slack-cli misc-read --operation get_dnd_info

# List scheduled messages
scripts/slack-cli misc-read --operation list_scheduled_messages

# Get channel members
scripts/slack-cli misc-read --operation get_channel_members --channel-id C123
```

## Channel management

```bash
# Join a channel
scripts/slack-cli misc-write --operation join_channel --channel-id C123

# Leave a channel
scripts/slack-cli misc-write --operation leave_channel --channel-id C123

# Set channel topic
scripts/slack-cli misc-write --operation set_channel_topic \
  --channel-id C123 --topic "New topic here"
```

