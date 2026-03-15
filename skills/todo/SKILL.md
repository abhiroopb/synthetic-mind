---
name: todo
description: "Persistent to-do list with proactive reminders. Auto-captures action items from start-of-day, emails, Slack, Linear, and manual input. Surfaces top items at session start and reminds on untouched high-priority items. Use when managing tasks, adding to-dos, checking the list, completing items, or snoozing reminders."
---

# To-Do List — Proactive Task Tracker

A persistent to-do system stored at `~/.config/amp/todo.json`. The user rarely checks a list manually — **proactive prompting is the core feature**.

## Data Schema

Each item in `items[]`:

```json
{
  "id": "uuid-v4",
  "title": "Short action description",
  "source": "Gmail | Slack | Linear | Notion | Figma | Google Docs | Calendar | manual",
  "source_ref": "optional link or ID for context",
  "priority": 2,
  "status": "open",
  "due": "2026-03-11T17:00:00Z",
  "snooze_until": null,
  "created_at": "2026-03-10T10:00:00Z",
  "completed_at": null,
  "context": "Short note or link for reference"
}
```

**Fields:**
- `id` — UUID v4, generated on creation
- `title` — concise action statement (start with a verb: "Reply to…", "Review…", "Follow up on…")
- `source` — where the item came from
- `source_ref` — URL, message ID, or issue ID for one-click context
- `priority` — 1=urgent, 2=high, 3=normal, 4=low
- `status` — `open`, `in-progress`, `done`, `snoozed`
- `due` — optional ISO 8601 datetime
- `snooze_until` — ISO 8601 datetime; item is hidden until this time
- `created_at` — ISO 8601 datetime
- `completed_at` — ISO 8601 datetime, set when status → done
- `context` — short description or link for quick reference

## Reading and Writing the To-Do List

Always use `python3` to read/write `~/.config/amp/todo.json`:

```bash
# Read all items
python3 -c "
import json
with open('$HOME/.config/amp/todo.json') as f:
    data = json.load(f)
print(json.dumps(data, indent=2))
"
```

```bash
# Add an item
python3 -c "
import json, uuid
from datetime import datetime, timezone
path = '$HOME/.config/amp/todo.json'
with open(path) as f:
    data = json.load(f)
item = {
    'id': str(uuid.uuid4()),
    'title': '<TITLE>',
    'source': '<SOURCE>',
    'source_ref': '<OPTIONAL_LINK>',
    'priority': 3,
    'status': 'open',
    'due': None,
    'snooze_until': None,
    'created_at': datetime.now(timezone.utc).isoformat(),
    'completed_at': None,
    'context': '<OPTIONAL_CONTEXT>'
}
data['items'].append(item)
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
print(f'✅ Added: {item[\"title\"]} (P{item[\"priority\"]})')
"
```

```bash
# Complete an item by ID
python3 -c "
import json
from datetime import datetime, timezone
path = '$HOME/.config/amp/todo.json'
with open(path) as f:
    data = json.load(f)
for item in data['items']:
    if item['id'] == '<ITEM_ID>':
        item['status'] = 'done'
        item['completed_at'] = datetime.now(timezone.utc).isoformat()
        print(f'✅ Done: {item[\"title\"]}')
        break
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
"
```

```bash
# Snooze an item
python3 -c "
import json
path = '$HOME/.config/amp/todo.json'
with open(path) as f:
    data = json.load(f)
for item in data['items']:
    if item['id'] == '<ITEM_ID>':
        item['status'] = 'snoozed'
        item['snooze_until'] = '<ISO_DATETIME>'
        print(f'😴 Snoozed: {item[\"title\"]} until <HUMAN_TIME>')
        break
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
"
```

```bash
# Delete an item by ID
python3 -c "
import json
path = '$HOME/.config/amp/todo.json'
with open(path) as f:
    data = json.load(f)
data['items'] = [i for i in data['items'] if i['id'] != '<ITEM_ID>']
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
print('🗑️ Deleted')
"
```

## Proactive Behaviors

### 1. Session Start — Surface Open Items

At the start of every session (after memory context injection), read the to-do list and present active items. This is the **most important behavior** — the user does not check the list themselves.

**Display format:**

```
## ✅ To-Do List (X open items)

1. 🔴 [P1] **Reply to Sarah's escalation email** — Gmail, 3h ago
2. 🟠 [P2] **Review PR #4521 for tip buttons** — GitHub, 1d ago
3. 🟡 [P3] **Update Q1 OKRs in Google Doc** — Google Docs, 2d ago
4. 🔵 [P4] **Read the new POS release notes** — Notion, 3d ago
5. 🟡 [P3] **Follow up with Andrea on pre-auth tipping** — Slack, 1d ago

> 📋 +4 more items (2 normal, 2 low priority)

**Actions:** Reply with a number to act — `1` = mark done, `2` = snooze, `3` = open context, or "show all"
```

**Rules:**
- Show top 5 items sorted by: priority (ascending) → due date (ascending, nulls last) → created_at (ascending)
- Summarize remaining items as: `+N more items (X high, Y normal, Z low)`
- Un-snooze items whose `snooze_until` has passed (set status back to `open`, clear `snooze_until`)
- Exclude items with status `done`
- Exclude items with `snooze_until` in the future

**Priority indicators:**
- P1 (urgent) = 🔴
- P2 (high) = 🟠
- P3 (normal) = 🟡
- P4 (low) = 🔵

### 2. Auto-Capture from Inputs

When processing **any** input source, automatically create to-do items for actionable items. **Do NOT ask for approval** — just create them silently and mention what was added at the end.

**Capture triggers:**
- **Start-of-day triage** — emails requiring reply, Slack messages needing response, PR reviews requested, unresolved comments. Create one to-do per actionable item that the user skips or saves for later.
- **Gmail** — emails from humans that require a reply or action. Not notifications/alerts.
- **Slack** — DMs or @mentions that ask a question or request something.
- **Linear** — issues assigned to the user, or comments requesting action.
- **Google Docs** — comments tagging the user or requesting review.
- **Figma** — comments requesting design feedback.
- **Notion** — comments or tasks assigned to the user.
- **Calendar** — events needing prep work (e.g., "prepare deck for X").

**Auto-capture rules:**
- Set priority based on signal: direct ask from a person = P2, FYI/review = P3, automated/bot = P4
- Escalate to P1 if: the word "urgent" or "ASAP" appears, or a manager/VP is the sender
- Set `source_ref` to the URL/ID of the original item for one-click navigation
- Deduplicate: before adding, check if a similar item already exists (same source_ref or very similar title)
- When items are auto-captured, mention at the end: `📌 Added 3 items to your to-do list`

### 3. After Completing Work

When the user completes an action that maps to an existing to-do item:
- Automatically find and mark the to-do item as `done`
- Show: `✅ Marked done: "Reply to Sarah's escalation email"`
- Remove from active display

### 4. Snooze Support

The user can snooze items with natural language:
- "snooze 2" → snooze item #2 for 2 hours (default)
- "snooze 2 for 4h" → snooze for 4 hours
- "snooze 2 until tomorrow" → snooze until 9am PT next day
- "snooze 2 until Monday" → snooze until 9am PT Monday
- "snooze all low" → snooze all P4 items for 24h

### 5. End-of-Session Reminder

Before the session ends (when the user seems done or says goodbye), check for untouched high-priority items:

```
⚠️ You still have 2 high-priority items open:
1. 🔴 [P1] Reply to Sarah's escalation email (3h ago)
2. 🟠 [P2] Review PR #4521 for tip buttons (1d ago)

Want to act on these before we wrap up?
```

### 6. Daily Digest (Part of Start-of-Day)

When the `start-of-day` skill runs, the to-do list should be surfaced as **Section 0** — before Slack, Gmail, Calendar, etc:

```
## ✅ To-Do List (8 open items)

### 🔴 Urgent / 🟠 High Priority
1. 🔴 [P1] **Reply to Sarah's escalation email** — Gmail, 3h ago
2. 🟠 [P2] **Review PR #4521 for tip buttons** — GitHub, 1d ago
3. 🟠 [P2] **Follow up with Blake on checkout redesign** — Slack, 2d ago

### 🟡 Normal
4. 🟡 [P3] **Update Q1 OKRs in Google Doc** — Google Docs, 2d ago
5. 🟡 [P3] **Follow up with Andrea on pre-auth tipping** — Slack, 1d ago

> 📋 +3 more items (1 normal, 2 low priority) — say "show all" to see them

---
After reviewing to-dos, continuing to Slack unreads...
```

After the triage surfaces new actionable items that the user skips, auto-capture them as to-do items.

## User Interaction Model

The user interacts with to-do items inline using numbers:

- **`1`** or **`done 1`** — mark item #1 as done
- **`snooze 2`** — snooze item #2 (default: 2 hours)
- **`snooze 2 until tomorrow`** — snooze with specific time
- **`open 3`** or **`3`** — show context / open source link
- **`show all`** — show all items including low priority
- **`add: <description>`** — manually add a to-do item (P3 by default)
- **`delete 4`** — remove an item
- **`prioritize 3 as P1`** — change priority

## Maintenance

- **Auto-archive:** Items marked `done` for more than 7 days are removed from the list on next session start.
- **Staleness alert:** Items older than 5 days without action get bumped up one priority level and flagged: `⏰ This item has been open for 5 days — still relevant?`
- **Max items:** If the list exceeds 25 open items, suggest a review: "You have 25+ open items — want to do a quick triage to close or snooze stale ones?"
