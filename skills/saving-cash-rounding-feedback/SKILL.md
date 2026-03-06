---
name: saving-cash-rounding-feedback
description: Save cash rounding seller feedback to the tracking Google Doc. Looks up merchant token from Regulator and appends a row. Use when asked to save cash rounding feedback, log rounding feedback, or record seller feedback about cash rounding.
---

# Saving Cash Rounding Feedback

Appends seller feedback to the Cash Rounding Feedback tracking table in Google Docs.

## Target Document

- **Doc ID**: `1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE`
- **Tab ID**: `t.yg7h7jh60g59` (this is the **"Post-Launch" child tab** under "Seller feedback")
- **URL**: https://docs.google.com/document/d/1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE/edit?tab=t.yg7h7jh60g59
- **Important**: When using `docs get`, you MUST use `--include-tabs` to see child/sub-tabs. The Post-Launch tab is a child of the "Seller feedback" tab and won't appear in the top-level tab list. Use `find_tab` recursively through `childTabs`.

## Workflow

When the user says to save cash rounding feedback, follow these steps:

### Step 1: Identify the feedback source

The feedback can come from **two sources**:

#### Option A: Email
The user will provide (or you'll extract from the current context):
- The **feedback text** (verbatim, word for word — do NOT modify it)
- The **seller's email address**

If either is missing, ask the user.

#### Option B: Slack link
The user will provide a Slack message URL (e.g., `https://sq-block.slack.com/archives/CXXXXXX/pXXXXXXXXXX`).

1. Load the `slack` skill and read the message using `get-channel-messages` with the channel ID and thread timestamp extracted from the URL. Use `--full-text` to avoid truncation.
2. Extract the **feedback text** verbatim from the message.
3. If a merchant token (e.g., `MT: XXXXX` or similar) is mentioned in the message, extract it directly — skip the Regulator lookup in Step 2.
4. The **Source** column should be the raw Slack link (not "Email from ...").

### Step 2: Look up merchant token from Regulator

**Skip this step if the merchant token was already extracted from the Slack message.**

Search Regulator for the seller using their email address.

**Method 1: GraphQL omniSearch**

```bash
sq curl -s -X POST 'https://graphql-gateway.sqprod.co/graphql' \
  -H 'Content-Type: application/json' \
  -H 'apollographql-client-name: amp-regulator-skill' \
  -H 'apollographql-client-version: 1.0.0' \
  -d '{"query": "query { omniSearch(query: \"<EMAIL_ADDRESS>\") { merchantToken } }"}'
```

**Method 2: Regulator Advanced Search UI (fallback)**

If the API returns null, provide the user with the Regulator advanced search link so they can look it up manually:

```
https://regulator.sqprod.co/o/advanced-search?searchParams=%7B%22email%22%3A%22<URL_ENCODED_EMAIL>%22%7D&searchTarget=email
```

Note: The advanced search is a client-side UI and cannot be queried via API. Always try the API first, then provide the link.

Extract the `merchantToken` from the result. If no merchant is found, note "Not found" in the merchant token column, provide the Regulator search link, and inform the user.

### Step 3: Read the current document structure

Get the document structure to find the table and its indices:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py docs get 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE
```

Find the table in the tab `t.yg7h7jh60g59`. Identify:
- The table's element index
- The last row index (to insert after it)
- The cell start indices for each column

### Step 4: Add a new row to the table

Insert a new row at the bottom of the table:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py docs batch-update 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE \
  --requests '[{"insertTableRow": {"tableCellLocation": {"tableStartLocation": {"index": <TABLE_INDEX>}, "rowIndex": <LAST_ROW_INDEX>, "columnIndex": 0}, "insertBelow": true}}]'
```

### Step 5: Populate the new row cells

After inserting the row, re-read the doc structure to get updated indices, then populate the three columns:

1. **Column 1 — Feedback**: Copy/paste the feedback text **verbatim** (do not change anything)
2. **Column 2 — Merchant Token**: The merchant token from Regulator lookup
3. **Column 3 — Source**: "Email from <email_address>" (for emails) or the raw Slack link (for Slack messages)

Use batch-update with insertText requests to populate each cell:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py docs batch-update 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE \
  --requests '[
    {"insertText": {"location": {"index": <COL1_INDEX>}, "text": "<FEEDBACK_TEXT>"}},
    {"insertText": {"location": {"index": <COL2_INDEX>}, "text": "<MERCHANT_TOKEN>"}},
    {"insertText": {"location": {"index": <COL3_INDEX>}, "text": "<SOURCE>"}}
  ]'
```

**Important**: When inserting text into multiple cells in a single batch, process the cells in **reverse index order** (highest index first) so earlier insertions don't shift the indices of later ones.

### Step 6: Confirm

Tell the user:
> ✅ Saved feedback to the Cash Rounding tracking doc.
> - **Merchant token**: <token>
> - **Source**: <source (email or Slack link)>
> - **Doc**: [link to doc]

## Notes

- Always copy the feedback **word for word** — never summarize, clean up, or rephrase.
- If the Regulator lookup returns multiple merchants, list them and ask the user to confirm which one.
- The tab ID `t.yg7h7jh60g59` is important — make sure you're looking at the right tab when reading the doc structure.
