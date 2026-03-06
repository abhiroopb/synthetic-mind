# Gather Context from Slack

Load when the user provides Slack channel(s) or thread URLs as input.

## Search for Feature Discussions

Use the `slack` skill to search for feature-related discussions:
```bash
cd ~/.claude/skills/slack/scripts && ./slack-cli search-messages --query "<feature name or flag>" --in-channel <channel-name>
```

For thread URLs, extract the channel ID and thread timestamp, then fetch the thread:
```bash
cd ~/.claude/skills/slack/scripts && ./slack-cli get-channel-messages --channel-id <channel-id> --thread-ts <thread-ts>
```

## What to Extract

- Edge cases and known limitations engineers discussed but didn't put in formal docs
- Design decisions and trade-offs that inform test scenarios
- Previously reported bugs that should be regression-tested

Use these to supplement test scenarios — especially for the Special Conditions section (Part 7).
