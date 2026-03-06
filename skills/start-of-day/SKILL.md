---
name: start-of-day
description: "Morning triage of Slack unreads, Gmail inbox, Google Calendar, and comments/notifications from Figma, Google Drive, Linear, and Notion. Presents each item with options to reply, mark as read, save for later, or accept/decline events. Use when asked to start the day, check inbox, morning triage, or catch up."
---

# Start of Day

Triage Slack, Gmail, Google Calendar, and comments/notifications from Figma, Google Drive, Linear, and Notion in one interactive session.

## Auto-Run on Session Start

This skill auto-triggers if it hasn't run in the past 12 hours. The timestamp file is `~/.config/start-of-day/last-run`.

After completing the full triage, write the current timestamp:

```bash
mkdir -p ~/.config/start-of-day && date -u +%Y-%m-%dT%H:%M:%SZ > ~/.config/start-of-day/last-run
```

## Overview

Run through five sections in order:
1. **💬 Slack Unreads** — Unread messages across workspaces with reply/read/save options
2. **📧 Gmail** — Unread inbox emails with reply/read/archive/save options
3. **📅 Google Calendar** — Today's schedule with conflict detection and accept/decline
4. **🔖 Slack Saved / Later Items** — Saved messages and reminders (uses `stars.list` + `reminders.list` APIs, falls back to screenshots for newer "Later" items)
5. **💬 Comments & Notifications** — Unresolved comments from Figma, Google Drive, Linear, and Notion

After presenting each section, pause and let the user act before moving to the next.

## Triage Flow: Auto-Draft Responses

**Do NOT ask "what would you like to do?" after presenting each section.** Instead, immediately start going through items one by one, proactively drafting responses for each:

1. **Show a summary** of all Slack, Gmail, and Calendar items as a numbered overview.
2. **Then go through each item sequentially**, starting with the most important (DMs, @mentions, priority channels, thread replies, then emails).
3. For each item:
   - Fetch the full message/thread context
   - Show the original message(s)
   - **Draft a response** (professional, friendly, concise — the user is a PM)
   - Ask with numbered options, each on its own line. For **Slack** items (no archive):
     - **(1) Send** — post the drafted reply
     - **(2) Edit** — let user modify the draft
     - **(3) Mark as Read**
     - **(4) Skip**
   - For **Email** items:
     - **(1) Send** — create Gmail draft reply
     - **(2) Edit** — let user modify
     - **(3) Mark as Read**
     - **(4) Archive**
     - **(5) Mark as Read & Archive**
     - **(6) Skip**
4. For bot/automated messages (GitHub, monitoring alerts, Slackbot reminders, Linear notifications, Google Docs comments), don't draft a reply — just show the applicable subset (Mark as Read, Archive if email, Skip)
5. For calendar events needing RSVP, present inline and ask: **Accept, Decline, Tentative, or Skip?**
6. Move to the next item automatically after each action.

This creates a fast inbox-zero flow where the user just approves/edits/skips each item in sequence.

---

## Section 1: Slack Unreads

### 1a. Fetch Unread Messages

**IMPORTANT**: The user may have thousands of channels across workspaces. DO NOT iterate through all channels — it will time out and get rate-limited. Use the bundled hybrid search script instead.

Run the `find-slack-unreads.py` script which uses a fast hybrid strategy:
1. Uses `search.messages` API to find recently active conversations (DMs, mentions, etc.)
2. Lists the first batch of group DMs (mpim)
3. Checks only those specific channels for unreads via `conversations.info`
4. Resolves display names for DMs and group DMs

```bash
uv run {{SKILL_DIR}}/scripts/find-slack-unreads.py workspace1 workspace2 workspace3
```

To scan only specific workspaces, pass them as arguments.

The output is JSON with this structure:
```json
{
  "ok": true,
  "total_unreads": 5,
  "total_channels": 4,
  "unreads": [
    {
      "channel_id": "D06CVPY5N57",
      "display_name": "Jane Doe",
      "is_im": true,
      "is_mpim": false,
      "is_channel": false,
      "unread_count": 1,
      "latest_text": "how are you holding up?",
      "latest_user_name": "Jane Doe",
      "workspace": "workspace1"
    }
  ]
}
```

For each unread conversation, fetch recent messages for preview:
```bash
your-slack-cli get-channel-messages \
  --channel-id <CHANNEL_ID> --workspace <WS> --limit 5
```

### 1b. Present Messages as an Inbox

Display unread Slack messages as a numbered list, grouped by workspace and channel/DM:

```
## 💬 Slack Unreads (5 messages across 2 workspaces)

### Workspace1 — #your-team-channel (2 unread)
1. **Sarah Kim** (2h ago): "Hey team, can someone review the PR for the new tip..."
2. **Mike Chen** (3h ago): "The staging deploy looks good, I tested the happy path..."

### Workspace1 — DM: Jane Doe (1 unread)
3. **Jane Doe** (1h ago): "Quick question about the redesign — are we still..."

### Workspace2 — #your-engineering-channel (2 unread)
4. **Bot: Monitoring** (30m ago): "[ALERT] Latency spike on your-service p99..."
5. **Alex Rivera** (1h ago): "Deployed the hotfix, monitoring now..."
```

### 1c. Ask for Action

> **Slack actions:**
> - **Reply** to a message (I'll draft a reply for you) — e.g., "reply to 3"
> - **Mark as read** — e.g., "mark 1-2, 4 as read" or "mark all as read"
> - **Save for later** — e.g., "save 3" (adds 🔖 reaction)
> - **Skip** — move on to Gmail

### 1d. Execute Slack Actions

#### Reply

1. Fetch full thread context using your Slack CLI
2. Draft a contextually appropriate reply (professional, friendly, concise).
3. Present draft and ask: **Send this?** (yes / edit / skip)
4. If "yes", post the reply using your Slack CLI
5. Mark channel as read

#### Mark as Read

Use your Slack CLI to mark the channel as read at the given message timestamp.

#### Save for Later

Use your Slack CLI to add a bookmark emoji reaction to the message.

---

## Section 2: Gmail

### 2a. Fetch All Inbox Emails

Fetch both unread and read emails in the inbox. Make two parallel calls:

```
mcp__gmail__search_tool(label="Inbox", only_is_unread=true, max_results=25, timezone="America/Los_Angeles")
mcp__gmail__search_tool(label="Inbox", only_is_read=true, max_results=20, timezone="America/Los_Angeles")
```

Combine results into a single list. Unread emails come first, then read emails. De-duplicate by message ID if any overlap.

### 2b. Present All Emails as a Numbered List

Display all inbox emails as a single numbered list, grouped by read status and then by importance. For each email show:

- **Index number** (restart at 1 for emails)
- **Sender** (name and email)
- **Subject**
- **Time** (human-readable relative time)
- **Snippet** (first ~100 chars)
- **Labels** (if any beyond Inbox)
- **🔵 Unread** or **Read** indicator

Categorize into sections:

```
## 📧 Gmail Inbox (12 emails — 3 unread, 9 read)

### 🔵 Unread
#### From People
1. 🔵 **Sarah Kim** <skim@example.com> (2h ago)
   "Re: Product redesign Q1 plan" — "Thanks for the updated timeline. One question about the..."

#### Automated / Notifications
2. 🔵 **GitHub** (1h ago) — "[your-org/your-repo] PR #4521 merged"
3. 🔵 **Monitoring** (3h ago) — "[ALERT] your-service latency p99 > 500ms"

### Read but Still in Inbox
#### From People
4. **External Contact** <contact@example.com> (2d ago)
   "Re: Feature not working" — "Login email: contact@example.com..."

#### Automated / Notifications
5. **Figma** (2d ago) — "2 new comments in Your Design File"
6. **Google Docs** (2d ago) — "Your Document: ... Someone replied"
```

### 2c. Present Each Email with Actions

Go through each email one at a time (unread first, then read). For each email:

1. Read the full email using `mcp__gmail__read_message_tool` with the message ID.
2. Show a summary of who sent it, what it's about, and the key content.
3. If it's a human-written email that warrants a reply, **proactively draft a reply** and present it.
4. Offer options for the email:

> **What do you want to do?**
> 1. **Send reply** (draft a reply)
> 2. **Mark as read** (only shown for unread emails)
> 3. **Archive** (remove from inbox)
> 4. **Save for later** (labels "1. To Do" + archives)
> 5. **Skip** (leave in inbox)

For bot/automated emails (GitHub, monitoring, Calendar invites, Figma notifications), skip the draft and just offer options 2–5.

### 2d. Execute Email Actions

#### Send Reply
1. Draft a contextually appropriate reply
2. Present in chat for review alongside the original message
3. After approval, create Gmail draft: `mcp__gmail__create_draft_tool`

#### Mark as Read
```
mcp__gmail__mark_as_read_tool(message_id=<ID>)
```

#### Archive
```
mcp__gmail__archive_tool(message_id=<ID>)
```

#### Save for Later
```
mcp__gmail__add_label_tool(message_id=<ID>, label="1. To Do")
mcp__gmail__archive_tool(message_id=<ID>)
```

---

## Section 3: Google Calendar

### 3a. Fetch Today's Events

```
mcp__gcal__list_events(calendarId="primary", timeMin=<today_start_iso>, timeMax=<today_end_iso>, timezone="America/Los_Angeles")
```

### 3b. Present Schedule

Display today's schedule as a timeline, flagging conflicts:

```
## 📅 Today's Schedule (7 events)

| Time | Event | Status |
|------|-------|--------|
| 9:00-9:30 | Standup | ✅ Accepted |
| 10:00-10:30 | 1:1 with Manager | ✅ Accepted |
| 10:30-11:00 | Design Review | ⚠️ Needs RSVP |
| 11:00-12:00 | ⚠️ CONFLICT: Sprint Planning + Customer Call | ❌ Overlap! |
| 1:00-2:00 | Lunch (blocked) | — |
| 2:00-3:00 | Engineering Sync | ✅ Accepted |
| 4:00-4:30 | New: Product Review | ⚠️ Needs RSVP |
```

### 3c. Ask for RSVP Actions

For events needing RSVP:
> **Event: Design Review (10:30-11:00)**
> - Organizer: Jane Doe
> - Description: "Review the latest mockups..."
>
> **(1) Accept  (2) Decline  (3) Tentative  (4) Skip**

### 3d. Execute Calendar Actions

```
mcp__gcal__respond_to_event(calendarId="primary", eventId=<ID>, response="accepted")
```

---

## Section 4: Slack Saved & Later Items

### 4a. Fetch Saved Items

```bash
uv run {{SKILL_DIR}}/scripts/find-slack-saved.py
```

This script calls `stars.list` and `reminders.list` and returns both in a combined JSON output.

### 4b. Present Items

Compile saved items and active (non-completed) reminders into a numbered list:

```
## 🔖 Slack Saved & Later Items (X items)

### Active Reminders
1. 🔔 **Reminder** (overdue by 3d) — "#your-team-channel: Can someone review the PR..." — from **Sarah Kim**
2. 🔔 **Reminder** (due today) — "DM: Follow up with Martin about..."

### Saved Messages
3. 🔖 **#your-engineering-channel** — "Offline payments edge case discussion..." — **Team Member** (saved 2d ago)
4. 🔖 **DM: Colleague** — "Link to the design doc..." (saved 1w ago)
```

### 4c. Ask for Action

> **Actions:**
> - **Complete reminder** — e.g., "complete 1-2"
> - **Unstar/unsave** — e.g., "unsave 3" (removes star)
> - **Reply via Slack** — e.g., "reply to 4"
> - **Skip** — move on

### 4d. Execute Actions

Use your Slack CLI to complete reminders, remove stars, or post replies.

---

## Section 5: Comments & Notifications

Fetch recent unresolved comments and notifications from Figma, Google Drive, Linear, and Notion. Run all four fetches **in parallel** since they are independent.

### 5a. Fetch Comments from All Sources

#### Figma Comments

Fetch comments from recently active Figma files. Use the user's Gmail to find recent Figma notification emails, then extract file keys:

```bash
FIGMA_TOKEN="$(cat ~/.config/figma/token 2>/dev/null)"
```

Search Gmail for recent Figma comment notifications to discover active files:
```
mcp__gmail__search_tool(from_sender="notifications@figma.com", newer_than_days=7, max_results=10, label="all", timezone="America/Los_Angeles")
```

Extract Figma file keys from the email subjects/bodies (format: `figma.com/design/<FILE_KEY>/...`), then fetch comments for each file:

```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/<FILE_KEY>/comments" | python3 -c "
import json, sys
data = json.load(sys.stdin)
comments = [c for c in data.get('comments', []) if not c.get('resolved_at')]
for c in comments:
    print(json.dumps({'id': c['id'], 'message': c['message'], 'user': c['user']['handle'], 'created': c['created_at'], 'file_key': '<FILE_KEY>'}))"
```

#### Google Drive Comments

Search for recently modified Google Docs/Sheets/Slides, then fetch unresolved comments using your Google Drive CLI.

Filter to show only **unresolved** comments (where `resolved` is false/null) from the last 7 days.

#### Linear Notifications

Fetch issues assigned to the user or where the user was mentioned recently:

```
mcp__linear__linear_getViewer()  → get the user's ID
mcp__linear__linear_searchIssues(assigneeId=<USER_ID>, limit=20)
```

For each issue, check for recent comments:
```
mcp__linear__linear_getComments(issueId=<ISSUE_ID>, limit=5)
```

Show comments from the last 7 days that were NOT authored by the user.

#### Notion Comments

For recent Notion pages the user is active on, use the Notion MCP to fetch discussions:

```
mcp__notion__notion_fetch(id=<PAGE_ID>, include_discussions=true)
```

Search Gmail for Notion comment notifications to discover pages with activity:
```
mcp__gmail__search_tool(from_sender="notify@notionmail.com", newer_than_days=7, max_results=10, label="all", timezone="America/Los_Angeles")
```

### 5b. Present Comments as a Numbered List

Group comments by source, then by file/issue. Show only unresolved/recent items:

```
## 💬 Comments & Notifications (12 items across 4 sources)

### 🎨 Figma (3 comments)
1. **Designer** in "Your Design File v3" (2h ago)
   "Can we move the selector above the total?" — node: Frame 42

### 📝 Google Docs (4 comments)
4. **Colleague** in "Your PRD" (1h ago)
   "Should we include the fallback behavior for offline?" — unresolved

### 🔷 Linear (3 notifications)
7. **Team Member** on PROJ-142 "Add feature buttons" (30m ago)
   "PR is ready for review — can you take a look at the API changes?"

### 📓 Notion (2 comments)
10. **Colleague** in "Your Roadmap" (1d ago)
    "Can we add the dependency on the other team?" — discussion://abc123
```

### 5c. Ask for Action

> **Comment actions:**
> - **Reply** to a comment — e.g., "reply to 4" (I'll draft a reply)
> - **Resolve** — e.g., "resolve 4-6" (marks Google Docs/Figma comments as resolved)
> - **Open** — e.g., "open 1" (opens the file/issue in browser)
> - **Skip** — move on

### 5d. Execute Comment Actions

#### Reply

1. Draft a contextually appropriate reply based on the comment thread.
2. Present draft and ask: **Send this?** (yes / edit / skip)
3. If "yes", post the reply via the appropriate API (Figma, Google Drive, Linear, or Notion).

#### Open

Open the source file/issue in the default browser:
```bash
open "https://www.figma.com/design/<FILE_KEY>?node-id=<NODE_ID>"
open "https://docs.google.com/document/d/<DOC_ID>"
open "https://linear.app/your-team/issue/<ISSUE_ID>"
open "https://www.notion.so/<PAGE_ID>"
```

---

## Important Notes

- **Numbering**: Each section uses its own numbering starting at 1.
- **Tone for drafts**: Professional but warm. Concise. The user is a PM.
- **Bot messages**: For bot/alert messages (monitoring, GitHub, PagerDuty, feature flags), suggest marking as read rather than replying.
- **Batch operations**: Parse ranges like "1-4" and comma-separated lists like "3, 7, 9".
- **Combined actions**: The user can say "accept 1, 3, decline 4, mark emails 3-5 as read".
- **Thread replies**: Always reply in-thread for Slack messages.
- **Gmail drafts**: Save as draft (not send directly) so the user can review before sending.
- **Email reply review**: When drafting email replies, always paste the exact original message received AND the full drafted response text in the chat so the user can review both side-by-side before opening Gmail.
- **Calendar conflicts**: Always flag overlapping events clearly with ⚠️.
- **Timezone**: Use `America/Los_Angeles` (Pacific) for all time displays.
