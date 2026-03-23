---
name: feature-request-scanner
description: "Daily scan of Slack channels for product feature requests. Auto-classifies, scores urgency, deduplicates against your roadmap tool, writes to a tracking spreadsheet, and promotes high-priority items. Use when asked to scan feature requests, check feedback channels, or run daily feature intake."
---

# Feature Request Scanner

Daily automated scan of customer/seller feedback channels for feature requests. Classifies, scores urgency, deduplicates, and writes to a tracking spreadsheet — then promotes high-priority items to your roadmap tool.

## Channels to Scan

Configure the channels relevant to your product area:

| Channel ID | Name | Workspace | Content Type |
|---|---|---|---|
| `CHANNEL_001` | `#customer-feedback` | your-workspace | Raw in-app "Suggest a Feature" submissions |
| `CHANNEL_002` | `#churn-signal-digests` | your-workspace | AI-generated daily digests of churn signals |
| `CHANNEL_003` | `#feedback-intake` | your-workspace | GTM team structured submissions |
| `CHANNEL_004` | `#strategic-churn-threats` | your-workspace | Account Manager escalations for high-value customers |

## Tracking

- **Google Sheet:** `YOUR_SHEET_ID` — tab `Feature Requests`
- **Columns:** Feature | Priority | Product Area | Detailed Description | Source | Requester | Status | Notes
- **Last-run timestamp:** `~/.config/feature-request-scanner/last-run`
- **Roadmap tool base:** Configure your Airtable/Linear/Jira project for deduplication

## Workflow

### Step 1 — Determine Time Window

```bash
mkdir -p ~/.config/feature-request-scanner
LAST_RUN=$(cat ~/.config/feature-request-scanner/last-run 2>/dev/null || echo "")
```

If `LAST_RUN` is empty or older than 7 days, default to the last 24 hours. Otherwise scan from `LAST_RUN` to now. Use the Unix timestamp for Slack API's `oldest` parameter.

### Step 2 — Fetch Messages from All Channels (in parallel)

For each channel, fetch messages since the last run using your Slack CLI:

```bash
slack-cli get-channel-messages \
  --channel-id <CHANNEL_ID> --workspace your-workspace --limit 50
```

Filter messages by timestamp — only keep messages newer than `LAST_RUN`.

**For `#customer-feedback`:** Messages follow the format "New feedback received:" with structured fields (Customer, Vertical, Platform, Feedback). Extract the `Feedback` field.

**For `#churn-signal-digests`:** These are daily digest posts. Parse the digest for individual items with links back to the feedback channel.

**For `#feedback-intake`:** Messages follow the format "Submission from @user" with structured fields (Team Name, Customer Type, Product, Request Details). Extract `Product` and `Request Details`.

**For `#strategic-churn-threats`:** Messages follow the format with structured fields (AM Name, Customer Name, Annual Revenue, Why is this customer a churn threat, What specific outcome...). Extract the churn reason and outcome fields.

### Step 3 — Filter for Relevant Product Areas

Only keep messages that match your configured product area keywords (case-insensitive matching). Define keyword groups for each product area your team owns.

Example product areas and keywords:

**E-commerce / Online Store:**
- `ecom`, `e-commerce`, `online store`, `online ordering`, `website`, `web store`, `digital storefront`, `online checkout`, `shipping`, `delivery`, `pickup`

**Customer Profiles:**
- `profile`, `profiles`, `customer profile`, `business profile`, `public page`, `landing page`

**Checkout:**
- `checkout`, `payment flow`, `tipping`, `tip`, `gratuity`, `receipt`, `payment screen`

**General POS:**
- `pos`, `point of sale`, `register`, `kiosk`, `items`, `catalog`, `inventory`

**Always include** messages from `#strategic-churn-threats` regardless of keywords — these are high-signal by definition.

Discard messages that are clearly support issues (can't login, charge failing, etc.) rather than feature requests.

### Step 4 — Auto-Classify Each Request

For each filtered message, determine:

| Field | Logic |
|---|---|
| **Feature** | Short name (≤ 10 words) summarizing the request |
| **Priority** | See urgency scoring below |
| **Product Area** | Tag with one or more from your configured product tags |
| **Detailed Description** | 2-3 sentence summary of the request and rationale |
| **Source** | Slack permalink to the original message |
| **Requester** | `Customer feedback` (in-app), `GTM / Sales` (intake channel), `AM escalation` (churn threats), or `Internal feedback` |
| **Status** | `Needs triage` |
| **Notes** | Customer revenue if available, country, vertical, churn signal if present |

### Product Tagging

Every request gets tagged with **one or more** product tags. Apply primary tags first — these are the areas your team owns. A request can have multiple tags.

- In the spreadsheet, write tags comma-separated in the Product Area column: `Profiles, ECOM`
- In the Slack summary, show the primary tag first: `Profiles · ECOM`
- If none of the primary tags match, use the best-fit secondary tag
- Requests tagged with at least one primary tag get a slight priority boost (they're in your domain)

### Step 5 — Urgency Scoring

| Priority | Criteria |
|---|---|
| **P0** | Explicit churn threat from high-value customer (>$1M revenue), OR blocking a deal, OR multiple customers requesting same thing in 24h |
| **P1** | Churn signal (mentions switching/leaving), OR strategic AM escalation, OR feature gap causing significant revenue impact |
| **P2** | Clear feature request with business value, multiple customers affected, or improving competitive position |
| **P3** | Nice-to-have, single customer request, or exploratory |

### Step 6 — Deduplicate Against Existing Sheet & Roadmap

Before adding any row, check if a similar feature already exists in the tracking sheet **and** your roadmap tool.

#### 6a. Check Google Sheet

Read existing rows from your tracking sheet and compare the new request's `Feature` name against existing rows (semantic match, not just exact string).

#### 6b. Check Roadmap Tool

Search your roadmap tool (Airtable, Linear, Jira, etc.) for existing projects that match the request. Try 2-3 keyword variations from the feature name to catch matches.

#### 6c. Handle Duplicates

If a match is found in either source:

- **Don't add a duplicate row** to the sheet
- Note it as "+1" in the presentation
- If the new request has a higher priority signal, flag it for priority upgrade
- **Capture the existing status** — is it `In Progress`, `Backlog`, `Delivered`, etc.?
- **Build a link** if a roadmap record exists

#### 6d. Notify the Original Poster (with approval)

For each duplicate where the original Slack message has a clear poster (not a bot), **offer to reply in-thread** letting them know the request is tracked:

> "This request matches an existing roadmap project. Reply to the poster? (y/n)"

If approved, reply in the original Slack thread with a status-appropriate message:
- **In Progress:** Let them know it's being worked on with a link
- **Backlog:** Acknowledge it's tracked and being evaluated
- **Delivered:** Good news — it's shipped! Share the link
- **Sheet only (no roadmap record):** Acknowledge it's tracked

**Rules:**
- **Always ask for approval** before posting any Slack reply
- Show the draft reply in chat first
- Don't reply to bot-posted messages — only to human posters
- Don't reply if the message is older than 7 days (stale threads)
- Batch the approvals: present all planned replies together so the user can approve/skip in bulk

### Step 7 — Present Results for Review

Present all classified requests in a single table, grouped by priority:

```
## 🔍 Feature Request Scan — [Date]
Scanned [N] channels · [N] messages · [M] relevant requests found · [D] duplicates skipped

### 🔴 P0 — Critical
| # | Feature | Product Area | Source Channel | Customer/Revenue | Action |
|---|---------|-------------|----------------|-----------------|--------|

### 🟡 P1 — High
| # | Feature | Product Area | Source Channel | Signal | Action |
|---|---------|-------------|----------------|--------|--------|

### 🔵 P2 — Medium
| # | Feature | Product Area | Source Channel | Notes | Action |
|---|---------|-------------|----------------|-------|--------|

### ⚪ P3 — Low
| # | Feature | Product Area | Source Channel | Notes |
|---|---------|-------------|----------------|-------|

### 🔄 Duplicates (already tracked)
| # | Feature | Status | Roadmap Link | New Signal | Reply? |
|---|---------|--------|-------------|------------|--------|
```

### Step 8 — Write to Google Sheet

For each new (non-duplicate) request, append to the tracking sheet with columns: Feature, Priority, Product Area, Description, Source, Requester, Status, Notes.

### Step 9 — Promote to Roadmap (user-driven)

**Nothing is filed to the roadmap without explicit approval.** All items are written to the sheet first. Promotion happens interactively.

After presenting the results table, go through P0 and P1 items one at a time:

> **[Feature name]** — [Product Area] · [Priority] · [1-line description]
> Promote to roadmap? (y / n / skip all)

For P2/P3 items, just mention they're in the sheet and can be promoted later.

### Step 10 — Post Summary to Slack (with approval)

After presenting results and completing any roadmap filings, offer to post a formatted summary to a Slack channel. **Only post after explicit user approval.** Never auto-post.

### Step 11 — Update Timestamp

```bash
date -u +%Y-%m-%dT%H:%M:%SZ > ~/.config/feature-request-scanner/last-run
```

## Start-of-Day Integration

When run as part of start-of-day, present a **condensed summary** before other triage sections:

```
## 🔍 Feature Request Scan (since yesterday)
[N] new requests found across [N] channels · [P0] critical · [P1] high · [P2] medium

🔴 **P0:** [Feature name] — [Customer] threatening churn over [issue] → Promote to roadmap? (y/n)
🟡 **P1:** [Feature name] — [N] customers requesting [thing] → Promote to roadmap? (y/n)
📝 **P2-P3:** [N] items added to tracking sheet
🔄 **Duplicates:** [N] already tracked · [N] replies drafted
```

## Weekly Rollup

Auto-generate a "Top 10 Feature Requests This Week" summary every week (or on demand). Write it to a shared doc for leadership review.

### Trigger

- **Automatic:** During start-of-day on Mondays
- **Manual:** "weekly rollup", "feature request rollup", "top feature requests this week"

### Rollup Workflow

1. **Gather the week's data** from the tracking sheet
2. **Rank and select top 10** by priority, duplicate count, primary tag match, and signal strength
3. **Write to shared doc** with a formatted table and theme summary
4. **Update timestamp** for next rollup

## Manual Trigger

The user can also trigger this skill manually:
- "scan feature requests"
- "check feedback channels"
- "run feature intake"
- "what's new in customer feedback?"
- "weekly rollup" / "feature request rollup"

## Notes

- Digest channels produce daily AI digests — use these as a shortcut when available, but still scan raw channels for items the digest may have missed
- Bot/app messages in feedback channels follow consistent formats — parse the structured fields
- For strategic churn threats, always capture the revenue and customer name — these are high-signal for prioritization
- The tracking sheet and roadmap tool are complementary: the sheet is the intake funnel, the roadmap is where items get staffed and tracked
- When in doubt about product area classification, default to `Other` and let the user re-classify during triage
