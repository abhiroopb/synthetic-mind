---
name: cash-rounding-responder
description: "Triages and drafts replies to feature-feedback@company.com emails since last run. Use when asked to respond to, triage, handle, draft, review, classify, or process feature feedback emails, feature requests, or seller inquiries."
---

# Cash Rounding Email Responder

Automatically triages new emails to `feature-feedback@company.com`, drafts context-aware replies using the feature reference doc, and lets the user approve/edit/skip each draft before sending.

> **STOP** if the `gdrive` skill is not available or the penny elimination doc cannot be fetched. Inform the user and ask how to proceed before drafting replies without the approved template.

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

Read the **"Overview"** tab from the feature reference doc for the approved seller-facing response:

```
Doc ID: 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE
Tab ID: t.eoei3otto5gk
```

Use the gdrive skill to read this tab:

```bash
cd ~/.agents/skills/gdrive && uv run gdrive-cli.py read 1WAPVMavQbnmnU83AWY7T1vGOCo92oZqSbhBMI6ZPhHE --tab t.eoei3otto5gk
```

Extract the seller-facing response block (after the marker). This is the approved template to base replies on.

### Step 3 — Search for new emails

Search Gmail for emails to `feature-feedback@company.com` after the last-run date:

- Use `label: all` to catch everything (inbox, forums, etc.)
- Use the `after:` date from Step 1
- Exclude emails sent by the current user — we only want inbound seller emails

### Step 4 — Filter out already-replied emails

For each inbound email found:

1. Read the full message to get the thread context.
2. Search for replies in the same thread. If the user has already replied, **skip** that email and note it as "already handled."

### Step 5 — Classify and draft responses

For each **unreplied** email, classify it using the rules in `references/classification-rules.md`. Pay close attention to context clues — understand what the seller is actually asking for.

### Step 6 — Present drafts to user

For **each** email, present a summary block with the sender, date, subject, classification, original message summary, and proposed draft. Then ask the user to **Send**, **Edit**, or **Skip**. Process emails one at a time.

### Step 7 — Update last-run timestamp

After all emails are processed, write the current date to the state file:

```bash
date -u +"%Y-%m-%d" > ~/.cash-rounding-last-run
```

### Step 8 — Summary

Print a final summary showing emails found, already replied, drafts created, skipped, and flagged for manual review.

## Important Notes

- **Never auto-send** — always create Gmail drafts, never send directly.
- **Always use the reply draft type** so the response threads correctly.
- If the doc fetch fails, fall back to the standard response: direct sellers to the feature access page in your dashboard.
