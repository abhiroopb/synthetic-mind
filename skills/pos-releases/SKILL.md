---
name: pos-releases
description: "Query POS release train schedules, branch cuts, betas, rollout dates, and version info. Use when asked about POS releases, release trains, branch cuts, betas, app store submissions, rollout percentages, next version, upcoming release, or release dates."
---

# POS Releases

Answers questions about Point of Sale release train schedules by querying the official release schedule and recent Slack updates.

## Data Sources

### Slack Channels (primary source for live/recent data)
Search these channels using the `slack` skill for real-time release info:
- **#pos-release-train** — Primary channel for branch cut announcements, beta drops, rollout updates, blockers, and train status changes
- **#release-foundation-discuss** — Cross-platform release infrastructure discussions, tooling changes, and process updates
- **#device-release-train** — Device-specific release train updates

### Local CSV Data (source of truth for projected dates)
- **iOS schedule:** `reference/2026-ios-release-schedule.csv`
  - Columns: Release, Release Train, Branch Cut, Beta, App Store Submission, 1%, 2%, 5%, 10%, 20%, 50%, 100%, Notes
- **Android schedule:** `reference/2026-android-release-schedule.csv`
  - Columns: Release Version, Release Train, Branch Cut, Beta, 10%, 25%, 50%, 100%, Notes

Read these CSVs to answer any schedule question. They contain the full projected schedule.

### Notion Page (for live/updated data if CSVs become stale)
- Fetch release schedule databases from Notion if the CSVs are outdated.

## Workflow

1. **Read the CSV schedule first** — read the iOS and/or Android schedule CSVs to get the projected dates. Filter to relevant rows based on today's date or the user's question.
2. **Search Slack for live status** — search channels for recent updates:
   - For branch cuts: search `"branch cut" in:#pos-release-train`
   - For betas: search `"beta" in:#pos-release-train`
   - For rollout/GA: search `"rollout" OR "GA" OR "100%" in:#pos-release-train`
   - For blockers/issues: search `"blocker" OR "blocked" in:#pos-release-train`
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
- For live train status issues and blockers, check the release ops issues databases.
- Slack channel for live updates: `#pos-release-train`
- Contact: `pos-release-ops@example.com`

## Scripts

- **`scripts/get-release-status.sh [ios|android|all] [days_back]`** — Fetches recent messages from release channels to show current train status. Run this first for any status question.

## Release Cadence

- **Branch cuts happen every Friday** (weekly)
- **Even versions are DRY RUN** trains (practice cuts)
- **Odd versions are real iOS/Android release trains**
- Actual releases ship **biweekly** (every other Friday's branch cut)

## Example Queries & Responses

**User:** "When is the next branch cut?"
→ Run `scripts/get-release-status.sh` to get current state, then derive next Friday's branch cut version.

**User:** "What version is going to beta next?"
→ Search Slack for the latest beta rolling announcement.

**User:** "Show me the Q1 2026 iOS release schedule"
→ Fetch iOS schedule from CSV/Notion, supplement with Slack.

**User:** "What's currently live?"
→ Run `scripts/get-release-status.sh` and look for the most recent "100% GA" announcement.
