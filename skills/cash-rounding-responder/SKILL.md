---
name: cash-rounding-responder
description: "Triages and drafts replies to cash-rounding@squareup.com emails since last run. Use when asked to respond to cash rounding emails, triage cash rounding inbox, or handle penny elimination requests."
---

# Cash Rounding Email Responder

Automatically triages new emails to `cash-rounding@squareup.com`, drafts context-aware replies using the penny elimination doc, and lets the user approve/edit/skip each draft before sending.

## State File

Track when the skill was last run using:

```
~/.cash-rounding-last-run
```

- On first run (file doesn't exist), default to **7 days ago**.
- Read the ISO date from the file to determine the `after:` search boundary.
- **Update the file with the current date/time at the very end**, after all drafts are processed.

## Workflow

### Step 1 — Determine time window

1. Check if `~/.cash-rounding-last-run` exists.
   - If yes, read the ISO date from it (e.g., `2026-02-28`).
   - If no, use 7 days ago as the default.
2. Tell the user the time window being searched.

### Step 2 — Fetch the seller-facing response template

Read the **"Overview"** tab from the penny elimination doc for the approved seller-facing response:

```
Doc ID: 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE
Tab ID: t.eoei3otto5gk
```

Use the gdrive skill to read this tab:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py read 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE --tab t.eoei3otto5gk
```

Extract the seller-facing response block (after the ⭐ marker). This is the approved template to base replies on.

### Step 3 — Search for new emails

Search Gmail for emails to `cash-rounding@squareup.com` after the last-run date:

- Use `label: all` to catch everything (inbox, forums, etc.)
- Use the `after:` date from Step 1
- Exclude emails **sent by the user** (from: abhiroop@squareup.com) — we only want inbound seller emails

### Step 4 — Filter out already-replied emails

For each inbound email found:

1. Read the full message to get the thread context.
2. Search for replies in the same thread (by subject or thread). If the user (abhiroop@squareup.com) has already replied, **skip** that email and note it as "already handled."

### Step 5 — Classify and draft responses

For each **unreplied** email, carefully read the full message and classify it into one of these categories. **Pay close attention to context clues** — don't just pattern-match keywords. Understand what the seller is actually asking for.

| Category | Signals | Draft approach |
|----------|---------|----------------|
| **Activation request** | Seller does NOT have cash rounding yet and wants to enable it ("enable", "turn on", "opt in", "activate", "join beta") | Use this standard activation response: "You can add yourself by going to this link: https://app.squareup.com/dashboard/early-feature-access. And you can learn more about the feature here: https://squareup.com/help/us/en/article/8595-beta-set-up-cash-rounding" |
| **Troubleshooting — version issue** | "not working", "failure", "doesn't show", app version mentioned and < 6.94 | Tell them to update to at least v6.94. |
| **Troubleshooting — already enabled** | Seller clearly already has cash rounding enabled but is experiencing issues (e.g., report discrepancies, rounding not appearing correctly) | Ask for specifics — screenshots, examples, device/app details. Do NOT tell them to enable via Early Feature Access since they already have it. |
| **Feature request** | "round up only", "nearest dime", custom rounding behavior | Acknowledge the request, explain current behavior (rounds to nearest $0.05 symmetrically), note it's not possible at the moment. |
| **General inquiry** | Broad questions about cash rounding, how it works, wanting more info before enabling | Use the seller-facing response template and direct to Early Feature Access. |
| **Other / unclear** | Doesn't fit above categories, missing critical details | Flag for manual review — do NOT auto-draft. |

#### Drafting guidelines

- **Read the email carefully.** If the seller mentions issues with an already-enabled feature (e.g., "end of day reports conflicting", "rounding not reflecting"), do NOT suggest enabling — they already have it. Instead, ask clarifying questions (screenshots, examples).
- **Be concise and relevant.** Only include information that directly addresses what the seller asked about. Don't add boilerplate about legislation or the beta unless the seller is asking to join.
- **Ask for details when troubleshooting.** Request screenshots, app version, device info, or specific examples of the problem.

### Step 6 — Present drafts to user

For **each** email, present a summary block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email X of Y
From: [sender name] <[sender email]>
Date: [date]
Subject: [subject]
Category: [classification]

📝 Original message (summary):
[1-2 line summary of what the seller asked]

✉️ Proposed draft:
[full draft reply text]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then present numbered options on separate lines so the user can reply with just a number:

> **1** — Send (create reply draft in Gmail)
> **2** — Edit (modify text, then create draft)
> **3** — Skip (move on)

Process emails **one at a time** so the user can make decisions sequentially.

### Step 7 — Update last-run timestamp

After all emails are processed, write the current date to the state file:

```bash
date -u +"%Y-%m-%d" > ~/.cash-rounding-last-run
```

### Step 8 — Summary

Print a final summary:

```
✅ Cash Rounding Triage Complete
   Emails found: X
   Already replied: X
   Drafts created: X
   Skipped: X
   Flagged for manual review: X
```

## Important Notes

- **Never auto-send** — always create Gmail drafts, never send directly.
- **Always use the reply draft type** so the response threads correctly.
- **Sign off as "Abhi"** in all drafts.
- If the doc fetch fails, fall back to the standard response: direct sellers to `https://app.squareup.com/dashboard/early-feature-access`.
