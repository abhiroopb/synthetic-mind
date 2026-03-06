---
name: email-triage-responder
description: "Triages and drafts replies to a shared team inbox emails since last run. Use when asked to respond to team inbox emails, triage shared inbox, or handle recurring customer requests."
---

# Email Triage Responder

Automatically triages new emails to a shared team inbox, drafts context-aware replies using an approved response template, and lets the user approve/edit/skip each draft before sending.

## State File

Track when the skill was last run using:

```
~/.email-triage-last-run
```

- On first run (file doesn't exist), default to **7 days ago**.
- Read the ISO date from the file to determine the `after:` search boundary.
- **Update the file with the current date/time at the very end**, after all drafts are processed.

## Workflow

### Step 1 — Determine time window

1. Check if `~/.email-triage-last-run` exists.
   - If yes, read the ISO date from it (e.g., `2026-02-28`).
   - If no, use 7 days ago as the default.
2. Tell the user the time window being searched.

### Step 2 — Fetch the response template

Read the approved response template from a shared document:

```
Doc ID: <your-google-doc-id>
Tab ID: <your-tab-id>
```

Use the gdrive skill to read this tab:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py read <your-google-doc-id> --tab <your-tab-id>
```

Extract the approved response block (after the ⭐ marker). This is the approved template to base replies on.

### Step 3 — Search for new emails

Search Gmail for emails to the shared inbox after the last-run date:

- Use `label: all` to catch everything (inbox, forums, etc.)
- Use the `after:` date from Step 1
- Exclude emails **sent by the user** (from: your-email) — we only want inbound emails

### Step 4 — Filter out already-replied emails

For each inbound email found:

1. Read the full message to get the thread context.
2. Search for replies in the same thread (by subject or thread). If the user has already replied, **skip** that email and note it as "already handled."

### Step 5 — Classify and draft responses

For each **unreplied** email, carefully read the full message and classify it into one of these categories. **Pay close attention to context clues** — don't just pattern-match keywords. Understand what the sender is actually asking for.

| Category | Signals | Draft approach |
|----------|---------|----------------|
| **Activation request** | Sender wants to enable a feature ("enable", "turn on", "opt in", "activate", "join beta") | Use the standard activation response with enrollment link |
| **Troubleshooting — version issue** | "not working", "failure", "doesn't show", app version mentioned | Tell them to update to the minimum required version. |
| **Troubleshooting — already enabled** | Sender clearly already has the feature enabled but is experiencing issues | Ask for specifics — screenshots, examples, device/app details. Do NOT tell them to enable since they already have it. |
| **Feature request** | Requesting custom behavior or configuration not currently supported | Acknowledge the request, explain current behavior, note it's not possible at the moment. |
| **General inquiry** | Broad questions about the feature, wanting more info before enabling | Use the response template and direct to enrollment page. |
| **Other / unclear** | Doesn't fit above categories, missing critical details | Flag for manual review — do NOT auto-draft. |

#### Drafting guidelines

- **Read the email carefully.** If the sender mentions issues with an already-enabled feature, do NOT suggest enabling — they already have it. Instead, ask clarifying questions (screenshots, examples).
- **Be concise and relevant.** Only include information that directly addresses what the sender asked about. Don't add boilerplate unless the sender is asking to join.
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
[1-2 line summary of what the sender asked]

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
date -u +"%Y-%m-%d" > ~/.email-triage-last-run
```

### Step 8 — Summary

Print a final summary:

```
✅ Email Triage Complete
   Emails found: X
   Already replied: X
   Drafts created: X
   Skipped: X
   Flagged for manual review: X
```

## Important Notes

- **Never auto-send** — always create Gmail drafts, never send directly.
- **Always use the reply draft type** so the response threads correctly.
- **Sign off with your name** in all drafts.
- If the doc fetch fails, fall back to the standard response: direct senders to the enrollment page.
