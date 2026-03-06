# Logging Feature Requests

> Digest feature requests from Slack threads and log them to a tracking spreadsheet.

## What it does

This skill takes a Slack thread link, fetches the full conversation, extracts and summarizes the feature request (including priority, product area, description, and requester type), and appends a structured row to a Google Sheets tracking spreadsheet. It confirms the extracted data with you before writing, ensuring accuracy. Priority is inferred from the thread's tone, urgency, and business impact.

## Usage

Paste a Slack message link when you want to capture a feature request, or explicitly ask to log one.

**Trigger phrases:**
- Paste a Slack thread URL
- "Log this feature request"
- "Record this feature request from Slack"
- "Add this to the feature requests sheet"

## Examples

- Paste `https://workspace.slack.com/archives/C123/p1234567890` — Fetches the thread, extracts the feature request details, presents a summary table for review, then appends to the tracking sheet.
- `"Log the feature request from this Slack thread: [URL]"` — Same workflow with explicit instruction.

## Why it was created

Feature requests come in through Slack constantly and are easy to lose track of. This skill creates a fast, standardized pipeline from Slack conversation to structured tracking sheet, ensuring nothing falls through the cracks.
