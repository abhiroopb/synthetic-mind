# POS Releases

> Query Point of Sale release train schedules, branch cuts, betas, rollout dates, and version info.

## What it does

POS Releases answers questions about the POS release train by combining two data sources: local CSV schedules containing projected dates for iOS and Android releases, and live Slack channel updates with actual train status, blockers, and delays. It synthesizes both sources into clear markdown tables showing branch cuts, betas, app store submissions, and rollout percentages. The skill understands the weekly branch cut cadence, the distinction between dry-run and real trains, and platform-specific rollout differences.

## Usage

Use this skill when you need information about POS release schedules, upcoming versions, or current rollout status.

**Trigger phrases:**
- "When is the next branch cut?"
- "What version is going to beta next?"
- "Show me the Q1 iOS release schedule"
- "What's currently live?"
- "What's the rollout status for version 6.45?"

## Examples

- `"When is the next branch cut?"` — Checks the current release state and derives the next Friday's branch cut version.
- `"Show me the Q1 2026 iOS release schedule"` — Reads the iOS schedule CSV and presents a table with branch cuts, betas, submissions, and rollout dates.
- `"What's currently live?"` — Searches Slack for the most recent "100% GA" announcement and reports the current production version.

## Why it was created

Release schedules are spread across CSVs, Notion pages, and Slack channels, making it hard to quickly answer "when does X ship?" This skill unifies all sources and presents a single, accurate answer — projected dates plus live status — in seconds.
