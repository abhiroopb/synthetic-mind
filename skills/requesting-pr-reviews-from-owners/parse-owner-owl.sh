#!/usr/bin/env bash
# Parses the owner-owl bot comment on the current PR.
# Outputs JSON with: pr_number, pr_url, pr_title, teams (with status, paths, slack_channels).
set -euo pipefail

PR_REF="${1:-}"  # optional: PR number or URL; defaults to current branch

# 1. Get PR metadata
PR_JSON=$(gh pr view $PR_REF --json number,url,title,comments 2>/dev/null) || {
  echo '{"error": "No PR found for the current branch."}' >&2
  exit 1
}

PR_NUMBER=$(echo "$PR_JSON" | jq -r '.number')
PR_URL=$(echo "$PR_JSON" | jq -r '.url')
PR_TITLE=$(echo "$PR_JSON" | jq -r '.title')

# 2. Extract the owner-owl comment body (last one, in case of updates)
OWL_COMMENT=$(echo "$PR_JSON" | jq -r '[.comments[] | select(.author.login == "owner-owl")] | last | .body // empty')

if [ -z "$OWL_COMMENT" ]; then
  echo '{"error": "No owner-owl comment found. The bot may not have commented yet."}' >&2
  exit 1
fi

# 3. Parse teams with approval status
# Each team appears as: <b>team-name</b> ✅ or <b>team-name</b> ❌
# We also grab the paths (<code>/path</code>) and slack channels from each <details> block.

# Use python for reliable HTML/text parsing
python3 - "$OWL_COMMENT" "$PR_NUMBER" "$PR_URL" "$PR_TITLE" <<'PYEOF'
import sys, re, json

comment = sys.argv[1]
pr_number = sys.argv[2]
pr_url = sys.argv[3]
pr_title = sys.argv[4]

# Split into <details> blocks
blocks = re.split(r'<details>', comment)

teams = []
all_channels = set()

for block in blocks[1:]:  # skip preamble before first <details>
    # Team name and status from <summary>
    m = re.search(r'<b>([^<]+)</b>\s*(✅|❌)', block)
    if not m:
        continue
    team_name = m.group(1).strip()
    approved = m.group(2) == '✅'

    # Paths: <code>/path/to/dir</code>
    paths = re.findall(r'<code>(/[^<]+)</code>', block)

    # Slack channels: [#channel-name](https://slack.com/app_redirect?channel=...)
    channels = re.findall(r'\[#([a-zA-Z0-9_-]+)\]\(https://slack\.com/app_redirect\?channel=[a-zA-Z0-9_-]+\)', block)
    channel_links = re.findall(r'\[#[a-zA-Z0-9_-]+\]\(https://slack\.com/app_redirect\?channel=[a-zA-Z0-9_-]+\)', block)

    for ch in channel_links:
        all_channels.add(ch)

    teams.append({
        "name": team_name,
        "approved": approved,
        "paths": paths,
        "slack_channels": channel_links,
    })

result = {
    "pr_number": int(pr_number),
    "pr_url": pr_url,
    "pr_title": pr_title,
    "teams": teams,
    "all_slack_channels": sorted(all_channels),
}

print(json.dumps(result, indent=2))
PYEOF
