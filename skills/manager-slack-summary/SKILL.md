---
name: manager-slack-summary
description: "Use when summarizing, digesting, recapping, reviewing, compiling, or generating a weekly summary of Slack conversations with your manager. Also use when updating, populating, or appending to a 1:1 Google Doc with conversation history. Searches DMs and shared channel threads, groups by topic, and writes formatted summaries."
argument-hint: "Optional: manager name or 'config' to set up"
references: [slack, gdrive]
---

# Manager Slack Summary

Weekly digest of all Slack conversations between you and your manager, written to a 1:1 Google Doc.

## Configuration

Manager details are stored in `~/.config/manager-slack-summary/config.json`:

```json
{
  "manager_name": "Jane Manager",
  "manager_short_name": "Jane",
  "manager_slack_id": "<manager-slack-id>",
  "manager_slack_display_name": "<manager-display-name>",
  "dm_channel_id": "<dm-channel-id>",
  "user_slack_id": "<your-slack-id>",
  "user_slack_display_name": "<your-display-name>",
  "user_short_name": "You",
  "google_doc_id": "<your-1-1-doc-id>",
  "google_doc_tab_id": "<tab-id>",
  "google_doc_title": "You/Jane 1:1"
}
```

### First-time setup (or changing managers)

If the config file doesn't exist, or the user says "config" / "set up" / provides a new manager name:

**Step 1: Ask for the manager's name**
> Who is your manager? (full name as it appears in Slack)

Also ask what short name to use in summaries.

**Step 2: Look up the manager in Slack**
Use the Slack user directory to find the manager by name. Confirm the match if multiple results. Then find the DM channel.

**Step 3: Ask for the 1:1 Google Doc**
> Paste the URL of your 1:1 Google Doc.
>
> ⚠️ **Important:** Create a dedicated tab in your 1:1 doc for AI summaries before proceeding. In Google Docs, click the **+** to add a new tab, name it "AI Summary", then share the URL with the tab selected.

Parse the doc ID and tab ID from the URL.

**Step 4: Look up your own Slack info**
Use the Slack user directory to find your own profile. Ask what short name to use.

**Step 5: Save config**
Write all values to `~/.config/manager-slack-summary/config.json`.

## When to Run

- **Automatically:** Every Friday morning as part of `start-of-day`
- **Manually:** When asked to summarize manager conversations or update the 1:1 doc

## Workflow

### 1. Determine date range

Calculate the Monday–Friday window for the current week.

### 2. Collect DM messages

Fetch all DM messages in the date range. Paginate if needed.

### 3. Search for shared channel/thread conversations

Search for messages where both people appear in the same thread. For each result in a non-DM channel, fetch the full thread. Only include threads where **both** people participated.

### 4. Deduplicate and organize

- Deduplicate messages by timestamp
- Group by conversation topic / thread
- Sort chronologically

### 5. Summarize

Write a concise summary organized by topic. For each topic:
- **Topic heading** (bold) — short descriptive label
- **Channel/context** — where the conversation happened (DM, #channel-name, thread)
- **Key points** — 2-5 bullet points capturing decisions, action items, updates, asks
- **Open items** — anything unresolved or needing follow-up

Keep summaries factual and concise. Use short names from config.

### 6. Write to Google Doc

Format the summary as markdown and insert at the **top** of the target tab (at index 1, so newest is first):

#### Markdown format

```markdown
## Week of <Month DD–DD, YYYY>

### Topic 1: <descriptive label>
*#channel-name / DM*
- Key point 1
- Key point 2
- Action item

### Topic 2: <descriptive label>
*DM*
- Summary point
- Decision made

---
```

Always end with `---` as a separator from previous weeks.

**Important:** After inserting, fix paragraph styles. The doc's default style may be TITLE, so restyle non-heading paragraphs to `NORMAL_TEXT`.

### 7. Confirm

Tell the user the summary was written with a count of conversations and topics. Include the doc link.

## Edge Cases

- **No conversations found:** Write a brief "No Slack conversations this week" entry
- **Rate limiting:** Add 3-second delays between API calls if rate-limited
- **Large threads:** Truncate individual threads to 50 messages max; summarize the rest
- **Config missing:** Run first-time setup interactively before proceeding
