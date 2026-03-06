---
Skill name: logging-feature-requests
Skill description: Digest feature requests from Slack links and log them to a Feature Requests Google Sheet. Use when pasting a Slack thread link to capture a feature request, or asked to log/record a feature request.
---

# Log Feature Request from Slack

Extracts feature requirements from a Slack thread and appends a summarized row to the **Feature Requests** tab of the tracking spreadsheet.

## Trigger

Activate when the user pastes a Slack message link (e.g. `https://workspace.slack.com/archives/CXXXX/pXXXX`).

## Workflow

### 1. Parse the Slack link

Extract `channel_id` and `thread_ts` from the URL:
- URL format: `https://workspace.slack.com/archives/<channel_id>/p<thread_ts_without_dot>`
- Convert the `p` timestamp: insert a `.` before the last 6 digits (e.g. `p1772059905598279` → `1772059905.598279`)

### 2. Fetch the Slack thread

```bash
{{SLACK_SKILL_DIR}}/scripts/slack-cli get-channel-messages --channel-id <channel_id> --thread-ts <thread_ts> --limit 100
```

Also resolve user IDs to real names using:
```bash
{{SLACK_SKILL_DIR}}/scripts/slack-cli get-user-info --user-id <user_id>
```

### 3. Digest and summarize

From the full thread, extract:

| Column | How to derive |
|---|---|
| **Feature** | Short, descriptive name for the feature request (≤ 10 words) |
| **Priority** | Infer from context: `P0` = urgent/blocking deals, `P1` = high demand from multiple customers, `P2` = clear value but not urgent, `P3` = nice-to-have or exploratory. Use your judgment based on the thread's tone, urgency, and business impact. |
| **Product Area** | Categorize into one of your defined product areas (e.g., `Payment Processing`, `Settings`, `UX`, `Receipts`, `Offline`, or `Other`) |
| **Detailed Description** | 2-4 sentence summary of the request, the business rationale, and any key constraints or nuances discussed in the thread |
| **Source** | The original Slack link pasted by the user |
| **Requester** | Infer from context: `Internal feedback` if from employees, `Customer feedback` if from customers/sales/AM channels, `UXR` if from user research. Use your judgment based on who started the thread and the channel context. |
| **Status** | `Needs triage` |
| **Notes** | Any additional context worth capturing (e.g. related features, competitive context, regulatory considerations). Leave blank if nothing notable. |

### 4. Confirm with user

Before writing to the sheet, present the row in a table and ask:
> "Here's what I'll add to the Feature Requests sheet. Want me to go ahead, or make any changes?"

### 5. Append to sheet

Once confirmed, append the row using the Google Sheets API or gdrive skill:

```bash
cd {{GDRIVE_SKILL_DIR}} && uv run gdrive-cli.py sheets append <SPREADSHEET_ID> \
  --range "'Feature Requests'" \
  --values '[["<Feature>", "<Priority>", "<Product Area>", "<Detailed Description>", "<Source>", "<Requester>", "<Status>", "<Notes>"]]'
```

### 6. Confirm

After appending, tell the user the row was added and link to the sheet.
