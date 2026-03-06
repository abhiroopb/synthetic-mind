#!/bin/bash
# Fetches current POS release train status from Slack channels
# Usage: get-release-status.sh [ios|android|all] [days_back]

SLACK_CLI="$HOME/.agents/skills/slack/scripts/slack-cli"
PLATFORM="${1:-all}"
DAYS_BACK="${2:-7}"

echo "=== POS Release Train Status (last ${DAYS_BACK} days) ==="
echo ""

# Channel IDs (Brand A workspace)
# #pos-release-train: YOUR_CHANNEL_ID_1
# SQUID/X2/T2 updates channel: YOUR_CHANNEL_ID_2

echo "--- #pos-release-train (iOS + Android POS) ---"
"$SLACK_CLI" get-channel-messages -w square --channel-id YOUR_CHANNEL_ID_1 --limit 30 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
msgs = data if isinstance(data, list) else data.get('messages', [])
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=${DAYS_BACK})
for m in msgs:
    ts = m.get('time', '')
    try:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        if dt < cutoff:
            continue
    except:
        pass
    text = m.get('text', '')
    platform = '${PLATFORM}'
    if platform == 'all' or \
       (platform == 'ios' and ('ios' in text.lower() or 'apple' in text.lower() or 'testflight' in text.lower())) or \
       (platform == 'android' and ('android' in text.lower())):
        print(f'[{ts}] {text[:300]}')
        print()
"

echo ""
echo "--- #squid-release-train (SQUID/X2/T2) ---"
"$SLACK_CLI" get-channel-messages -w square --channel-id YOUR_CHANNEL_ID_2 --limit 20 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
msgs = data if isinstance(data, list) else data.get('messages', [])
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=${DAYS_BACK})
for m in msgs:
    ts = m.get('time', '')
    try:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        if dt < cutoff:
            continue
    except:
        pass
    text = m.get('text', '')
    print(f'[{ts}] {text[:300]}')
    print()
"
