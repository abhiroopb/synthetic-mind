---
name: pos-releases
description: "Query POS release train schedules, branch cuts, betas, rollout dates, and version info from the go/posreleases Notion page. Use when asked about POS releases, release trains, branch cuts, betas, app store submissions, rollout percentages, next version, upcoming release, or release dates."
---

# POS Releases

Answers questions about Square Point of Sale release train schedules by querying the official POS Releases Notion page (go/posreleases) and recent Slack updates.

## Data Sources

### Slack Channels (primary source for live/recent data)
Search these channels using the `slack` skill for real-time release info:
- **#pos-release-train** — Primary channel for branch cut announcements, beta drops, rollout updates, blockers, and train status changes
- **#release-foundation-discuss** — Cross-platform release infrastructure discussions, tooling changes, and process updates
- **#squid-release-train** — SQUID-specific release train updates (device software tied to POS releases)

### Local CSV Data (exported from Notion — source of truth for projected dates)
- **iOS schedule:** `reference/2026-ios-release-schedule.csv`
  - Columns: Release, Release Train, Branch Cut, Beta, App Store Submission, 1%, 2%, 5%, 10%, 20%, 50%, 100%, Notes
- **Android schedule:** `reference/2026-android-release-schedule.csv`
  - Columns: Release Version, Release Train, Branch Cut, Beta, 10%, 25%, 50%, 100%, Notes

Read these CSVs to answer any schedule question. They contain the full 2026 projected schedule through Jan 2027.

### Notion Page (for live/updated data if CSVs become stale)
- **Parent page:** `https://www.notion.so/db5acde38502482790fba31398686382`
- **iOS database:** `https://www.notion.so/2df70293beed802e8a39d9224044a843`
- **Android database:** `https://www.notion.so/2df70293beed80e89488e7394c221d12`

## Workflow

1. **Read the CSV schedule first** — read `reference/2026-ios-release-schedule.csv` and/or `reference/2026-android-release-schedule.csv` to get the projected dates. Filter to relevant rows based on today's date or the user's question.
2. **Search Slack for live status** — load the `slack` skill and run `scripts/get-release-status.sh` or search the channels for recent updates:
   - For branch cuts: search `"branch cut" in:#pos-release-train`
   - For betas: search `"beta" in:#pos-release-train`
   - For rollout/GA: search `"rollout" OR "GA" OR "100%" in:#pos-release-train`
   - For blockers/issues: search `"blocker" OR "blocked" in:#pos-release-train`
   - Channel IDs: #pos-release-train = C02FFLH8H, SQUID updates = CAMTTU16D
3. **Synthesize** — combine CSV (projected schedule) with Slack (actual/live status). If Slack shows a date change, blocker, or delay, note it alongside the projected date.
4. **Present results as a markdown table** — always include a clear, well-formatted table. Include the most relevant columns:
   - For schedule questions: Release, Branch Cut, Beta, key rollout dates (1%/10%, 100%)
   - For "when" questions: focus on the specific milestone asked about
5. **Add context** — note whether dates are projected or confirmed via Slack. Recommend `#pos-release-train` for live updates.

## Important Notes
- Apple does NOT do phased rollouts like Android — they phase *automatic updates* over a week, but the app is immediately available for manual download once released.
- Android rollout percentages: 10%, 25%, 50%, 100%.
- iOS rollout percentages: 1%, 2%, 5%, 10%, 20%, 50%, 100%.
- These are **projected dates** and subject to change.
- For live train status issues and blockers, check the RELOPS Issues databases.
- Slack channel for live updates: `#pos-release-train`
- Contact: `pos-release-ops@squareup.com`

## Scripts

- **`scripts/get-release-status.sh [ios|android|all] [days_back]`** — Fetches recent messages from #pos-release-train and the SQUID updates channel to show current train status. Run this first for any status question.

## Release Cadence

- **Branch cuts happen every Friday** (weekly)
- **Even versions (6.88, 6.90, 6.92, ..., 6.98) are DRY RUN** trains (practice cuts)
- **Odd versions (6.89, 6.91, 6.93, ..., 6.99) are real iOS/Android release trains**
- So actual releases ship **biweekly** (every other Friday's branch cut)
- After 6.99, versions continue to 7.x (Q2 2026 starts around 7.7)

## Slack Channel IDs (Square workspace)
- `#pos-release-train`: C02FFLH8H
- SQUID/X2/T2 updates: CAMTTU16D
- `#release-foundation-discuss`: search by name

## Example Queries & Responses

**User:** "When is the next branch cut?"
→ Run `scripts/get-release-status.sh` to get current state, then derive next Friday's branch cut version. Present both DRY RUN and real train dates.

**User:** "What version is going to beta next?"
→ Search Slack for the latest beta rolling announcement, identify the next version in the pipeline.

**User:** "Show me the Q1 2026 iOS release schedule"
→ Fetch iOS schedule from Notion, supplement with Slack for actual status.

**User:** "What's currently live?"
→ Run `scripts/get-release-status.sh` and look for the most recent "100% GA" announcement.
