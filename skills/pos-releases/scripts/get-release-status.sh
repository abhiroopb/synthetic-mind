#!/bin/bash
# Fetches current POS release train status from Slack channels
# Usage: get-release-status.sh [ios|android|all] [days_back]

set -euo pipefail

SLACK_CLI="$HOME/.agents/skills/slack/scripts/slack-cli"
export POS_PLATFORM="${1:-all}"
export POS_DAYS_BACK="${2:-7}"

echo "=== POS Release Train Status (last ${POS_DAYS_BACK} days) ==="
echo ""

# Channel IDs (Square workspace)
# #pos-release-train: C02FFLH8H
# SQUID/X2/T2 updates channel: CAMTTU16D

echo "--- #pos-release-train (iOS + Android POS) ---"
"$SLACK_CLI" get-channel-messages -w square --channel-id C02FFLH8H --limit 30 | python3 -c "
import json, sys, os
from datetime import datetime, timedelta
data = json.load(sys.stdin)
msgs = data if isinstance(data, list) else data.get('messages', [])
days_back = int(os.environ.get('POS_DAYS_BACK', '7'))
platform = os.environ.get('POS_PLATFORM', 'all')
cutoff = datetime.now() - timedelta(days=days_back)
for m in msgs:
    ts = m.get('time', '')
    try:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        if dt < cutoff:
            continue
    except:
        pass
    text = m.get('text', '')
    if platform == 'all' or \
       (platform == 'ios' and ('ios' in text.lower() or 'apple' in text.lower() or 'testflight' in text.lower())) or \
       (platform == 'android' and ('android' in text.lower())):
        print(f'[{ts}] {text[:300]}')
        print()
"

echo ""
echo "--- #squid-release-train (SQUID/X2/T2) ---"
"$SLACK_CLI" get-channel-messages -w square --channel-id CAMTTU16D --limit 20 | python3 -c "
import json, sys, os
from datetime import datetime, timedelta
data = json.load(sys.stdin)
msgs = data if isinstance(data, list) else data.get('messages', [])
days_back = int(os.environ.get('POS_DAYS_BACK', '7'))
cutoff = datetime.now() - timedelta(days=days_back)
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
