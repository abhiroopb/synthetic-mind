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
4. For bot/automated messages (GitHub, Datadog, Slackbot reminders, Linear notifications, Google Docs comments), don't draft a reply — just show the applicable subset (Mark as Read, Archive if email, Skip)
5. For calendar events needing RSVP, present inline and ask: **Accept, Decline, Tentative, or Skip?**
6. Move to the next item automatically after each action.

This creates a fast inbox-zero flow where the user just approves/edits/skips each item in sequence.

---

## Section 1: Slack Unreads

### 1a. Fetch Unread Messages

**IMPORTANT**: The user has 14,000+ channels across workspaces. DO NOT iterate through all channels — it will time out and get rate-limited. Use the bundled hybrid search script instead.

Run the `find-slack-unreads.py` script which uses a fast hybrid strategy:
1. Uses `search.messages` API to find recently active conversations (DMs, mentions, etc.)
2. Lists the first batch of group DMs (mpim)
3. Checks only those specific channels for unreads via `conversations.info`
4. Resolves display names for DMs and group DMs

```bash
uv run /Users/abhiroop/.agents/skills/start-of-day/scripts/find-slack-unreads.py block square cashapp
```

To scan only specific workspaces, pass them as arguments (e.g., `block` only).

The output is JSON with this structure:
```json
{
  "ok": true,
  "total_unreads": 5,
  "total_channels": 4,
  "unreads": [
    {
      "channel_id": "D06CVPY5N57",
      "display_name": "Katie Chung",
      "is_im": true,
      "is_mpim": false,
      "is_channel": false,
      "unread_count": 1,
      "latest_text": "how are you holding up?",
      "latest_user_name": "Katie Chung",
      "workspace": "block"
    }
  ]
}
```

For each unread conversation, fetch recent messages for preview:
```bash
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli get-channel-messages \
  --channel-id <CHANNEL_ID> --workspace <WS> --limit 5
```

### 1b. Present Messages as an Inbox

Display unread Slack messages as a numbered list, grouped by workspace and channel/DM:

```
## 💬 Slack Unreads (5 messages across 2 workspaces)

### Block — #checkout-flow (2 unread)
1. **Sarah Kim** (2h ago): "Hey team, can someone review the PR for the new tip..."
2. **Mike Chen** (3h ago): "The staging deploy looks good, I tested the happy path..."

### Block — DM: Jane Doe (1 unread)
3. **Jane Doe** (1h ago): "Quick question about the checkout redesign — are we still..."

### Square — #pos-engineering (2 unread)
4. **Bot: Datadog** (30m ago): "[ALERT] Latency spike on checkout-service p99..."
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

1. Fetch full thread context:
   ```bash
   /Users/abhiroop/.agents/skills/slack/scripts/slack-cli get-channel-messages \
     --channel-id <CHANNEL_ID> --thread-ts <MESSAGE_TS> --limit 20 --workspace <WS>
   ```
2. Draft a contextually appropriate reply (professional, friendly, concise).
3. Present draft and ask: **Send this?** (yes / edit / skip)
4. If "yes", post:
   ```bash
   /Users/abhiroop/.agents/skills/slack/scripts/slack-cli post-message \
     --channel-id <CHANNEL_ID> --thread-ts <THREAD_TS> --text "<REPLY>" --workspace <WS>
   ```
5. Mark channel as read:
   ```bash
   /Users/abhiroop/.agents/skills/slack/scripts/slack-cli mark-channel-read \
     --channel-id <CHANNEL_ID> --ts <MESSAGE_TS> --workspace <WS>
   ```

#### Mark as Read

```bash
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli mark-channel-read \
  --channel-id <CHANNEL_ID> --ts <MESSAGE_TS> --workspace <WS>
```

#### Save for Later

```bash
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli message \
  --channel-id <CHANNEL_ID> --message-ts <MESSAGE_TS> \
  --operation add_reaction --emoji bookmark --workspace <WS>
```

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
1. 🔵 **Sarah Kim** <skim@squareup.com> (2h ago)
   "Re: Checkout redesign Q1 plan" — "Thanks for the updated timeline. One question about the..."

#### Automated / Notifications
2. 🔵 **GitHub** (1h ago) — "[squareup/ios-register] PR #4521 merged"
3. 🔵 **Datadog** (3h ago) — "[ALERT] checkout-service latency p99 > 500ms"

### Read but Still in Inbox
#### From People
4. **Mark McKinney** <mark@mckinney.net> (2d ago)
   "Re: [Cash Rounding] Cash rounding not working" — "Login email: mark@mckinney.net..."
5. **Aarohi Vohra** <aarohivohra09@g.ucla.edu> (3d ago)
   "Re: Student Interested in Product @ Square" — "My schedule just opened up..."

#### Automated / Notifications
6. **Figma** (2d ago) — "2 new comments in Onboarding & Activation [SOT & DEMO]"
7. **Google Docs** (2d ago) — "Pre-Auth Tipping: ... Andrea replied"
```

### 2c. Present Each Email with Actions

Go through each email one at a time (unread first, then read). For each email:

1. Read the full email using `mcp__gmail__read_message_tool` with the message ID.
2. Show a summary of who sent it, what it's about, and the key content.
3. If it's a human-written email that warrants a reply, **proactively draft a reply** and present it:
   > **From Sarah Kim — "Re: Checkout redesign Q1 plan"** 🔵
   > She's asking about the updated timeline for the first milestone...
   >
   > **Suggested reply:**
   > "Hey Sarah — good question. The updated timeline has the first milestone landing mid-March..."
4. Offer options for the email:

> **What do you want to do?**
> 1. **Send reply** (draft a reply)
> 2. **Mark as read** (only shown for unread emails)
> 3. **Archive** (remove from inbox)
> 4. **Save for later** (labels "1. To Do" + archives)
> 5. **Skip** (leave in inbox)

For bot/automated emails (GitHub, Datadog, Calendar invites, Figma notifications), skip the draft and just offer options 2–5.

### 2d. Execute Email Actions

#### Send Reply

1. Create the reply using `mcp__gmail__draft_tool` with `draft_type="reply"` and the `reference_message_id`.
2. Tell the user: "📝 Reply draft saved — open Gmail to review and hit send."
3. If unread, mark as read: `mcp__gmail__edit_message` with `labels_to_remove=["UNREAD"]`.

#### Mark as Read

```
mcp__gmail__edit_message(message_ids=[<IDs>], labels_to_remove=["UNREAD"])
```

#### Archive

```
mcp__gmail__edit_message(message_ids=[<IDs>], labels_to_remove=["INBOX"])
```

#### Save for Later

Apply the "1. To Do" label and archive in one call:

```
mcp__gmail__edit_message(message_ids=[<IDs>], labels_to_add=["1. To Do"], labels_to_remove=["INBOX"])
```

---

## Section 3: Google Calendar

### 3a. Fetch Today's Events

```bash
cd /Users/abhiroop/.agents/skills/gcal && uv run gcal-cli.py events list \
  --time-min <TODAY>T00:00:00-08:00 \
  --time-max <TOMORROW>T00:00:00-08:00 \
  --limit 50
```

Replace `<TODAY>` and `<TOMORROW>` with actual dates (e.g., `2026-02-28` and `2026-03-01`). Use the user's timezone `America/Los_Angeles`.

### 3b. Check Free/Busy for Conflicts

```bash
cd /Users/abhiroop/.agents/skills/gcal && uv run gcal-cli.py freebusy \
  --time-min <TODAY>T00:00:00-08:00 \
  --time-max <TOMORROW>T00:00:00-08:00 \
  --timezone "America/Los_Angeles"
```

### 3c. Present Events Needing RSVP — One at a Time

For events where the user's `responseStatus` is `needsAction`, present each one individually using the **reviewing-calendar** inline format. Show a 3-hour window before and after on the same day for context.

```
### 📩 {Event Title}
**{Optional/Required}** · {Day} · {start} – {end} ({duration}) · from **{organizer}**

**Your calendar around this time:**

\```
  {time}  {status_icon} {Event name}
          ·····························
 ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
 ┃  {time}  ⏳ {EVENT TITLE IN CAPS}                        ┃
 ┃           {duration} · {optional/required} · from {org}  ┃
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  {time}  🔶 {Conflicting event}       ← CONFLICT (overlaps Xm)
          ·····························
  {time}  {status_icon} {Event name}
\```

**Accept, Decline, Tentative, or Skip?**
```

Rules:
- **The target event** is inside a `┏━━━┓` box — visually prominent
- **Surrounding events** use status icons (✅ ❌ ❓ ⏳ 👤) but NO box
- **Conflicts** get 🔶 icon + `← CONFLICT (overlaps Xm)` annotation
- **Free gaps** shown as `·····························`
- **One event per message** — wait for user action before showing next
- For already-accepted events, just show a summary list (no individual triage needed)
- **Time to next meeting**: Always calculate the actual minutes/hours until the next upcoming meeting using the current system time (`date` command). Never guess or approximate — show the exact delta (e.g., "Your first meeting is in **21 minutes** at 9:05 AM").

### 3e. Ask for Action

> **Calendar actions:**
> - **Accept** — e.g., "accept 3, 5"
> - **Decline** — e.g., "decline 4" (I'll ask for an optional message)
> - **Tentative** — e.g., "tentative 3"
> - **Skip** — move on to Slack Past-Due

### 3f. Execute Calendar Actions

#### Accept

```bash
cd /Users/abhiroop/.agents/skills/gcal && uv run gcal-cli.py rsvp <EVENT_ID> --status accept
```

#### Decline

Ask: "Any message to include?" Then:

```bash
cd /Users/abhiroop/.agents/skills/gcal && uv run gcal-cli.py rsvp <EVENT_ID> --status decline --comment "<MESSAGE>"
```

#### Tentative

```bash
cd /Users/abhiroop/.agents/skills/gcal && uv run gcal-cli.py rsvp <EVENT_ID> --status tentative
```

Confirm: "✅ Accepted events 3, 5. ❌ Declined event 4."

---

## Section 4: Slack Saved / Later Items

Slack's "Later" tab includes starred/saved messages and reminders. Use the `stars.list` API for saved items and `reminders.list` for reminders.

### 4a. Fetch Saved Items & Reminders

Use the slack-cli to fetch both:

```bash
# Saved items (starred messages)
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli misc-read --workspace block --operation get_saved_items 2>/dev/null
```

If `misc-read` doesn't support saved items, use a direct API call via the script environment:
```bash
uv run /Users/abhiroop/.agents/skills/start-of-day/scripts/find-slack-saved.py
```

This script calls `stars.list` (team_id=T05HJ0CKWG5) and `reminders.list` (team_id=T05HJ0CKWG5) and returns both in a combined JSON output.

### 4b. Present Items

Compile saved items and active (non-completed) reminders into a numbered list:

```
## 🔖 Slack Saved & Later Items (X items)

### Active Reminders
1. 🔔 **Reminder** (overdue by 3d) — "#checkout-flow: Can someone review the PR..." — from **Sarah Kim**
2. 🔔 **Reminder** (due today) — "DM: Follow up with Martin about..."

### Saved Messages
3. 🔖 **#pos-engineering** — "Offline payments edge case discussion..." — **Blake McAnally** (saved 2d ago)
4. 🔖 **DM: Steph Grodin** — "Link to the design doc..." (saved 1w ago)
```

### 4c. Ask for Action

> **Actions:**
> - **Complete reminder** — e.g., "complete 1-2"
> - **Unstar/unsave** — e.g., "unsave 3" (removes star)
> - **Reply via Slack** — e.g., "reply to 4"
> - **Skip** — move on

### 4d. Execute Actions

For **completing reminders**:
```bash
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli misc-write --workspace block \
  --operation complete_reminder --reminder-id <REMINDER_ID>
```

For **unstarring messages** (removing from saved):
```bash
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli message \
  --channel-id <CHANNEL_ID> --message-ts <MESSAGE_TS> \
  --operation remove_star --workspace block
```

For **Slack replies**, use the slack-cli to post:
```bash
/Users/abhiroop/.agents/skills/slack/scripts/slack-cli post-message \
  --channel-id <CHANNEL_ID> --thread-ts <THREAD_TS> --text "<REPLY>" --workspace block
```

> **Note**: If the above API commands don't work for saved/later items (some require undocumented APIs), fall back to the screenshot approach: ask the user to screenshot `app.slack.com/client/E01BAFDEXUP/later` and use `look_at` to extract items.

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

Search for recently modified Google Docs/Sheets/Slides, then fetch unresolved comments:

```bash
# Find recently modified docs where the user was mentioned or commented
cd /Users/abhiroop/.agents/skills/gdrive && uv run gdrive-cli.py search "" --limit 20
```

Then for each file, fetch comments:
```bash
cd /Users/abhiroop/.agents/skills/gdrive && uv run gdrive-cli.py comments list <file-id>
```

Filter to show only **unresolved** comments (where `resolved` is false/null) from the last 7 days.

Alternatively, search Gmail for Google Docs comment notifications to discover files with activity:
```
mcp__gmail__search_tool(from_sender="comments-noreply@docs.google.com", newer_than_days=7, max_results=10, label="all", timezone="America/Los_Angeles")
```

Extract doc IDs from the notification emails, then fetch comments for those specific docs.

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

Show comments from the last 7 days that were NOT authored by the user (i.e., comments from others on the user's issues). Also search for issues where the user was @mentioned in recent comments.

#### Notion Comments

For recent Notion pages the user is active on, use the Notion MCP to fetch discussions:

```
mcp__notion__notion_fetch(id=<PAGE_ID>, include_discussions=true)
```

Search Gmail for Notion comment notifications to discover pages with activity:
```
mcp__gmail__search_tool(from_sender="notify@notionmail.com", newer_than_days=7, max_results=10, label="all", timezone="America/Los_Angeles")
```

Extract Notion page IDs from the notification emails, then fetch each page with `include_discussions=true`.

### 5b. Present Comments as a Numbered List

Group comments by source, then by file/issue. Show only unresolved/recent items:

```
## 💬 Comments & Notifications (12 items across 4 sources)

### 🎨 Figma (3 comments)
1. **Sarah Kim** in "Checkout Redesign v3" (2h ago)
   "Can we move the tip selector above the total?" — node: Frame 42
2. **Design Team** in "Checkout Redesign v3" (1d ago)
   "The spacing looks off on mobile — see attached screenshot"
3. **Alex Rivera** in "POS Settings Mockup" (3d ago)
   "Approved! One small note on the icon sizing..."

### 📝 Google Docs (4 comments)
4. **Andrea Lopez** in "Pre-Auth Tipping PRD" (1h ago)
   "Should we include the fallback behavior for offline?" — unresolved
5. **Mike Chen** in "Pre-Auth Tipping PRD" (3h ago)
   "The data section needs the Snowflake query link" — unresolved
6. **Jane Doe** in "Q1 OKRs" (2d ago)
   "@Abhi can you update the checkout milestone?" — unresolved

### 🔷 Linear (3 notifications)
7. **Blake McAnally** on CHKT-142 "Add tip percentage buttons" (30m ago)
   "PR is ready for review — can you take a look at the API changes?"
8. **Steph Grodin** on CHKT-138 "Checkout flow redesign" (1d ago)
   "Updated the acceptance criteria based on our sync"
9. **Bot: GitHub** on CHKT-145 "Fix rounding edge case" (2h ago)
   "PR #4521 merged to main"

### 📓 Notion (2 comments)
10. **Katie Chung** in "Checkout Flow Roadmap" (1d ago)
    "Can we add the dependency on the payments team?" — discussion://abc123
11. **Product Team** in "Sprint Review Notes" (3d ago)
    "Missing the demo link for the tipping feature"
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
3. If "yes", post the reply:

**Figma:**
```bash
curl -sH "X-Figma-Token: $FIGMA_TOKEN" -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "<REPLY>", "comment_id": "<PARENT_COMMENT_ID>"}' \
  "https://api.figma.com/v1/files/<FILE_KEY>/comments"
```

**Google Drive:**
```bash
cd /Users/abhiroop/.agents/skills/gdrive && uv run gdrive-cli.py comments reply <file-id> <comment-id> "<REPLY>"
```

**Linear:**
```
mcp__linear__linear_createComment(issueId=<ISSUE_ID>, body="<REPLY>", parentId=<PARENT_COMMENT_ID>)
```

**Notion:**
Use the Notion MCP `get_comments` tool to reply to a discussion thread.

#### Resolve (Google Docs & Figma only)

**Google Drive:** Mark comment as resolved via the Drive API (not currently in gdrive-cli — use the API directly or note for the user to resolve in-app).

**Figma:** Figma API doesn't support resolving comments programmatically — note for the user to resolve in Figma.

#### Open

Open the source file/issue in the default browser:
```bash
open "https://www.figma.com/design/<FILE_KEY>?node-id=<NODE_ID>"
open "https://docs.google.com/document/d/<DOC_ID>"
open "https://linear.app/square/issue/<ISSUE_ID>"
open "https://www.notion.so/<PAGE_ID>"
```

---

## Important Notes

- **Numbering**: Each section uses its own numbering starting at 1.
- **Tone for drafts**: Professional but warm. Concise. The user is a PM on the Checkout Flow team.
- **Bot messages**: For bot/alert messages (Datadog, GitHub, PagerDuty, LaunchDarkly), suggest marking as read rather than replying.
- **Batch operations**: Parse ranges like "1-4" and comma-separated lists like "3, 7, 9".
- **Combined actions**: The user can say "accept 1, 3, decline 4, mark emails 3-5 as read".
- **Thread replies**: Always use `--thread-ts` for Slack to reply in-thread.
- **Gmail drafts**: Save as draft (not send directly) so the user can review before sending.
- **Email reply review**: When drafting email replies, always paste the exact original message received AND the full drafted response text in the chat so the user can review both side-by-side before opening Gmail.
- **Calendar conflicts**: Always flag overlapping events clearly with ⚠️.
- **Timezone**: Use `America/Los_Angeles` (Pacific) for all time displays.
