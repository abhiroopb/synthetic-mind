---
Skill name: saving-cash-rounding-feedback
Skill description: Save customer feedback to a tracking Google Doc. Looks up account token from the account lookup tool and appends a row. Use when asked to save feedback, log feedback, or record customer feedback about a feature.
---

# Saving Customer Feedback

Appends customer feedback to a tracking table in Google Docs.

## Target Document

- **Doc ID**: `<YOUR_DOC_ID>`
- **Tab ID**: `<YOUR_TAB_ID>` (the feedback tracking tab)
- **URL**: `https://docs.google.com/document/d/<YOUR_DOC_ID>/edit?tab=<YOUR_TAB_ID>`
- **Important**: When using `docs get`, you MUST use `--include-tabs` to see child/sub-tabs.

## Workflow

When the user says to save feedback, follow these steps:

### Step 1: Identify the feedback source

The feedback can come from **two sources**:

#### Option A: Email
The user will provide (or you'll extract from the current context):
- The **feedback text** (verbatim, word for word — do NOT modify it)
- The **customer's email address**

If either is missing, ask the user.

#### Option B: Slack link
The user will provide a Slack message URL.

1. Load the `slack` skill and read the message using `get-channel-messages` with the channel ID and thread timestamp extracted from the URL. Use `--full-text` to avoid truncation.
2. Extract the **feedback text** verbatim from the message.
3. If an account token is mentioned in the message, extract it directly — skip the lookup in Step 2.
4. The **Source** column should be the raw Slack link.

### Step 2: Look up account token

**Skip this step if the account token was already extracted from the Slack message.**

Search the account lookup tool for the customer using their email address.

**Method 1: GraphQL omniSearch**

```bash
curl -s -X POST 'https://graphql-gateway.example.com/graphql' \
  -H 'Content-Type: application/json' \
  -H 'apollographql-client-name: agent-feedback-skill' \
  -H 'apollographql-client-version: 1.0.0' \
  -d '{"query": "query { omniSearch(query: \"<EMAIL_ADDRESS>\") { merchantToken } }"}'
```

**Method 2: Advanced Search UI (fallback)**

If the API returns null, provide the user with the advanced search link so they can look it up manually.

Extract the `merchantToken` from the result. If no account is found, note "Not found" and inform the user.

### Step 3: Read the current document structure

Get the document structure to find the table and its indices:

```bash
cd {{GDRIVE_SKILL_DIR}} && uv run gdrive-cli.py docs get <DOC_ID>
```

Find the table in the target tab. Identify the table's element index and last row index.

### Step 4: Add a new row to the table

Insert a new row at the bottom of the table using the Google Docs batch-update API.

### Step 5: Populate the new row cells

After inserting the row, re-read the doc structure to get updated indices, then populate the three columns:

1. **Column 1 — Feedback**: Copy/paste the feedback text **verbatim**
2. **Column 2 — Account Token**: The account token from lookup
3. **Column 3 — Source**: "Email from <email_address>" (for emails) or the raw Slack link (for Slack messages)

**Important**: When inserting text into multiple cells in a single batch, process the cells in **reverse index order** (highest index first).

### Step 6: Confirm

Tell the user:
> ✅ Saved feedback to the tracking doc.
> - **Account token**: <token>
> - **Source**: <source>
> - **Doc**: [link to doc]

## Notes

- Always copy the feedback **word for word** — never summarize, clean up, or rephrase.
- If the lookup returns multiple accounts, list them and ask the user to confirm which one.
